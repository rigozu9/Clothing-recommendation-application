import os
import json
import argparse
from pathlib import Path

import pandas as pd

# ijson is used to parse large JSON files in a memory-efficient way
import ijson

# tqdm is used to show progress bars for long-running operations
from tqdm import tqdm

import psycopg
from psycopg import sql

import csv
from io import StringIO

from dotenv import load_dotenv
load_dotenv()

def get_conn() -> psycopg.Connection:
   """
    Load environment variables from .env file
   """
   return psycopg.connect(
        host=os.getenv("PGHOST"),
        port=int(os.getenv("PGPORT")),
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        autocommit=True,
    )

def create_schema_and_tables(conn):
    with conn.cursor() as cursor:
        cursor.execute("CREATE SCHEMA IF NOT EXISTS raw;")

        # Excel label map: make it typed (no need for JSONB here)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw.imat_label_map (
            label_id INTEGER PRIMARY KEY,
            task_id INTEGER NOT NULL,
            label_name TEXT NOT NULL,
            task_name TEXT NOT NULL
        );
        """)

        # info + license (one row per split)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw.imat_info (
            split TEXT PRIMARY KEY,
            info JSONB NOT NULL
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw.imat_license (
            split TEXT PRIMARY KEY,
            license JSONB NOT NULL
        );
        """)

        # images
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw.imat_images (
            split TEXT NOT NULL,
            image_id BIGINT NOT NULL,
            url TEXT NOT NULL,
            PRIMARY KEY (split, image_id)
        );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS imat_images_image_id_idx ON raw.imat_images(image_id);")

        # annotations (label_ids is a JSON array of strings in your sample)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw.imat_annotations (
            split TEXT NOT NULL,
            image_id BIGINT NOT NULL,
            label_ids JSONB NOT NULL,
            PRIMARY KEY (split, image_id)
        );
        """)
        # create indexes for efficient querying
        cursor.execute("CREATE INDEX IF NOT EXISTS imat_annotations_image_id_idx ON raw.imat_annotations(image_id);")
        # GIN = Generalized Inverted Index.
        cursor.execute("CREATE INDEX IF NOT EXISTS imat_annotations_label_ids_gin ON raw.imat_annotations USING GIN (label_ids);")

def copy_rows(conn, table_name: str, columns, rows):
    """
    Bulk-load rows into Postgres using COPY ... FROM STDIN (FAST).

    Args:
      conn: psycopg connection
      table_name: table to load into (prefer schema-qualified, e.g. "raw.imat_images")
      columns: list/tuple of column names in the order your row tuples are provided
      rows: iterable of row tuples/lists, e.g. [("train", 1, "http://..."), ...]
    """

    with conn.cursor() as cursor:
        # Build a safe SQL fragment for the column list.
        # Example: columns = ["split", "image_id", "url"]
        # col_list becomes the SQL: split, image_id, url
        #
        # sql.Identifier(...) ensures proper quoting if column names have special chars.
        col_list = sql.SQL(", ").join(map(sql.Identifier, columns))

        # Build the COPY command.
        # Example result:
        #   COPY raw.imat_images (split, image_id, url) FROM STDIN WITH (FORMAT CSV)
        #
        # NOTE: table_name is injected as raw SQL here via sql.SQL(table_name).
        # That is OK if table_name is a constant you control (not user input).
        q = sql.SQL("COPY {} ({}) FROM STDIN WITH (FORMAT CSV)").format(
            sql.SQL(table_name),
            col_list
        )

        # Start COPY streaming session
        with cursor.copy(q) as copy:
            # Create an in-memory "file" where csv.writer can write one CSV line
            wbuf = StringIO()
            writer = csv.writer(wbuf)

            # Stream each row into COPY
            for r in rows:
                # Clear the buffer (so we reuse the same StringIO object)
                wbuf.seek(0)
                wbuf.truncate(0)

                # Convert the Python row into a single CSV line (handles quoting/commas safely)
                writer.writerow(r)

                # Send that CSV line to Postgres COPY stream
                copy.write(wbuf.getvalue())


def load_label_map(conn, xlsx_path: Path):
    if not xlsx_path.exists():
        raise FileNotFoundError(xlsx_path)

    df = pd.read_excel(xlsx_path)

    with conn.cursor() as cursor:
        cursor.execute("TRUNCATE raw.imat_label_map;")

    def generate():
        for _, row in df.iterrows():
            yield (
                int(row["labelId"]),
                int(row["taskId"]),
                str(row["labelName"]),
                str(row["taskName"]),
            )

    copy_rows(
        conn,
        "raw.imat_label_map",
        ("label_id", "task_id", "label_name", "task_name"),
        generate()
    )
    print(f"[OK] label_map loaded: {len(df)} rows -> raw.imat_label_map")

def load_imat_split_info_and_license(conn, json_path: Path, split: str):
    if not json_path.exists():
        raise FileNotFoundError(json_path)

    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    info_obj = data.get("info")
    license_obj = data.get("license")

    # validation.json may not contain these; that's OK
    if info_obj is None and license_obj is None:
        print(f"[SKIP] {split}: no info/license in {json_path.name}")
        return

    # Re-runnable: delete any existing rows for this split
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM raw.imat_info WHERE split = %s;", (split,))
        cursor.execute("DELETE FROM raw.imat_license WHERE split = %s;", (split,))

    if info_obj is not None:
        copy_rows(
            conn,
            "raw.imat_info",
            ("split", "info"),
            [(split, json.dumps(info_obj, ensure_ascii=False))]
        )

    if license_obj is not None:
        copy_rows(
            conn,
            "raw.imat_license",
            ("split", "license"),
            [(split, json.dumps(license_obj, ensure_ascii=False))]
        )

    print(f"[OK] {split}: loaded info/license (if present)")

def load_imat_split_images(conn, json_path: Path, split: str, batch_size: int = 20000):
    """
    Streams data["images"] array from the JSON and loads into raw.imat_images:
      (split, image_id, url)

    Re-runnable: delete existing rows for this split first.
    """
    if not json_path.exists():
        raise FileNotFoundError(json_path)

    # Remove old rows for this split (re-runnable)
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM raw.imat_images WHERE split = %s;", (split,))

    total = 0
    buffer = []

    def flush():
        nonlocal total
        if not buffer:
            return
        copy_rows(conn, "raw.imat_images", ("split", "image_id", "url"), buffer)
        total += len(buffer)
        buffer.clear()

    with json_path.open("rb") as f:
        # ijson.items(f, "images.item") streams each item inside the images array
        for img in tqdm(ijson.items(f, "images.item"), desc=f"iMAT {split} images"):
            # img expected like: {"url": "...", "imageId": "1"}
            image_id = int(img["imageId"])
            url = str(img["url"])

            buffer.append((split, image_id, url))
            if len(buffer) >= batch_size:
                flush()

    flush()
    print(f"[OK] {split}: loaded images -> raw.imat_images ({total} rows)")

def load_imat_split_annotations(conn, json_path: Path, split: str, batch_size: int = 20000):
    """
    Streams data["annotations"] array and loads into raw.imat_annotations:
      (split, image_id, label_ids)

    label_ids is stored as JSONB array (we send a JSON string).
    Re-runnable: delete existing rows for this split first.
    """
    if not json_path.exists():
        raise FileNotFoundError(json_path)

    # Remove old rows for this split (re-runnable)
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM raw.imat_annotations WHERE split = %s;", (split,))

    total = 0
    buffer = []

    def flush():
        nonlocal total
        if not buffer:
            return
        copy_rows(conn, "raw.imat_annotations", ("split", "image_id", "label_ids"), buffer)
        total += len(buffer)
        buffer.clear()

    with json_path.open("rb") as f:
        for ann in tqdm(ijson.items(f, "annotations.item"), desc=f"iMAT {split} annotations"):
            # ann expected like: {"labelId": ["95","66",...], "imageId": "1"}
            image_id = int(ann["imageId"])
            label_ids = ann["labelId"]  # list of strings in your sample

            # Store as JSONB: must be valid JSON string
            buffer.append((split, image_id, json.dumps(label_ids, ensure_ascii=False)))

            if len(buffer) >= batch_size:
                flush()

    flush()
    print(f"[OK] {split}: loaded annotations -> raw.imat_annotations ({total} rows)")

def load_imat_split(conn, json_path: Path, split: str):
    """
    Convenience wrapper: loads one split JSON into all four raw tables.
    """
    load_imat_split_info_and_license(conn, json_path, split)
    load_imat_split_images(conn, json_path, split)
    load_imat_split_annotations(conn, json_path, split)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--imat-dir", default="imat", help="Path to imat directory")
    args = ap.parse_args()

    imat_dir = Path(args.imat_dir).resolve()

    conn = get_conn()
    try:
        create_schema_and_tables(conn)
        load_label_map(conn, imat_dir / "label_map_228.xlsx")
        load_imat_split(conn, imat_dir / "train.json", "train")
        load_imat_split(conn, imat_dir / "validation.json", "validation")
    finally:
        conn.close()


if __name__ == "__main__":
    main()