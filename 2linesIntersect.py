# 2点を通る直線の式を求める
# ２直線の交点を求める
# ２直線が交差する角度を求める
# Angle at which two straight lines intersect

import sympy as sp
import math
import itertools

# テストデータ
cords = [[3.9,0],[4.1,2],[2,2.1],[2,5],[0,5.1],[0.1,2],[-2,2.1],[-2,0.5]]
print(cords[2])
order = {'L1': 2, 'R1': 3, 'R2': 4, 'L2': 5, 'R3': 6, 'R4': 7, 'R5': 0, 'R6': 1}
print(order['L1'])

L_list = [[2, 2.1], [0.1, 2]]
R_list = [[2, 5], [0, 5.1], [-2, 2.1], [-2, 0.5], [3.9, 0], [4.1, 2]]

new_nodes = len(order)
print(new_nodes)

# 2点を通る直線の方程式
def makeLine(x1, y1, x2, y2):
    line = {}
    if y1 == y2:
        # y軸に平行な直線
        line["y"] = y1
    elif x1 == x2:
        # x軸に平行な直線
        line["x"] = x1
    else:
        # y = mx + n
        line["m"] = (y2 - y1) / (x2 - x1)
        line["n"] = y1 - line["m"] * x1
    # print(line)
    return line

# 2直線の交点を求める
def interSect(a1, b1, a2, b2):
    global x
    x = sp.Symbol('x')
    global y
    y = sp.Symbol('y')
    # expr1 = sp.Eq(y, 70*x)
    expr1 = sp.Eq(y, a1 * x + b1)
    # expr2 = sp.Eq(y, 100*x-600)
    expr2 = sp.Eq(y, a2 * x + b2)
    global ans
    ans = sp.solve([expr1, expr2])
    return ans # {x: 20, y: 1400}が返ってくる

# ベクトルの長さを求める
def vectorLength(x1, y1, x0, y0):
    global vect_x
    vect_x = x1 - x0
    # ベクトルAのY座標の差分
    global vect_y
    vect_y = y1 - y0
    # ベクトルAの長さ
    global vector
    vector = math.sqrt(vect_x ** 2 + vect_y ** 2)
    print("ベクトルx", vect_x)
    print("ベクトルy", vect_y)
    print("ベクトル", vector)

# ベクトルの交差角度を求める
def crossAngle(ax, ay, bx, by, al, bl):
    # cosθを求める
    taihen = math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)
    cos_theta = (al ** 2 + bl ** 2 - taihen ** 2) / (2 * al * bl)
    print("cosθ", cos_theta)
    # 角度を求める
    global theta
    theta = math.degrees(math.acos(cos_theta))
    # print("角度", theta)

for LR_key in order:
    ini = LR_key[0]
    if(ini == 'L'):
        print(LR_key)
        # L点の直交条件．対向する辺との交点の角度制限を確認する．
        num = order[LR_key]
        # print(num)

        # 直交する辺は．L点と1つ前の点で結ばれる線分
        # 直交する辺の座標ペア
        choku_cords = []
        choku_cords.append(cords[num])
        choku_cords.append(cords[num - 1])

        # 対向する辺は，L点から２つ目と３つ目の点で結ばれる線分
        # 対向する辺の座標ペア
        # hen_coprds = [[] for _ in range(hen_cnt)]
        taiko_cords = []
        if((num + 2) > (new_nodes - 1)):
            taiko_cords.append(cords[num + 2 - new_nodes])
        else:
            taiko_cords.append(cords[num + 2])
        if ((num + 3) > (new_nodes - 1)):
            taiko_cords.append(cords[num + 2 - new_nodes + 1])
        else:
            taiko_cords.append(cords[num + 3])

        print("choku_cords", choku_cords)
        print("taiko_cords", taiko_cords)

        # print(list(itertools.chain.from_iterable(choku_cords)))
        # print(tuple(itertools.chain.from_iterable(choku_cords)))

        # 直交する辺の両端座標（一方がL点）
        x1 = choku_cords[0][0]
        y1 = choku_cords[0][1]
        x2 = choku_cords[1][0]
        y2 = choku_cords[1][1]
        # 直交する直線の方程式
        line_1 = makeLine(x1, y1, x2, y2)
        print(line_1)
        m1 = line_1['m']
        n1 = line_1['n']
        # 対向する辺の両端座標
        x1 = taiko_cords[0][0]
        y1 = taiko_cords[0][1]
        x2 = taiko_cords[1][0]
        y2 = taiko_cords[1][1]
        # 対向する直線の方程式
        line_2 = makeLine(x1, y1, x2, y2)
        print(line_2)
        m2 = line_2['m']
        n2 = line_2['n']

        # ２直線の交点を求める
        interSect(m1, n1, m2, n2)
        print(ans)
        int_X = ans[x]
        int_Y = ans[y]

        # 内積を計算して交差する角度を求める
        # ベクトルA　交点とL1点を結ぶベクトル
        vectorLength(choku_cords[0][0], choku_cords[0][1], int_X, int_Y)
        vect_ax = vect_x
        vect_ay = vect_y
        vector_a = vector

        # ベクトルB　交点と２つ目の点を結ぶベクトル
        vectorLength(taiko_cords[0][0], taiko_cords[0][1], int_X, int_Y)
        vect_bx = vect_x
        vect_by = vect_y
        vector_b = vector

        # ベクトルの交差角度
        crossAngle(vect_ax, vect_ay, vect_bx, vect_by, vector_a, vector_b)
        # 角度を求める
        print("角度", theta)

        if(theta < 60 or theta > 120):
            break
    else:
        continue
    print("Break")
print("END")
