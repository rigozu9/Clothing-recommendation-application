import json

with open("train.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# print(data.keys())
for annotation in data["annotations"]:
    print(annotation)
    break  # just print the first annotation