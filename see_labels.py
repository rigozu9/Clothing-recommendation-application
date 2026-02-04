import pandas as pd

df = pd.read_excel("label_map_228.xlsx")

materials = df[df["taskName"] == "material"][["labelId", "labelName"]].sort_values("labelName")
print(materials.head(50))
print("Material label count:", len(materials))
