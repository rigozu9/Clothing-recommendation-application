import pandas as pd

path = "deepfashion/annotations/list_attr_cloth.txt"

rows = []
with open(path, "r", encoding="utf-8") as f:
    next(f)  # first row: number of attributes
    next(f)  # second row: header
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        attr_type = int(parts[-1])          # last token
        attr_name = " ".join(parts[:-1])    # everything before last token
        rows.append((attr_name, attr_type))

attr = pd.DataFrame(rows, columns=["attribute_name", "attribute_type"])

# "materials" ~ fabric-related
fabric = attr[attr["attribute_type"] == 2]

# print("Total attributes:", len(attr))
# print("Fabric/material attributes:", len(fabric))
# print(fabric.head(100))

print(fabric[fabric["attribute_name"].str.contains("polyester", case=False, na=False)].head(100))
