# 四角形分割のために多角形から凹頂点のL点を抽出する
# L点のリストとR点のリストを作成する
# Classify into L point and R point

import math
import sympy as sp
import math
import itertools

# テストデータ
cords = [[3.9,0],[4.1,2],[2,2.1],[2,5],[0,5.1],[0.1,2],[-2,2.1],[-2,0.5]]
# print(cords[2])
# 頂点数，メインのプログラムからnew_nodesを受け取る
new_nodes = len(cords)
# print(new_nodes)
order = {'L1': 2, 'R1': 3, 'R2': 4, 'L2': 5, 'R3': 6, 'R4': 7, 'R5': 0, 'R6': 1}
# print(order['L1'])

# L点のリストを用意する
L_list = []
# R点のリストを用意する
R_list = []
# R点の予備のリストを用意する
R_suslist = []

# 外積を求めて，左回りか右回りかを調べる．
# XY平面上でZ軸方向に右ネジを回して（反時計回り）進む方向が正
# 頂点の並びは左回り（反時計回り）が基本とする
# 左回りの場合に，求まった内積の角度から凹内角の角度を求める．
def ccw_Chk(cnt):
    # 外積を計算する
    xs = cords[cnt][0]
    ys = cords[cnt][1]
    if (cnt == 0):
        xp = cords[new_nodes - 1][0]
        yp = cords[new_nodes - 1][1]
        xn = cords[cnt + 1][0]
        yn = cords[cnt + 1][1]
    elif (cnt == new_nodes - 1):
        xp = cords[cnt - 1][0]
        yp = cords[cnt - 1][1]
        xn = cords[0][0]
        yn = cords[0][1]
    else:
        xp = cords[cnt - 1][0]
        yp = cords[cnt - 1][1]
        xn = cords[cnt + 1][0]
        yn = cords[cnt + 1][1]
    global S
    S = (xp - xs) * (yn - ys) - (xn - xs) * (yp - ys)
    print("S=", S)
    # 外積の結果で左回りか右回りか判断する
    print(cnt)
    if (S > 0):  # 左回り
        print('LH')
    elif (S < 0):  # 右回り
        print('RH')

# ベクトルの長さを求める
def vector_Length(x1, y1, x0, y0):
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
def cross_Angle(ax, ay, bx, by, al, bl):
    # cosθを求める
    taihen = math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)
    cos_theta = (al ** 2 + bl ** 2 - taihen ** 2) / (2 * al * bl)
    print("cosθ", cos_theta)
    # 角度を求める
    global theta
    theta = math.degrees(math.acos(cos_theta))
    # print("角度", theta)

# def flat_vert(new_nodes): で内積を求めている．
# def load_data(self):　の中なので，メソッドは別に用意すべき．
# 内積を求めて３点からなら角度を求める，
# しかし，内角が求まらない．180°以下しか求まらない．
def inner_Product(cnt):
    print(cnt)
    # 隣合う点との間の距離から辺の長さを求める
    if (cnt != 0):    # 最初の頂点でない時
        # ベクトルAのX座標の差分
        vect_ax = cords[cnt - 1][0] - cords[cnt][0]
        # ベクトルAのY座標の差分
        vect_ay = cords[cnt - 1][1] - cords[cnt][1]
        # ベクトルAの長さ
        vector_a = math.sqrt(vect_ax ** 2 + vect_ay ** 2)
        print(cnt, "ベクトルAx", vect_ax)
        print(cnt, "ベクトルAy", vect_ay)
        print(cnt, "ベクトルA", vector_a)
    else:
        vect_ax = cords[cnt - 1][0] - cords[0][0]
        vect_ay = cords[cnt - 1][1] - cords[0][1]
        vector_a = math.sqrt(vect_ax ** 2 + vect_ay ** 2)
        print(cnt, "ベクトルAx", vect_ax)
        print(cnt, "ベクトルAy", vect_ay)
        print(cnt, "ベクトルA", vector_a)
    if (cnt != (new_nodes - 1)):    # 最後の頂点でない時
        # ベクトルBのX座標の差分
        vect_bx = cords[cnt + 1][0] - cords[cnt][0]
        # ベクトルBのY座標の差分
        vect_by = cords[cnt + 1][1] - cords[cnt][1]
        # ベクトルBの長さ
        vector_b = math.sqrt(vect_bx ** 2 + vect_by ** 2)
        print(cnt, "ベクトルBx", vect_bx)
        print(cnt, "ベクトルBy", vect_by)
        print(cnt, "ベクトルB", vector_b)
    else:
        vect_bx = cords[0][0] - cords[cnt][0]
        vect_by = cords[0][1] - cords[cnt][1]
        vector_b = math.sqrt(vect_bx ** 2 + vect_by ** 2)
        print(cnt, "ベクトルBx", vect_bx)
        print(cnt, "ベクトルBy", vect_by)
        print(cnt, "ベクトルB", vector_b)
    # 角度を求める
    cross_Angle(vect_ax, vect_ay, vect_bx, vect_by, vector_a, vector_b)
    print(cnt, "角度", theta)

# 四角形分割プログラム
# L点を抽出する．凹角の角度制限を確認する．
# Ｎ角形　内角数：N=2x,x=N/2，凹角数：L=x-2=N/2-2
L_cnt = new_nodes / 2 - 2
order = {}  # 頂点データの並び順を格納する
L_num = 1
R_num = 1

for i in range(new_nodes):

    # 外積を求めてL点かどうか判断する
    ccw_Chk(i)
    if (S > 0): # L点の場合の処理
        # 内積から角度を求める
        inner_Product(i)
        naikaku = 360 - theta
        print(naikaku)
        # 凹角の角度制限
        if (naikaku > 280 or naikaku < 260):
            break
            # break   #子ループから抜けて親ループから抜ける為のbreak
        else:
            L_list.append(cords[i])
            order["L" + str(L_num)] = i
            L_num += 1
    else:   # R点の場合の処理
        if not L_list:
            R_suslist.append(cords[i])
        else:
            R_list.append(cords[i])
            order["R" + str(R_num)] = i
            R_num += 1

R_list.extend(R_suslist)
sus_len = len(R_suslist)
for j in range(sus_len):
    order["R" + str(R_num)] = j
    R_num += 1

print(L_list)
print(R_list)
print(R_suslist)
print(order)

# L点と対抗する辺との直交条件の確認
# 2点を通る直線の式を求める
# ２直線の交点を求める
# ２直線が交差する角度を求める
# Angle at which two straight lines inter_Sect

# 2点を通る直線の方程式
def make_Line(x1, y1, x2, y2):
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
def inter_Sect(a1, b1, a2, b2):
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

for LR_key in order:
    ini = LR_key[0]
    if (ini == 'L'):
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
        if ((num + 2) > (new_nodes - 1)):
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
        line_1 = make_Line(x1, y1, x2, y2)
        print(line_1)
        m1 = line_1['m']
        n1 = line_1['n']
        # 対向する辺の両端座標
        x1 = taiko_cords[0][0]
        y1 = taiko_cords[0][1]
        x2 = taiko_cords[1][0]
        y2 = taiko_cords[1][1]
        # 対向する直線の方程式
        line_2 = make_Line(x1, y1, x2, y2)
        print(line_2)
        m2 = line_2['m']
        n2 = line_2['n']

        # ２直線の交点を求める
        inter_Sect(m1, n1, m2, n2)
        print(ans)
        int_X = ans[x]
        int_Y = ans[y]

        # 内積を計算して交差する角度を求める
        # ベクトルA　交点とL1点を結ぶベクトル
        vector_Length(choku_cords[0][0], choku_cords[0][1], int_X, int_Y)
        vect_ax = vect_x
        vect_ay = vect_y
        vector_a = vector

        # ベクトルB　交点と２つ目の点を結ぶベクトル
        vector_Length(taiko_cords[0][0], taiko_cords[0][1], int_X, int_Y)
        vect_bx = vect_x
        vect_by = vect_y
        vector_b = vector

        # ベクトルの交差角度
        cross_Angle(vect_ax, vect_ay, vect_bx, vect_by, vector_a, vector_b)
        # 角度を求める
        print("角度", theta)

        if (theta < 60 or theta > 120):
            break
    else:
        continue
    print("Break")
print("END")
