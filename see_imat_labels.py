import pandas as pd

df = pd.read_excel("imat/label_map_228.xlsx")

materials_draft = df[["taskName", "labelName"]]

materials_only = materials_draft[materials_draft["taskName"] == "material"]
print(materials_only)