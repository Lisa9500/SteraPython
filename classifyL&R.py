# 四角形分割のために多角形から凹頂点のL点を抽出する
# L点のリストとR点のリストを作成する
# Classify into L point and R point

import math

# cords = [[0,0],[4,0],[4,2],[2,2],[2,5],[0,5],[0,2],[-2,2],[-2,0]]
cords = [[3.9,0],[4.1,2],[2,2.1],[2,5],[0,5.1],[0.1,2],[-2,2.1],[-2,0.5]]
angles = len(cords)
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
def ccwChk(cnt):
    # 外積を計算する
    xs = cords[cnt][0]
    ys = cords[cnt][1]
    if (cnt == 1):
        xp = cords[angles - 1][0]
        yp = cords[angles - 1][1]
        xn = cords[cnt + 1][0]
        yn = cords[cnt + 1][1]
    elif (cnt == angles - 1):
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
    # 外積の結果で左回りか右回りか判断する
    print(cnt)
    if (S > 0):  # 左回り
        print('LH')
    elif (S < 0):  # 右回り
        print('RH')

# def flat_vert(new_nodes): で内積を求めている．
# def load_data(self):　の中なので，メソッドは別に用意すべき．
# 内積を求めて３点からなら角度を求める，
# しかし，内角が求まらない．180°以下しか求まらない．
def innerProduct(cnt):
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
    if (cnt != (angles - 1)):    # 最後の頂点でない時
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
    # cosθを求める
    # cos_theta = (vect_ax * vect_ay + vect_bx * vect_by) / (vector_a * vector_b)
    taihen = math.sqrt((vect_ax - vect_bx) ** 2 + (vect_ay - vect_by) ** 2)
    cos_theta = (vector_a ** 2 + vector_b ** 2 - taihen ** 2) / (2 * vector_a * vector_b)
    print(cnt, "cosθ", cos_theta)
    # 角度を求める
    global theta
    theta = math.degrees(math.acos(cos_theta))
    print(cnt, "角度", theta)

# 四角形分割プログラム
# L点を抽出する．凹角の角度制限を確認する．
# Ｎ角形　内角数：N=2x,x=N/2，凹角数：L=x-2=N/2-2
L_cnt = angles / 2 - 2
order = {}  # 頂点データの並び順を格納する
L_num = 1
R_num = 1

for i in range(angles):

    # 外積を求めてL点かどうか判断する
    ccwChk(i)
    if (S > 0): # L点の場合の処理
        # 内積から角度を求める
        innerProduct(i)
        naikaku = 360 - theta
        print(naikaku)
        # 凹角の角度制限
        if (naikaku > 280 or naikaku < 260):
            break
            break   #子ループから抜けて親ループから抜ける為のbreak
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
