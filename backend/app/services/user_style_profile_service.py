from sqlalchemy import text
from sqlalchemy.orm import Session

def get_user_style_plot_data(db: Session, user_id: int, token_type: str = "color"):
    query = text("""
        WITH user_tokens AS (
            SELECT
                uli.user_id,
                t.token
            FROM analytics.user_liked_item uli
            JOIN analytics.int_imat_image_tokens t
                ON t.image_id = uli.image_id
            WHERE uli.user_id = :user_id
        ),

        parsed_tokens AS (
            SELECT
                user_id,
                split_part(token, ':', 1) AS token_type,
                split_part(token, ':', 2) AS token_value
            FROM user_tokens
        ),

        token_counts AS (
            SELECT
                user_id,
                token_type,
                token_value,
                COUNT(*) AS token_count
            FROM parsed_tokens
            WHERE token_type = :token_type
            GROUP BY user_id, token_type, token_value
        ),

        ranked_tokens AS (
            SELECT
                user_id,
                token_type,
                token_value,
                token_count,
                RANK() OVER (
                    PARTITION BY user_id, token_type
                    ORDER BY token_count DESC, token_value ASC
                ) AS token_rank
            FROM token_counts
        )

        SELECT
            token_value,
            token_count
        FROM ranked_tokens
        ORDER BY token_rank, token_value
    """)

    result = db.execute(
        query,
        {
            "user_id": user_id,
            "token_type": token_type,
        },
    )

    rows = result.fetchall()

    labels = [row[0] for row in rows]
    values = [row[1] for row in rows]

    return {
        "labels": labels,
        "values": values,
    }