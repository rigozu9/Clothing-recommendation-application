import pandas as pd

df = pd.read_excel("imat/label_map_228.xlsx")

# materials_draft = df[["taskName", "labelName"]]

# materials_only = materials_draft[materials_draft["taskName"] == "material"]
# print(materials_only)

print(df.columns)
print(df["labelId"][0])
print(df["taskId"][0])
print(df["labelName"][0])
print(df["taskName"][0])
