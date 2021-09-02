import json

json_open = open('test.json', 'r', encoding="utf-8")
json_load = json.load(json_open)

print(json_load)