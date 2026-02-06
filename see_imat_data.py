import json

with open("imat/train.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# print(data.keys())
for annotation in data.keys():
    # print(annotation)
    break  # just print the first annotation

print(data.keys())
print(data["annotations"][0])
print(data["images"][0])
print(data["info"])
print(data["license"])