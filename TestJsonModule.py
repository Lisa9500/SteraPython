import json

f = open('sample.json', 'r', encoding="utf-8")
data = json.load(f)
f.close()

print("普通に表示")
print(data)
print("キレイに表示")
print(json.dumps(data, sort_keys=True, indent=4))
print("中身に直接アクセス")
print(data[0]["name"])
print(data[0]["appearedIn"])
print("Name:{obj[name]}, appearedIn:{obj[appearedIn]}".format(obj=data[0]))
print("influencedBy", ",".join(data[0]["influencedBy"]))