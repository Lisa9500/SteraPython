import json

fj = open('hutsu_tate.json', 'r', encoding='utf-8')
# JSONファイルを辞書型データに変換する
with fj:
    src = json.load(fj)
    print(src)
    ftr = src["type"]
    print(ftr)
    # prop = src["properties"]
    # print(prop)