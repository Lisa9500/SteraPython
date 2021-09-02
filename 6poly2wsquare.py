num = 6
cord2 = [[-75287.8699953546, -104688.98004354979], [-75271.89998301842, -104697.36998239889],
         [-75276.66000782167, -104698.1700180574], [-75280.75997580224, -104700.08995697794],
         [-75280.98000826316, -104698.8300253034], [-75286.059984843, -104699.68996762336],
         [-75287.8699953546, -104688.98004354979]]
print(cord2)
D1 = [-75273.71999730935, -104686.58996118378]
D2 = [-75276.45003970628, -104699.35995864532]
cord2.extend([D1])
print(cord2)

D1_num = num + 1

tops_dict = {'L1': 4, 'R1': 5, 'R2': 0, 'R3': 1, 'R4': 2, 'R5': 3}
print(tops_dict)

tops_dict['D1'] = D1_num
print(tops_dict)

rect_1 = dict(tops_dict)
print(rect_1)
# rect_1.pop('R2')
# rect_1.pop('R4')
pop_lst_1 = ['R3', 'R4', 'R5']
for i in pop_lst_1:
    rect_1.pop(i)
print(rect_1)

# 辞書の中味に従ってリストの座標データで四角形を作る
rect_1_list = []
for i in list(rect_1.values()):
    rect_1_list.append(cord2[i])
print(rect_1.values())
print(rect_1_list)

print(tops_dict)

rect_2 = dict(tops_dict)
print(rect_2)
pop_lst_2 = ['R1', 'R2', 'L1']
for i in pop_lst_2:
    rect_2.pop(i)
print(rect_2)

print(tops_dict)
