import sys
import os
import json
import itertools
import math
from numpy.ma import copy
import sympy as sp

from PyQt5.QtWidgets import *
from pathlib import Path

from SteraPyDialog import *


def f_build_start():

    # リストの要素から値を取得する
    def f_ext_elem(ftr):
        # ftr = data
        prop = ftr.get('properties')
        global val_id
        val_id = prop.get('id')
        print('id', val_id)
        # val_fid = prop.get('fid')
        # kind = prop.get('種別')
        # global name
        name = prop.get('名称')
        print('名称', name)
        global elevation
        elevation = prop.get('median標高')
        print('標高', elevation)
        geom = ftr.get('geometry')
        # 平面直角座標系のX軸は真北に向かう値が正，Y軸は真東に向かう値が正
        cords = geom.get('coordinates')
        global cord2
        cord2 = list(itertools.chain.from_iterable(cords))
        print("cord2", cord2)

    # 閉じた図形かどうかチェックする
    def f_chk_close(apex):
        if (cord2[0][0] == cord2[apex - 1][0]) and (cord2[0][1] == cord2[apex - 1][1]):
            global nodes
            nodes = apex - 1

    # 頂点間の距離をチェックする，近接する頂点を削除する
    def f_chk_vert_dist(tops):
        del_nodes_lst = []
        global new_nodes
        new_nodes = 0
        for j in range(tops):
            # 次の頂点までの距離を求める
            if j != (tops - 1):
                # ベクトルAのX座標の差分
                chk_vect_x = cord2[j + 1][0] - cord2[j][0]
                # ベクトルAのY座標の差分
                chk_vect_y = cord2[j + 1][1] - cord2[j][1]
                print(j, "ベクトルX", chk_vect_x)
                print(j, "ベクトルY", chk_vect_y)
            else:
                chk_vect_x = cord2[0][0] - cord2[j][0]
                chk_vect_y = cord2[0][1] - cord2[j][1]
                print(j, "ベクトルX", chk_vect_x)
                print(j, "ベクトルY", chk_vect_y)
            if abs(chk_vect_x) < 1.0 and abs(chk_vect_y) < 1.0:
                del_nodes_lst.append(j + 1)
        print('削除するノード', del_nodes_lst)

        del_cnt = len(del_nodes_lst)
        if del_cnt != 0:
            in_cnt = 0
            for lst in range(del_cnt):
                # print(del_nodes_lst[lst])
                cord2.pop(del_nodes_lst[lst] - in_cnt)
                in_cnt += 1
            new_nodes = nodes - del_cnt
            for j in range(new_nodes):
                print(j, 'X', cord2[j][0])
                print(j, 'Y', cord2[j][1])
        # Date210830 コーディングの目的が不明なためコメント化した．
        if new_nodes == 0:
            new_nodes = tops
        print('new_nodes=', new_nodes)

    # 頂点数が奇数の場合，最大鈍角の頂点を削除する
    def f_flat_vert(chk_nodes):
        # 内積を求めて３点からなら角度を求める，
        max_deg = 0
        del_codes = 0
        for j in range(chk_nodes):
            # 隣合う点との間の距離から辺の長さを求める
            if j != (chk_nodes - 1):
                # ベクトルAのX座標の差分
                vect_ax = cord2[j + 1][1] - cord2[j][1]
                # ベクトルAのY座標の差分
                vect_ay = cord2[j + 1][0] - cord2[j][0]
                # ベクトルAの長さ
                vector_a = math.sqrt(vect_ax ** 2 + vect_ay ** 2)
                print(j, "ベクトルAx", vect_ax)
                print(j, "ベクトルAy", vect_ay)
                print(j, "ベクトルA", vector_a)
            else:
                vect_ax = cord2[0][1] - cord2[j][1]
                vect_ay = cord2[0][0] - cord2[j][0]
                vector_a = math.sqrt(vect_ax ** 2 + vect_ay ** 2)
                print(j, "ベクトルAx", vect_ax)
                print(j, "ベクトルAy", vect_ay)
                print(j, "ベクトルA", vector_a)
            if j != 0:
                # ベクトルBのX座標の差分
                vect_bx = cord2[j - 1][1] - cord2[j][1]
                # ベクトルBのY座標の差分
                vect_by = cord2[j - 1][0] - cord2[j][0]
                # ベクトルBの長さ
                vector_b = math.sqrt(vect_bx ** 2 + vect_by ** 2)
                print(j, "ベクトルBx", vect_bx)
                print(j, "ベクトルBy", vect_by)
                print(j, "ベクトルB", vector_b)
            else:
                vect_bx = cord2[chk_nodes - 1][1] - cord2[0][1]
                vect_by = cord2[chk_nodes - 1][0] - cord2[0][0]
                vector_b = math.sqrt(vect_bx ** 2 + vect_by ** 2)
                print(j, "ベクトルBx", vect_bx)
                print(j, "ベクトルBy", vect_by)
                print(j, "ベクトルB", vector_b)
            # cosθを求める
            cos_theta = (vect_ax * vect_bx + vect_ay * vect_by) / (vector_a * vector_b)
            print(j, "cosθ", cos_theta)
            # 角度を求める
            obt_angle = math.degrees(math.acos(cos_theta))
            print(j, "角度", obt_angle)
            # 最大鈍角（175°～185°）の頂点を削除する
            if obt_angle > max_deg:
                max_deg = obt_angle
                del_codes = j
        print('max_deg=', max_deg)
        if 175 < max_deg < 185:
            print('削除するノード', del_codes)
            cord2.pop(del_codes)
            chk_nodes -= 1
        print('chk_nodes=', chk_nodes)
        for j in range(chk_nodes):
            print(j, 'X', cord2[j][1])
            print(j, 'Y', cord2[j][0])
        global ret_nodes
        ret_nodes = chk_nodes
        return ret_nodes

    # 外積を求めてL点かどうか判断する
    def f_ccw_check(ccw_nodes):
        global LH
        LH = 0  # 左回り（反時計回り）
        global RH
        RH = 0  # 右回り（時計回り）
        global S
        S = []
        global in_angle
        in_angle = [0.0] * ccw_nodes
        # 外積を計算する
        for j in range(ccw_nodes):
            xs = cord2[j][1]
            ys = cord2[j][0]
            if j == 0:
                xp = cord2[ccw_nodes - 1][1]
                yp = cord2[ccw_nodes - 1][0]
                xn = cord2[j + 1][1]
                yn = cord2[j + 1][0]
            elif j == ccw_nodes - 1:
                xp = cord2[j - 1][1]
                yp = cord2[j - 1][0]
                xn = cord2[0][1]
                yn = cord2[0][0]
            else:
                xp = cord2[j - 1][1]
                yp = cord2[j - 1][0]
                xn = cord2[j + 1][1]
                yn = cord2[j + 1][0]
            s = (xp - xs) * (yn - ys) - (xn - xs) * (yp - ys)
            S.append(s)
            print("S[j]=", S[j])
            # 外積の結果で左回りか右回りか判断する
            if S[j] > 0:  # 左回り
                LH += 1
                # L点の場合は，角度が約270°かチェックする（内積計算）
                # 内角計算->凹角　約270°でない場合は四角形分割を中断
                f_inner_product(j)
                naikaku = 360 - theta
                print('内角=', naikaku)
                in_angle[j] = naikaku

            elif S[j] < 0:  # 右回り
                RH += 1
        print(in_angle)

    # 内積を求めて３点からなら角度を求める，
    def f_inner_product(cnt):
        print(cnt)
        # 隣合う点との間の距離から辺の長さを求める
        if cnt != 0:  # 最初の頂点でない時
            # ベクトルAのX座標の差分
            vect_ax = cord2[cnt - 1][1] - cord2[cnt][1]
            # ベクトルAのY座標の差分
            vect_ay = cord2[cnt - 1][0] - cord2[cnt][0]
            # ベクトルAの長さ
            vector_a = math.sqrt(vect_ax ** 2 + vect_ay ** 2)
            print(cnt, "ベクトルAx", vect_ax)
            print(cnt, "ベクトルAy", vect_ay)
            print(cnt, "ベクトルA", vector_a)
        else:  # cnt == 0
            vect_ax = cord2[new_nodes - 1][1] - cord2[0][1]
            vect_ay = cord2[new_nodes - 1][0] - cord2[0][0]
            vector_a = math.sqrt(vect_ax ** 2 + vect_ay ** 2)
            print(cnt, "ベクトルAx", vect_ax)
            print(cnt, "ベクトルAy", vect_ay)
            print(cnt, "ベクトルA", vector_a)
        if cnt != (new_nodes - 1):  # 最後の頂点でない時
            # ベクトルBのX座標の差分
            vect_bx = cord2[cnt + 1][1] - cord2[cnt][1]
            # ベクトルBのY座標の差分
            vect_by = cord2[cnt + 1][0] - cord2[cnt][0]
            # ベクトルBの長さ
            vector_b = math.sqrt(vect_bx ** 2 + vect_by ** 2)
            print(cnt, "ベクトルBx", vect_bx)
            print(cnt, "ベクトルBy", vect_by)
            print(cnt, "ベクトルB", vector_b)
        else:
            vect_bx = cord2[0][1] - cord2[cnt][1]
            vect_by = cord2[0][0] - cord2[cnt][0]
            vector_b = math.sqrt(vect_bx ** 2 + vect_by ** 2)
            print(cnt, "ベクトルBx", vect_bx)
            print(cnt, "ベクトルBy", vect_by)
            print(cnt, "ベクトルB", vector_b)
        # 角度を求める
        f_cross_angle(vect_ax, vect_ay, vect_bx, vect_by, vector_a, vector_b)
        print(cnt, "角度", theta)

    # ベクトルの交差角度を求める
    def f_cross_angle(ax, ay, bx, by, al, bl):
        # cosθを求める
        taihen = math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)
        # 余弦定理　第二余弦定理を変形した公式を使えば、辺の長さから余弦を求めることができる。
        cos_theta = (al ** 2 + bl ** 2 - taihen ** 2) / (2 * al * bl)
        print("cosθ", cos_theta)
        # 角度を求める
        global theta
        theta = math.degrees(math.acos(cos_theta))
        # print("角度", theta)

    # 頂点の並びが時計回りなので反時計回りに並び変える
    def f_back_reverse(rev_nodes):
        rev_codes = copy.deepcopy(cord2)
        for j in range(rev_nodes - 1, 0):
            rev_codes[j][1] = cord2[j][1]
            rev_codes[j][0] = cord2[j][0]
        for j in range(1, rev_nodes):
            cord2[j][1] = rev_codes[j][1]
            cord2[j][0] = rev_codes[j][0]
        for j in range(rev_nodes):
            print(j, 'X', cord2[j][1])
            print(j, 'Y', cord2[j][0])

    # 2点を通る直線の方程式
    def f_make_line(x1, y1, x2, y2):
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

    # ベクトルの長さを求める
    def f_vector_length(x1, y1, x0, y0):
        global vect_x
        vect_x = x1 - x0
        # ベクトルAのY座標の差分
        global vect_y
        vect_y = y1 - y0
        # ベクトルAの長さ
        global vector
        vector = math.sqrt(vect_x ** 2 + vect_y ** 2)
        # return vect_x
        # return vect_y
        print("ベクトルx", vect_x)
        print("ベクトルy", vect_y)
        print("ベクトル", vector)

    # 2直線の交点を求める
    def f_inter_sect(a1, b1, a2, b2):
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
        return ans  # {x: 20, y: 1400}が返ってくる

    # L点を含む直線と対抗する辺との交差角度を求める
    def f_chokuko_check(choku_cords, taiko_cords):
        # 直交する辺の両端座標（一方がL点）
        x1 = choku_cords[0][1]
        y1 = choku_cords[0][0]
        x2 = choku_cords[1][1]
        y2 = choku_cords[1][0]
        # 直交する直線の方程式
        line_1 = f_make_line(x1, y1, x2, y2)
        print(line_1)
        m1 = line_1['m']
        n1 = line_1['n']
        # 対向する辺の両端座標
        x1 = taiko_cords[0][1]
        y1 = taiko_cords[0][0]
        x2 = taiko_cords[1][1]
        y2 = taiko_cords[1][0]
        # 対向する直線の方程式
        line_2 = f_make_line(x1, y1, x2, y2)
        print(line_2)
        m2 = line_2['m']
        n2 = line_2['n']

        # ２直線の交点を求める
        f_inter_sect(m1, n1, m2, n2)
        print(ans)
        global int_x
        int_x = ans[x]
        global int_y
        int_y = ans[y]

        # 内積を計算して交差する角度を求める
        # ベクトルA　交点とL1点を結ぶベクトル
        f_vector_length(choku_cords[0][1], choku_cords[0][0], int_x, int_y)
        vect_ax = vect_x
        vect_ay = vect_y
        vector_a = vector
        # ベクトルB　交点と３つ目の点を結ぶベクトル
        f_vector_length(taiko_cords[0][1], taiko_cords[0][0], int_x, int_y)
        vect_bx = vect_x
        vect_by = vect_y
        vector_b = vector

        # ベクトルの交差角度
        f_cross_angle(vect_ax, vect_ay, vect_bx, vect_by, vector_a, vector_b)
        # 角度を求める
        print("角度", theta)

    # L点とR点をリストおよび辞書に振り分ける
    def gene_lr_listdic(nodes):
        global l_num
        l_num = 1
        global r_num
        r_num = 1
        for i in range(nodes):
            if S[i] > 0:  # L点の場合の処理
                l_list.append(cord2[i])
                order["L" + str(l_num)] = i
                l_num += 1
            else:  # R点の場合の処理
                if not l_list:
                    r_suslist.append(cord2[i])
                else:
                    r_list.append(cord2[i])
                    order["R" + str(r_num)] = i
                    r_num += 1

        r_list.extend(r_suslist)
        sus_len = len(r_suslist)
        for j in range(sus_len):
            order["R" + str(r_num)] = j
            r_num += 1
        print(l_list)
        print(r_list)
        print(r_suslist)
        print(order)

        # L-R並びで型分けする
        global arr_lr_p
        arr_lr_p = []
        for LR_key in order:
            ini = LR_key[0]
            arr_lr_p.append(ini)
        print(arr_lr_p)

    # 6角形を2つに四角形分割する
    def hexagonal_divider(cords):
        # L点の直交条件．対向する辺との交点の角度制限を確認する．
        for LR_key in order:
            if LR_key == 'L1':
                print(LR_key)
                num = order[LR_key]
                # print(num)

                # 直交する辺は．L点と1つ前の点で結ばれる線分
                # 直交する辺の座標ペア
                if num == 0:
                    choku_cords_1 = [cords[num], cords[new_nodes - 1]]
                else:
                    choku_cords_1 = [cords[num], cords[num - 1]]

                # 対向する辺は，L点から２つ目と３つ目の点で結ばれる線分
                # 対向する辺の座標ペア
                # hen_coprds = [[] for _ in range(hen_cnt)]
                taiko_cords_1 = []
                if (num + 2) > (new_nodes - 1):
                    taiko_cords_1.append(cords[num + 2 - new_nodes])
                else:
                    taiko_cords_1.append(cords[num + 2])
                if (num + 3) > (new_nodes - 1):
                    taiko_cords_1.append(cords[num + 3 - new_nodes])
                else:
                    taiko_cords_1.append(cords[num + 3])

                print("choku_cords_1", choku_cords_1)
                print("taiko_cords_1", taiko_cords_1)

                # 直交する直線aと対向する辺との直交条件を確認する
                f_chokuko_check(choku_cords_1, taiko_cords_1)
                int_1st_x = int_x
                int_1st_y = int_y

                # 交差角度が制限範囲内でない場合は処理を中断する
                if theta < 60 or theta > 120:
                    continue
                    # 折れ曲がりの切妻屋根
                    # tsuma_line =
                    # yane_type =
                    # f_bent_gable_roof(order, tsuma_line, yane_type)

                # もう一方の直交する辺は．L点と1つ次の点で結ばれる線分
                # 直交する辺の座標ペア
                if num == (new_nodes - 1):
                    choku_cords_2 = [cords[num], cords[0]]
                else:
                    choku_cords_2 = [cords[num], cords[num + 1]]

                # もう一方の対向する辺は，L点から３つ目と４つ目の点で結ばれる線分
                # 対向する辺の座標ペア
                taiko_cords_2 = []
                if (num + 3) > (new_nodes - 1):
                    taiko_cords_2.append(cords[num + 3 - new_nodes])
                else:
                    taiko_cords_2.append(cords[num + 3])
                if (num + 4) > (new_nodes - 1):
                    taiko_cords_2.append(cords[num + 3 - new_nodes + 1])
                else:
                    taiko_cords_2.append(cords[num + 4])

                print("choku_cords_2", choku_cords_2)
                print("taiko_cords_2", taiko_cords_2)

                # 直交する直線bと対向する辺との直交条件を確認する
                f_chokuko_check(choku_cords_2, taiko_cords_2)
                int_2nd_x = int_x
                int_2nd_y = int_y

                # 交差角度が制限範囲内でない場合は処理を中断する
                if theta < 60 or theta > 120:
                    continue
                    # 折れ曲がりの切妻屋根
                    # tsuma_line =
                    # yane_type =
                    # f_bent_gable_roof(order, tsuma_line, yane_type)
            else:
                continue
            print("normal termination")
        print("All finished")

        # L点から対向する二辺までの距離を比較する
        # L点の座標
        print(cords[num][1])
        print(cords[num][0])
        # 交点１の座標
        # print(int_1st_x)
        # print(int_1st_y)
        # 交点１までの距離
        div_line_a = math.sqrt((cords[num][1] - int_1st_x) ** 2 + (cords[num][0] - int_1st_y) ** 2)
        print("div_line_a=", div_line_a)
        # 交点２の座標
        # print(int_2nd_x)
        # print(int_2nd_y)
        # 交点２までの距離
        div_line_b = math.sqrt((cords[num][1] - int_2nd_x) ** 2 + (cords[num][0] - int_2nd_y) ** 2)
        print("div_line_b=", div_line_b)

        # 距離の短い方の線分を分割線とする
        if div_line_a < div_line_b:
            print("分割線はdiv_line_a")
            # 分割点はD1点（交点１）
            d1 = [int_1st_y, int_1st_x]
            # 座標値のリストにD1点の座標値を追加する
            cords.extend([d1])
            print(cords)
            # 頂点並びの辞書に分割点を追加する
            d1_num = new_nodes + 1
            order['D1'] = d1_num
            print('line_a', order)

            # 四角形D1-R1-R2-R3
            rect_1_name = ['D1', 'R1', 'R2', 'R3']
            # 四角形L1-D1-R4-R5
            rect_2_name = ['L1', 'D1', 'R4', 'R5']

        elif div_line_a > div_line_b:
            print("分割線はdiv_line_b")
            # 分割点はD2点（交点２）
            d2 = [int_2nd_y, int_2nd_x]
            # 座標値のリストにD2点の座標値を追加する
            cords.extend([d2])
            print(cords)
            # 頂点並びの辞書に分割点を追加する
            d2_num = new_nodes + 1
            order['D2'] = d2_num
            print('line_b', order)

            # 四角形L1-R1-R2-D2
            rect_1_name = ['L1', 'R1', 'R2', 'D2']
            # 四角形D2-R3-R4-R5
            rect_2_name = ['D2', 'R3', 'R4', 'R5']

        # 辞書の中味に従ってリストの座標データで四角形を作る
        rect_1_list = []
        for name in rect_1_name:
            n = order[name]
            rect_1_list.append(cords[n])
            # tsuma_line =
            # yane_type =
            # f_make_roof(rect_1_list, tsuma_line, yane_type)
        print(rect_1_list)

        # 辞書の中味に従ってリストの座標データで四角形を作る
        rect_2_list = []
        for name in rect_2_name:
            n = order[name]
            rect_2_list.append(cords[n])
            # tsuma_line =
            # yane_type =
            # f_make_roof(rect_2_list, tsuma_line, yane_type)
        print(rect_2_list)

    # 8角形を３つの四角形に分割する
    def octagonal_divider(cords):
        # L-R並びで型分けする
        if arr_lr_p == ['L', 'R', 'L', 'R', 'R', 'R', 'R', 'R']:
            oct_type = '歯型1'
            num1 = order['L1']
            # 直交する辺は．L点と1つ前の点で結ばれる線分
            # 直交する辺の座標ペア
            if num1 == 0:
                choku_cords_1 = [cords[num1], cords[new_nodes - 1]]
            else:
                choku_cords_1 = [cords[num1], cords[num1 - 1]]
            # 対向する辺は，L点から５つ目と６つ目の点で結ばれる線分
            # 対向する辺の座標ペア
            # hen_coprds = [[] for _ in range(hen_cnt)]
            taiko_cords_1 = []
            if (num1 + 5) > (new_nodes - 1):
                taiko_cords_1.append(cords[num1 + 5 - new_nodes])
            else:
                taiko_cords_1.append(cords[num1 + 5])
            if (num1 + 6) > (new_nodes - 1):
                taiko_cords_1.append(cords[num1 + 6 - new_nodes])
            else:
                taiko_cords_1.append(cords[num1 + 6])
            # 直交する直線aと対向する辺との直交条件を確認する
            f_chokuko_check(choku_cords_1, taiko_cords_1)
            int_1st_x = int_x
            int_1st_y = int_y
            # 交差角度が制限範囲内でない場合は処理を中断する
            # if theta < 60 or theta > 120:
            #     continue
                # f_tri_mesh(cord2)

            num2 = order['L2']
            # もう一本の直交する辺は．L点と1つ次の点で結ばれる線分
            # 直交する辺の座標ペア
            if num2 == (new_nodes - 1):
                choku_cords_2 = [cords[num2], cords[0]]
            else:
                choku_cords_2 = [cords[num2], cords[num2 + 1]]
            # 対向する辺は，L点から２つ目と３つ目の点で結ばれる線分
            # 対向する辺の座標ペア
            # hen_coprds = [[] for _ in range(hen_cnt)]
            taiko_cords_2 = []
            if (num2 + 2) > (new_nodes - 1):
                taiko_cords_2.append(cords[num2 + 2 - new_nodes])
            else:
                taiko_cords_2.append(cords[num2 + 2])
            if (num2 + 3) > (new_nodes - 1):
                taiko_cords_2.append(cords[num2 + 3 - new_nodes])
            else:
                taiko_cords_2.append(cords[num2 + 3])
            # 直交する直線bと対向する辺との直交条件を確認する
            f_chokuko_check(choku_cords_2, taiko_cords_2)
            int_2nd_x = int_x
            int_2nd_y = int_y
            # 交差角度が制限範囲内でない場合は処理を中断する
            # if theta < 60 or theta > 120:
            #     continue
            # f_tri_mesh(cord2)

            # 分割点はD1点（交点１）
            d1 = [int_1st_y, int_1st_x]
            # 座標値のリストにD1点の座標値を追加する
            cords.extend([d1])
            # 分割点はD2点（交点２）
            d2 = [int_2nd_y, int_2nd_x]
            # 座標値のリストにD2点の座標値を追加する
            cords.extend([d2])
            print(cords)
            # 頂点並びの辞書に分割点を追加する
            d1_num = new_nodes + 1
            order['D1'] = d1_num
            d2_num = new_nodes + 2
            order['D2'] = d2_num
            print(order)

            # 四角形L1-D1-R5-R6
            rect_1_name = ['L1', 'D1', 'R5', 'R6']
            # 四角形L2-R2-R3-D2
            rect_2_name = ['L2', 'R2', 'R3', 'D2']
            # 四角形R1-D2-R4-D1
            rect_3_name = ['R1', 'D2', 'R4', 'D1']

            # 辞書の中味に従ってリストの座標データで四角形を作る
            rect_1_list = []
            for name in rect_1_name:
                n = order[name]
                rect_1_list.append(cords[n])
                # tsuma_line =
                # yane_type =
                # f_make_roof(rect_1_list, tsuma_line, yane_type)
            print(rect_1_list)
            # 辞書の中味に従ってリストの座標データで四角形を作る
            rect_2_list = []
            for name in rect_2_name:
                n = order[name]
                rect_2_list.append(cords[n])
                # tsuma_line =
                # yane_type =
                # f_make_roof(rect_2_list, tsuma_line, yane_type)
            print(rect_2_list)
            # 辞書の中味に従ってリストの座標データで四角形を作る
            rect_3_list = []
            for name in rect_3_name:
                n = order[name]
                rect_3_list.append(cords[n])
                # tsuma_line =
                # yane_type =
                # f_make_roof(rect_3_list, tsuma_line, yane_type)
            print(rect_3_list)

        elif arr_lr_p == ['L', 'R', 'R', 'R', 'R', 'R', 'L', 'R']:
            oct_type = '歯型2'
            num1 = order['L1']
            # 直交する辺は．L点と1つ前の点で結ばれる線分
            # 直交する辺の座標ペア
            if num1 == 0:
                choku_cords_1 = [cords[num1], cords[new_nodes - 1]]
            else:
                choku_cords_1 = [cords[num1], cords[num1 - 1]]
            # 対向する辺は，L点から２つ目と３つ目の点で結ばれる線分
            # 対向する辺の座標ペア
            taiko_cords_1 = []
            if (num1 + 2) > (new_nodes - 1):
                taiko_cords_1.append(cords[num1 + 2 - new_nodes])
            else:
                taiko_cords_1.append(cords[num1 + 2])
            if (num1 + 3) > (new_nodes - 1):
                taiko_cords_1.append(cords[num1 + 3 - new_nodes])
            else:
                taiko_cords_1.append(cords[num1 + 3])
            # 直交する直線aと対向する辺との直交条件を確認する
            f_chokuko_check(choku_cords_1, taiko_cords_1)
            int_1st_x = int_x
            int_1st_y = int_y
            # 交差角度が制限範囲内でない場合は処理を中断する
            # if theta < 60 or theta > 120:
            #     continue
                # f_tri_mesh(cord2)

            num2 = order['L2']
            # もう一本の直交する辺は．L点と1つ次の点で結ばれる線分
            # 直交する辺の座標ペア
            if num2 == (new_nodes - 1):
                choku_cords_2 = [cords[num2], cords[0]]
            else:
                choku_cords_2 = [cords[num2], cords[num2 + 1]]
            # 対向する辺は，L点から５つ目と６つ目の点で結ばれる線分
            # 対向する辺の座標ペア
            # hen_coprds = [[] for _ in range(hen_cnt)]
            taiko_cords_2 = []
            if (num2 + 5) > (new_nodes - 1):
                taiko_cords_2.append(cords[num2 + 5 - new_nodes])
            else:
                taiko_cords_2.append(cords[num2 + 5])
            if (num2 + 6) > (new_nodes - 1):
                taiko_cords_2.append(cords[num2 + 6 - new_nodes])
            else:
                taiko_cords_2.append(cords[num2 + 6])
            # 直交する直線bと対向する辺との直交条件を確認する
            f_chokuko_check(choku_cords_2, taiko_cords_2)
            int_2nd_x = int_x
            int_2nd_y = int_y
            # 交差角度が制限範囲内でない場合は処理を中断する
            # if theta < 60 or theta > 120:
            #     continue
            # f_tri_mesh(cord2)

            # 分割点はD1点（交点１）
            d1 = [int_1st_y, int_1st_x]
            # 座標値のリストにD1点の座標値を追加する
            cords.extend([d1])
            # 分割点はD2点（交点２）
            d2 = [int_2nd_y, int_2nd_x]
            # 座標値のリストにD2点の座標値を追加する
            cords.extend([d2])
            print(cords)
            # 頂点並びの辞書に分割点を追加する
            d1_num = new_nodes + 1
            order['D1'] = d1_num
            d2_num = new_nodes + 2
            order['D2'] = d2_num
            print(order)

            # 四角形L1-D1-R5-R6
            rect_1_name = ['L2', 'D2', 'R4', 'R5']
            # 四角形L2-R2-R3-D2
            rect_2_name = ['L1', 'R1', 'R2', 'D1']
            # 四角形R1-D2-R4-D1
            rect_3_name = ['R6', 'D1', 'R3', 'D2']

            # 辞書の中味に従ってリストの座標データで四角形を作る
            rect_1_list = []
            for name in rect_1_name:
                n = order[name]
                rect_1_list.append(cords[n])
                # tsuma_line =
                # yane_type =
                # f_make_roof(rect_1_list, tsuma_line, yane_type)
            print(rect_1_list)
            # 辞書の中味に従ってリストの座標データで四角形を作る
            rect_2_list = []
            for name in rect_2_name:
                n = order[name]
                rect_2_list.append(cords[n])
                # tsuma_line =
                # yane_type =
                # f_make_roof(rect_2_list, tsuma_line, yane_type)
            print(rect_2_list)
            # 辞書の中味に従ってリストの座標データで四角形を作る
            rect_3_list = []
            for name in rect_3_name:
                n = order[name]
                rect_3_list.append(cords[n])
                # tsuma_line =
                # yane_type =
                # f_make_roof(rect_3_list, tsuma_line, yane_type)
            print(rect_3_list)

        elif arr_lr_p == ['L', 'L', 'R', 'R', 'R', 'R', 'R', 'R']:
            oct_type = '凹型1'
            num1 = order['L1']
            # １つ目の直交する辺は．L点と1つ前の点で結ばれる線分
            # 直交する辺の座標ペア
            if num1 == 0:
                choku_cords_1a = [cords[num1], cords[new_nodes - 1]]
            else:
                choku_cords_1a = [cords[num1], cords[num1 - 1]]
            # 対向する辺は，L点から４つ目と５つ目の点で結ばれる線分
            # 対向する辺の座標ペア
            taiko_cords_1a = []
            if (num1 + 4) > (new_nodes - 1):
                taiko_cords_1a.append(cords[num1 + 4 - new_nodes])
            else:
                taiko_cords_1a.append(cords[num1 + 4])
            if (num1 + 5) > (new_nodes - 1):
                taiko_cords_1a.append(cords[num1 + 5 - new_nodes])
            else:
                taiko_cords_1a.append(cords[num1 + 5])
            # 直交する直線1aと対向する辺との直交条件を確認する
            f_chokuko_check(choku_cords_1a, taiko_cords_1a)
            int_1a_x = int_x
            int_1a_y = int_y
            # 交差角度が制限範囲内でない場合は処理を中断する
            # if theta < 60 or theta > 120:
            #     continue
                # f_tri_mesh(cord2)
            # もう一方の直交する辺は．L点と次の点で結ばれる線分
            # 直交する辺の座標ペア
            if num1 == (new_nodes - 1):
                choku_cords_1b = [cords[num1], cords[0]]
            else:
                choku_cords_1b = [cords[num1], cords[num1 + 1]]
            # 対向する辺は，L点から５つ目と６つ目の点で結ばれる線分
            # 対向する辺の座標ペア
            taiko_cords_1b = []
            if (num1 + 5) > (new_nodes - 1):
                taiko_cords_1b.append(cords[num1 + 5 - new_nodes])
            else:
                taiko_cords_1b.append(cords[num1 + 5])
            if (num1 + 6) > (new_nodes - 1):
                taiko_cords_1b.append(cords[num1 + 6 - new_nodes])
            else:
                taiko_cords_1b.append(cords[num1 + 6])
            # 直交する直線1bと対向する辺との直交条件を確認する
            f_chokuko_check(choku_cords_1b, taiko_cords_1b)
            int_1b_x = int_x
            int_1b_y = int_y
            # 交差角度が制限範囲内でない場合は処理を中断する
            # if theta < 60 or theta > 120:
            #     continue
            # f_tri_mesh(cord2)

            num2 = order['L2']
            # ２つ目の直交する辺は．L点と1つ前の点で結ばれる線分
            # 直交する辺の座標ペア
            if num2 == 0:
                choku_cords_2a = [cords[num2], cords[new_nodes - 1]]
            else:
                choku_cords_2a = [cords[num2], cords[num2 - 1]]
            # 対向する辺は，L点から２つ目と３つ目の点で結ばれる線分
            # 対向する辺の座標ペア
            taiko_cords_2a = []
            if (num2 + 2) > (new_nodes - 1):
                taiko_cords_2a.append(cords[num2 + 2 - new_nodes])
            else:
                taiko_cords_2a.append(cords[num2 + 2])
            if (num2 + 3) > (new_nodes - 1):
                taiko_cords_2a.append(cords[num2 + 3 - new_nodes])
            else:
                taiko_cords_2a.append(cords[num2 + 3])
            # 直交する直線2aと対向する辺との直交条件を確認する
            f_chokuko_check(choku_cords_2a, taiko_cords_2a)
            int_2a_x = int_x
            int_2a_y = int_y
            # 交差角度が制限範囲内でない場合は処理を中断する
            # if theta < 60 or theta > 120:
            #     continue
            # f_tri_mesh(cord2)
            # もう一方の直交する辺は．L点と次の点で結ばれる線分
            # 直交する辺の座標ペア
            if num1 == (new_nodes - 1):
                choku_cords_2b = [cords[num1], cords[0]]
            else:
                choku_cords_2b = [cords[num1], cords[num1 + 1]]
            # 対向する辺は，L点から３つ目と４つ目の点で結ばれる線分
            # 対向する辺の座標ペア
            taiko_cords_2b = []
            if (num1 + 5) > (new_nodes - 1):
                taiko_cords_2b.append(cords[num1 + 5 - new_nodes])
            else:
                taiko_cords_2b.append(cords[num1 + 5])
            if (num1 + 6) > (new_nodes - 1):
                taiko_cords_2b.append(cords[num1 + 6 - new_nodes])
            else:
                taiko_cords_2b.append(cords[num1 + 6])
            # 直交する直線1bと対向する辺との直交条件を確認する
            f_chokuko_check(choku_cords_2b, taiko_cords_2b)
            int_2b_x = int_x
            int_2b_y = int_y
            # 交差角度が制限範囲内でない場合は処理を中断する
            # if theta < 60 or theta > 120:
            #     continue
            # f_tri_mesh(cord2)

            # L点から対向する二辺までの距離を比較する
            # L1点の座標
            print(cords[num1][1])
            print(cords[num1][0])
            # 交点1aの座標
            # print(int_1a_x)
            # print(int_1a_y)
            # 交点1aまでの距離
            div_line_1a = math.sqrt((cords[num1][1] - int_1a_x) ** 2 + (cords[num1][0] - int_1a_y) ** 2)
            print("div_line_a=", div_line_1a)
            # 交点1bの座標
            # print(int_1b_x)
            # print(int_1b_y)
            # 交点1bまでの距離
            div_line_1b = math.sqrt((cords[num1][1] - int_1b_x) ** 2 + (cords[num1][0] - int_1b_y) ** 2)
            print("div_line_b=", div_line_1b)
            # L2点の座標
            print(cords[num2][1])
            print(cords[num2][0])
            # 交点2aの座標
            # print(int_2a_x)
            # print(int_2a_y)
            # 交点2aまでの距離
            div_line_2a = math.sqrt((cords[num2][1] - int_2a_x) ** 2 + (cords[num2][0] - int_2a_y) ** 2)
            print("div_line_a=", div_line_2a)
            # 交点2bの座標
            # print(int_2b_x)
            # print(int_2b_y)
            # 交点2bまでの距離
            div_line_2b = math.sqrt((cords[num2][1] - int_2b_x) ** 2 + (cords[num2][0] - int_2b_y) ** 2)
            print("div_line_b=", div_line_2b)

            # 距離の短い方の線分を分割線とする
            if div_line_1a < div_line_1b:
                print("分割線はdiv_line_a")
                # 分割点はD1a点（交点１）
                d1 = [int_1a_y, int_1a_x]
                # 座標値のリストにD1点の座標値を追加する
                cords.extend([d1])
                print(cords)
                # 頂点並びの辞書に分割点を追加する
                d1_num = new_nodes + 1
                order['D1'] = d1_num
                print('line_a', order)

                # 四角形D1-R4-R5-R6
                rect_1_name = ['D1', 'R4', 'R5', 'R6']

                # 距離の短い方の線分を分割線とする
                if div_line_2a < div_line_2b:
                    print("分割線はdiv_line_a")
                    # 分割点はD1a点（交点１）
                    d2 = [int_2a_y, int_2a_x]
                    # 座標値のリストにD1点の座標値を追加する
                    cords.extend([d2])
                    print(cords)
                    # 頂点並びの辞書に分割点を追加する
                    d2_num = new_nodes + 2
                    order['D2'] = d2_num
                    print('line_a', order)

                    # 四角形L1-D2-R3-D1
                    rect_2_name = ['L1', 'D2', 'R3', 'D1']
                    # 四角形R1-R2-D2-L2
                    rect_3_name = ['R1', 'R2', 'D2', 'L2']

                elif div_line_2a > div_line_2b:
                    print("分割線はdiv_line_b")
                    # 分割点はD1b点（交点１）
                    d2 = [int_2b_y, int_2b_x]
                    # 座標値のリストにD1点の座標値を追加する
                    cords.extend([d2])
                    print(cords)
                    # 頂点並びの辞書に分割点を追加する
                    d2_num = new_nodes + 2
                    order['D2'] = d2_num
                    print('line_b', order)

                    # 四角形L1-L2-D2-D1
                    rect_2_name = ['L1', 'L2', 'D2', 'D1']
                    # 四角形R1-R2-R3-D2
                    rect_3_name = ['R1', 'R2', 'R3', 'D2']

            elif div_line_1a > div_line_1b:
                print("分割線はdiv_line_b")
                # 分割点はD1b点（交点１）
                d1 = [int_1b_y, int_1b_x]
                # 座標値のリストにD1点の座標値を追加する
                cords.extend([d1])
                print(cords)
                # 頂点並びの辞書に分割点を追加する
                d1_num = new_nodes + 1
                order['D1'] = d1_num
                print('line_b', order)

                # 四角形L1-D1-R5-R6
                rect_1_name = ['L1', 'D1', 'R5', 'R6']

                # 距離の短い方の線分を分割線とする
                if div_line_2a < div_line_2b:
                    print("分割線はdiv_line_a")
                    # 分割点はD1a点（交点１）
                    d2 = [int_2a_y, int_2a_x]
                    # 座標値のリストにD1点の座標値を追加する
                    cords.extend([d2])
                    print(cords)
                    # 頂点並びの辞書に分割点を追加する
                    d2_num = new_nodes + 2
                    order['D2'] = d2_num
                    print('line_a', order)

                    # 四角形L2-D2-R4-D1
                    rect_2_name = ['L2', 'D2', 'R4', 'D1']
                    # 四角形R1-R2-R3-D2
                    rect_3_name = ['R1', 'R2', 'R3', 'D2']

                elif div_line_2a > div_line_2b:
                    print("分割線はdiv_line_b")
                    # 分割点はD1b点（交点１）
                    d2 = [int_2b_y, int_2b_x]
                    # 座標値のリストにD1点の座標値を追加する
                    cords.extend([d2])
                    print(cords)
                    # 頂点並びの辞書に分割点を追加する
                    d2_num = new_nodes + 2
                    order['D2'] = d2_num
                    print('line_b', order)

                    # 四角形D2-R3-R4-D1
                    rect_2_name = ['D2', 'R3', 'R4', 'D1']
                    # 四角形R1-R2-D2-L2
                    rect_3_name = ['R1', 'R2', 'D2', 'L2']

            # 辞書の中味に従ってリストの座標データで四角形を作る
            rect_1_list = []
            for name in rect_1_name:
                n = order[name]
                rect_1_list.append(cords[n])
                # tsuma_line =
                # yane_type =
                # f_make_roof(rect_1_list, tsuma_line, yane_type)
            print(rect_1_list)
            # 辞書の中味に従ってリストの座標データで四角形を作る
            rect_2_list = []
            for name in rect_2_name:
                n = order[name]
                rect_2_list.append(cords[n])
                # tsuma_line =
                # yane_type =
                # f_make_roof(rect_2_list, tsuma_line, yane_type)
            print(rect_2_list)
            # 辞書の中味に従ってリストの座標データで四角形を作る
            rect_3_list = []
            for name in rect_3_name:
                n = order[name]
                rect_3_list.append(cords[n])
                # tsuma_line =
                # yane_type =
                # f_make_roof(rect_3_list, tsuma_line, yane_type)
            print(rect_3_list)

        elif arr_lr_p == ['L', 'R', 'R', 'R', 'R', 'R', 'R', 'L']:
            oct_type = '凹型2'
            num1 = order['L1']
            # １つ目の直交する辺は．L点と1つ前の点で結ばれる線分
            # 直交する辺の座標ペア
            if num1 == 0:
                choku_cords_1a = [cords[num1], cords[new_nodes - 1]]
            else:
                choku_cords_1a = [cords[num1], cords[num1 - 1]]
            # 対向する辺は，L点から２つ目と３つ目の点で結ばれる線分
            # 対向する辺の座標ペア
            taiko_cords_1a = []
            if (num1 + 2) > (new_nodes - 1):
                taiko_cords_1a.append(cords[num1 + 2 - new_nodes])
            else:
                taiko_cords_1a.append(cords[num1 + 2])
            if (num1 + 3) > (new_nodes - 1):
                taiko_cords_1a.append(cords[num1 + 3 - new_nodes])
            else:
                taiko_cords_1a.append(cords[num1 + 3])
            # 直交する直線1aと対向する辺との直交条件を確認する
            f_chokuko_check(choku_cords_1a, taiko_cords_1a)
            int_1a_x = int_x
            int_1a_y = int_y
            # 交差角度が制限範囲内でない場合は処理を中断する
            # if theta < 60 or theta > 120:
            #     continue
                # f_tri_mesh(cord2)
            # もう一方の直交する辺は．L点と次の点で結ばれる線分
            # 直交する辺の座標ペア
            if num1 == (new_nodes - 1):
                choku_cords_1b = [cords[num1], cords[0]]
            else:
                choku_cords_1b = [cords[num1], cords[num1 + 1]]
            # 対向する辺は，L点から３つ目と４つ目の点で結ばれる線分
            # 対向する辺の座標ペア
            taiko_cords_1b = []
            if (num1 + 3) > (new_nodes - 1):
                taiko_cords_1b.append(cords[num1 + 3 - new_nodes])
            else:
                taiko_cords_1b.append(cords[num1 + 3])
            if (num1 + 4) > (new_nodes - 1):
                taiko_cords_1b.append(cords[num1 + 4 - new_nodes])
            else:
                taiko_cords_1b.append(cords[num1 + 4])
            # 直交する直線1bと対向する辺との直交条件を確認する
            f_chokuko_check(choku_cords_1b, taiko_cords_1b)
            int_1b_x = int_x
            int_1b_y = int_y
            # 交差角度が制限範囲内でない場合は処理を中断する
            # if theta < 60 or theta > 120:
            #     continue
            # f_tri_mesh(cord2)

            num2 = order['L2']
            # ２つ目の直交する辺は．L点と1つ前の点で結ばれる線分
            # 直交する辺の座標ペア
            if num2 == 0:
                choku_cords_2a = [cords[num2], cords[new_nodes - 1]]
            else:
                choku_cords_2a = [cords[num2], cords[num2 - 1]]
            # 対向する辺は，L点から４つ目と５つ目の点で結ばれる線分
            # 対向する辺の座標ペア
            taiko_cords_2a = []
            if (num2 + 4) > (new_nodes - 1):
                taiko_cords_2a.append(cords[num2 + 4 - new_nodes])
            else:
                taiko_cords_2a.append(cords[num2 + 4])
            if (num2 + 5) > (new_nodes - 1):
                taiko_cords_2a.append(cords[num2 + 5 - new_nodes])
            else:
                taiko_cords_2a.append(cords[num2 + 5])
            # 直交する直線2aと対向する辺との直交条件を確認する
            f_chokuko_check(choku_cords_2a, taiko_cords_2a)
            int_2a_x = int_x
            int_2a_y = int_y
            # 交差角度が制限範囲内でない場合は処理を中断する
            # if theta < 60 or theta > 120:
            #     continue
            # f_tri_mesh(cord2)
            # もう一方の直交する辺は．L点と次の点で結ばれる線分
            # 直交する辺の座標ペア
            if num1 == (new_nodes - 1):
                choku_cords_2b = [cords[num1], cords[0]]
            else:
                choku_cords_2b = [cords[num1], cords[num1 + 1]]
            # 対向する辺は，L点から５つ目と６つ目の点で結ばれる線分
            # 対向する辺の座標ペア
            taiko_cords_2b = []
            if (num1 + 5) > (new_nodes - 1):
                taiko_cords_2b.append(cords[num1 + 5 - new_nodes])
            else:
                taiko_cords_2b.append(cords[num1 + 5])
            if (num1 + 6) > (new_nodes - 1):
                taiko_cords_2b.append(cords[num1 + 6 - new_nodes])
            else:
                taiko_cords_2b.append(cords[num1 + 6])
            # 直交する直線1bと対向する辺との直交条件を確認する
            f_chokuko_check(choku_cords_2b, taiko_cords_2b)
            int_2b_x = int_x
            int_2b_y = int_y
            # 交差角度が制限範囲内でない場合は処理を中断する
            # if theta < 60 or theta > 120:
            #     continue
            # f_tri_mesh(cord2)

            # L点から対向する二辺までの距離を比較する
            # L1点の座標
            print(cords[num1][1])
            print(cords[num1][0])
            # 交点1aの座標
            # print(int_1a_x)
            # print(int_1a_y)
            # 交点1aまでの距離
            div_line_1a = math.sqrt((cords[num1][1] - int_1a_x) ** 2 + (cords[num1][0] - int_1a_y) ** 2)
            print("div_line_a=", div_line_1a)
            # 交点1bの座標
            # print(int_1b_x)
            # print(int_1b_y)
            # 交点1bまでの距離
            div_line_1b = math.sqrt((cords[num1][1] - int_1b_x) ** 2 + (cords[num1][0] - int_1b_y) ** 2)
            print("div_line_b=", div_line_1b)
            # L2点の座標
            print(cords[num2][1])
            print(cords[num2][0])
            # 交点2aの座標
            # print(int_2a_x)
            # print(int_2a_y)
            # 交点2aまでの距離
            div_line_2a = math.sqrt((cords[num2][1] - int_2a_x) ** 2 + (cords[num2][0] - int_2a_y) ** 2)
            print("div_line_a=", div_line_2a)
            # 交点2bの座標
            # print(int_2b_x)
            # print(int_2b_y)
            # 交点2bまでの距離
            div_line_2b = math.sqrt((cords[num2][1] - int_2b_x) ** 2 + (cords[num2][0] - int_2b_y) ** 2)
            print("div_line_b=", div_line_2b)

            # 距離の短い方の線分を分割線とする
            if div_line_1a < div_line_1b:
                print("分割線はdiv_line_a")
                # 分割点はD1a点（交点１）
                d1 = [int_1a_y, int_1a_x]
                # 座標値のリストにD1点の座標値を追加する
                cords.extend([d1])
                print(cords)
                # 頂点並びの辞書に分割点を追加する
                d1_num = new_nodes + 1
                order['D1'] = d1_num
                print('line_a', order)

                # 四角形L1-R1-R2-D1
                rect_1_name = ['L1', 'R1', 'R2', 'D1']

                # 距離の短い方の線分を分割線とする
                if div_line_2a < div_line_2b:
                    print("分割線はdiv_line_a")
                    # 分割点はD1a点（交点１）
                    d2 = [int_2a_y, int_2a_x]
                    # 座標値のリストにD1点の座標値を追加する
                    cords.extend([d2])
                    print(cords)
                    # 頂点並びの辞書に分割点を追加する
                    d2_num = new_nodes + 2
                    order['D2'] = d2_num
                    print('line_a', order)

                    # 四角形D2-R4-R5-R6
                    rect_2_name = ['D2', 'R4', 'R5', 'R6']
                    # 四角形L2-D1-R3-D2
                    rect_3_name = ['L2', 'D1', 'R3', 'D2']

                elif div_line_2a > div_line_2b:
                    print("分割線はdiv_line_b")
                    # 分割点はD1b点（交点１）
                    d2 = [int_2b_y, int_2b_x]
                    # 座標値のリストにD1点の座標値を追加する
                    cords.extend([d2])
                    print(cords)
                    # 頂点並びの辞書に分割点を追加する
                    d2_num = new_nodes + 2
                    order['D2'] = d2_num
                    print('line_b', order)

                    # 四角形L2-D2-R5-R6
                    rect_2_name = ['L2', 'D2', 'R5', 'R6']
                    # 四角形D1-R3-R4-D2
                    rect_3_name = ['D1', 'R3', 'R4', 'D2']

            elif div_line_1a > div_line_1b:
                print("分割線はdiv_line_b")
                # 分割点はD1b点（交点１）
                d1 = [int_1b_y, int_1b_x]
                # 座標値のリストにD1点の座標値を追加する
                cords.extend([d1])
                print(cords)
                # 頂点並びの辞書に分割点を追加する
                d1_num = new_nodes + 1
                order['D1'] = d1_num
                print('line_b', order)

                # 四角形R1-R2-R3-D1
                rect_1_name = ['R1', 'R2', 'R3', 'D1']

                # 距離の短い方の線分を分割線とする
                if div_line_2a < div_line_2b:
                    print("分割線はdiv_line_a")
                    # 分割点はD1a点（交点１）
                    d2 = [int_2a_y, int_2a_x]
                    # 座標値のリストにD1点の座標値を追加する
                    cords.extend([d2])
                    print(cords)
                    # 頂点並びの辞書に分割点を追加する
                    d2_num = new_nodes + 2
                    order['D2'] = d2_num
                    print('line_a', order)

                    # 四角形D2-R4-R5-R6
                    rect_2_name = ['D2', 'R4', 'R5', 'R6']
                    # 四角形L2-L1-D1-D2
                    rect_3_name = ['L2', 'L1', 'D1', 'D2']

                elif div_line_2a > div_line_2b:
                    print("分割線はdiv_line_b")
                    # 分割点はD1b点（交点１）
                    d2 = [int_2b_y, int_2b_x]
                    # 座標値のリストにD1点の座標値を追加する
                    cords.extend([d2])
                    print(cords)
                    # 頂点並びの辞書に分割点を追加する
                    d2_num = new_nodes + 2
                    order['D2'] = d2_num
                    print('line_b', order)

                    # 四角形L2-D2-R5-R6
                    rect_2_name = ['L2', 'D2', 'R5', 'R6']
                    # 四角形L1-D1-R4-D2
                    rect_3_name = ['L1', 'D1', 'R4', 'D2']

            # 辞書の中味に従ってリストの座標データで四角形を作る
            rect_1_list = []
            for name in rect_1_name:
                n = order[name]
                rect_1_list.append(cords[n])
                # tsuma_line =
                # yane_type =
                # f_make_roof(rect_1_list, tsuma_line, yane_type)
            print(rect_1_list)
            # 辞書の中味に従ってリストの座標データで四角形を作る
            rect_2_list = []
            for name in rect_2_name:
                n = order[name]
                rect_2_list.append(cords[n])
                # tsuma_line =
                # yane_type =
                # f_make_roof(rect_2_list, tsuma_line, yane_type)
            print(rect_2_list)
            # 辞書の中味に従ってリストの座標データで四角形を作る
            rect_3_list = []
            for name in rect_3_name:
                n = order[name]
                rect_3_list.append(cords[n])
                # tsuma_line =
                # yane_type =
                # f_make_roof(rect_3_list, tsuma_line, yane_type)
            print(rect_3_list)

        elif arr_lr_p == ['L', 'R', 'R', 'L', 'R', 'R', 'R', 'R']:
            oct_type = '凸型1'
            num1 = order['L1']
            # １つ目の直交する辺は．L点と1つ前の点で結ばれる線分
            # 直交する辺の座標ペア
            if num1 == 0:
                choku_cords_1a = [cords[num1], cords[new_nodes - 1]]
            else:
                choku_cords_1a = [cords[num1], cords[num1 - 1]]
            # 対向する辺は，L点から２つ目と３つ目の点で結ばれる線分
            # 対向する辺の座標ペア
            taiko_cords_1a = []
            if (num1 + 2) > (new_nodes - 1):
                taiko_cords_1a.append(cords[num1 + 2 - new_nodes])
            else:
                taiko_cords_1a.append(cords[num1 + 2])
            if (num1 + 3) > (new_nodes - 1):
                taiko_cords_1a.append(cords[num1 + 3 - new_nodes])
            else:
                taiko_cords_1a.append(cords[num1 + 3])
            # 直交する直線1aと対向する辺との直交条件を確認する
            f_chokuko_check(choku_cords_1a, taiko_cords_1a)
            int_1a_x = int_x
            int_1a_y = int_y
            # 交差角度が制限範囲内でない場合は処理を中断する
            # if theta < 60 or theta > 120:
            #     continue
                # f_tri_mesh(cord2)
            # もう一方の直交する辺は．L点と次の点で結ばれる線分
            # 直交する辺の座標ペア
            if num1 == (new_nodes - 1):
                choku_cords_1b = [cords[num1], cords[0]]
            else:
                choku_cords_1b = [cords[num1], cords[num1 + 1]]
            # 対向する辺は，L点から５つ目と６つ目の点で結ばれる線分
            # 対向する辺の座標ペア
            taiko_cords_1b = []
            if (num1 + 5) > (new_nodes - 1):
                taiko_cords_1b.append(cords[num1 + 5 - new_nodes])
            else:
                taiko_cords_1b.append(cords[num1 + 5])
            if (num1 + 6) > (new_nodes - 1):
                taiko_cords_1b.append(cords[num1 + 6 - new_nodes])
            else:
                taiko_cords_1b.append(cords[num1 + 6])
            # 直交する直線1bと対向する辺との直交条件を確認する
            f_chokuko_check(choku_cords_1b, taiko_cords_1b)
            int_1b_x = int_x
            int_1b_y = int_y
            # 交差角度が制限範囲内でない場合は処理を中断する
            # if theta < 60 or theta > 120:
            #     continue
            # f_tri_mesh(cord2)

            num2 = order['L2']
            # ２つ目の直交する辺は．L点と1つ前の点で結ばれる線分
            # 直交する辺の座標ペア
            if num2 == 0:
                choku_cords_2a = [cords[num2], cords[new_nodes - 1]]
            else:
                choku_cords_2a = [cords[num2], cords[num2 - 1]]
            # 対向する辺は，L点から２つ目と３つ目の点で結ばれる線分
            # 対向する辺の座標ペア
            taiko_cords_2a = []
            if (num2 + 2) > (new_nodes - 1):
                taiko_cords_2a.append(cords[num2 + 2 - new_nodes])
            else:
                taiko_cords_2a.append(cords[num2 + 2])
            if (num2 + 3) > (new_nodes - 1):
                taiko_cords_2a.append(cords[num2 + 3 - new_nodes])
            else:
                taiko_cords_2a.append(cords[num2 + 3])
            # 直交する直線2aと対向する辺との直交条件を確認する
            f_chokuko_check(choku_cords_2a, taiko_cords_2a)
            int_2a_x = int_x
            int_2a_y = int_y
            # 交差角度が制限範囲内でない場合は処理を中断する
            # if theta < 60 or theta > 120:
            #     continue
            # f_tri_mesh(cord2)
            # もう一方の直交する辺は．L点と次の点で結ばれる線分
            # 直交する辺の座標ペア
            if num1 == (new_nodes - 1):
                choku_cords_2b = [cords[num1], cords[0]]
            else:
                choku_cords_2b = [cords[num1], cords[num1 + 1]]
            # 対向する辺は，L点から５つ目と６つ目の点で結ばれる線分
            # 対向する辺の座標ペア
            taiko_cords_2b = []
            if (num1 + 5) > (new_nodes - 1):
                taiko_cords_2b.append(cords[num1 + 5 - new_nodes])
            else:
                taiko_cords_2b.append(cords[num1 + 5])
            if (num1 + 6) > (new_nodes - 1):
                taiko_cords_2b.append(cords[num1 + 6 - new_nodes])
            else:
                taiko_cords_2b.append(cords[num1 + 6])
            # 直交する直線1bと対向する辺との直交条件を確認する
            f_chokuko_check(choku_cords_2b, taiko_cords_2b)
            int_2b_x = int_x
            int_2b_y = int_y
            # 交差角度が制限範囲内でない場合は処理を中断する
            # if theta < 60 or theta > 120:
            #     continue
            # f_tri_mesh(cord2)

            # L点から対向する二辺までの距離を比較する
            # L1点の座標
            print(cords[num1][1])
            print(cords[num1][0])
            # 交点1aの座標
            # print(int_1a_x)
            # print(int_1a_y)
            # 交点1aが R2-L2上にあるかチェックする
            if (taiko_cords_1a[0][1] < int_1a_x < taiko_cords_1a[1][1]) or (taiko_cords_1a[0][1] < int_1a_x < taiko_cords_1a[1][1]):
                # 交点1aまでの距離
                div_line_1a = math.sqrt((cords[num1][1] - int_1a_x) ** 2 + (cords[num1][0] - int_1a_y) ** 2)
                print("div_line_a=", div_line_1a)
            else:
                f_inf = float('inf')
                div_line_1a = f_inf
            # 交点1bの座標
            # print(int_1b_x)
            # print(int_1b_y)
            # 交点1bまでの距離
            div_line_1b = math.sqrt((cords[num1][1] - int_1b_x) ** 2 + (cords[num1][0] - int_1b_y) ** 2)
            print("div_line_b=", div_line_1b)
            # L2点の座標
            print(cords[num2][1])
            print(cords[num2][0])
            # 交点2aの座標
            # print(int_2a_x)
            # print(int_2a_y)
            # 交点2aまでの距離
            div_line_2a = math.sqrt((cords[num2][1] - int_2a_x) ** 2 + (cords[num2][0] - int_2a_y) ** 2)
            print("div_line_a=", div_line_2a)
            # 交点2bの座標
            # print(int_2b_x)
            # print(int_2b_y)
            # 交点2bが L1-R1上にあるかチェックする
            if (taiko_cords_2b[0][1] < int_2b_x < taiko_cords_2b[1][1]) or (
                    taiko_cords_2b[0][1] < int_2b_x < taiko_cords_2b[1][1]):
                # 交点2bまでの距離
                div_line_2b = math.sqrt((cords[num2][1] - int_2b_x) ** 2 + (cords[num2][0] - int_2b_y) ** 2)
                print("div_line_b=", div_line_2b)
            else:
                f_inf = float('inf')
                div_line_2b = f_inf

            # 距離の短い方の線分を分割線とする
            if div_line_1a > div_line_1b:
                print("分割線はdiv_line_b")
                # 分割点はD1b点（交点１）
                d1 = [int_1b_y, int_1b_x]
                # 座標値のリストにD1点の座標値を追加する
                cords.extend([d1])
                print(cords)
                # 頂点並びの辞書に分割点を追加する
                d1_num = new_nodes + 1
                order['D1'] = d1_num
                print('line_b', order)

                # 四角形L1-D1-R5-R6
                rect_1_name = ['L1', 'D1', 'R5', 'R6']

                # 距離の短い方の線分を分割線とする
                if div_line_2a < div_line_2b:
                    print("分割線はdiv_line_a")
                    # 分割点はD2a点（交点２）
                    d2 = [int_2a_y, int_2a_x]
                    # 座標値のリストにD1点の座標値を追加する
                    cords.extend([d2])
                    print(cords)
                    # 頂点並びの辞書に分割点を追加する
                    d2_num = new_nodes + 2
                    order['D2'] = d2_num
                    print('line_a', order)

                    # 四角形L2-R3-R4-D2
                    rect_2_name = ['L2', 'R3', 'R4', 'D2']
                    # 四角形R1-R2-D2-D1
                    rect_3_name = ['R1', 'R2', 'D2', 'D1']

                elif div_line_2a > div_line_2b:
                    print("分割線はdiv_line_b")
                    # 分割点はD2b点（交点２）
                    d2 = [int_2b_y, int_2b_x]
                    # 座標値のリストにD2点の座標値を追加する
                    cords.extend([d2])
                    print(cords)
                    # 頂点並びの辞書に分割点を追加する
                    d2_num = new_nodes + 2
                    order['D2'] = d2_num
                    print('line_b', order)

                    # 四角形L2-D2-R1-R2
                    rect_2_name = ['L2', 'D2', 'R1', 'R2']
                    # 四角形R3-R4-D1-D2
                    rect_3_name = ['R3', 'R4', 'D1', 'D2']

            elif div_line_2a < div_line_2b:
                print("分割線はdiv_line_a")
                # 分割点はD2a点（交点２）
                d2 = [int_2a_y, int_2a_x]
                # 座標値のリストにD2点の座標値を追加する
                cords.extend([d2])
                print(cords)
                # 頂点並びの辞書に分割点を追加する
                d2_num = new_nodes + 2
                order['D2'] = d2_num
                print('line_a', order)

                # 四角形L2-R3-R4-D2
                rect_1_name = ['L2', 'R3', 'R4', 'D2']

                # 距離の短い方の線分を分割線とする
                if div_line_1a < div_line_1b:
                    print("分割線はdiv_line_a")
                    # 分割点はD1a点（交点１）
                    d1 = [int_1a_y, int_1a_x]
                    # 座標値のリストにD1点の座標値を追加する
                    cords.extend([d1])
                    print(cords)
                    # 頂点並びの辞書に分割点を追加する
                    d1_num = new_nodes + 1
                    order['D1'] = d1_num
                    print('line_a', order)

                    # 四角形L1-R1-R2-D1
                    rect_2_name = ['L1', 'R1', 'R2', 'D1']
                    # 四角形D1-D2-R5-R6
                    rect_3_name = ['D1', 'D2', 'R5', 'R6']

                elif div_line_1a > div_line_1b:
                    print("分割線はdiv_line_b")
                    # 分割点はD1b点（交点１）
                    d1 = [int_1b_y, int_1b_x]
                    # 座標値のリストにD1点の座標値を追加する
                    cords.extend([d1])
                    print(cords)
                    # 頂点並びの辞書に分割点を追加する
                    d1_num = new_nodes + 1
                    order['D1'] = d1_num
                    print('line_b', order)

                    # 四角形L1-D1-R5-R6
                    rect_2_name = ['L1', 'D1', 'R5', 'R6']
                    # 四角形R1-R2-D2-D1
                    rect_3_name = ['R1', 'R2', 'D2', 'D1']

            # 辞書の中味に従ってリストの座標データで四角形を作る
            rect_1_list = []
            for name in rect_1_name:
                n = order[name]
                rect_1_list.append(cords[n])
                # tsuma_line =
                # yane_type =
                # f_make_roof(rect_1_list, tsuma_line, yane_type)
            print(rect_1_list)
            # 辞書の中味に従ってリストの座標データで四角形を作る
            rect_2_list = []
            for name in rect_2_name:
                n = order[name]
                rect_2_list.append(cords[n])
                # tsuma_line =
                # yane_type =
                # f_make_roof(rect_2_list, tsuma_line, yane_type)
            print(rect_2_list)
            # 辞書の中味に従ってリストの座標データで四角形を作る
            rect_3_list = []
            for name in rect_3_name:
                n = order[name]
                rect_3_list.append(cords[n])
                # tsuma_line =
                # yane_type =
                # f_make_roof(rect_3_list, tsuma_line, yane_type)
            print(rect_3_list)

        elif arr_lr_p == ['L', 'R', 'R', 'R', 'R', 'L', 'R', 'R']:
            oct_type = '凸型2'
            num1 = order['L1']
            # １つ目の直交する辺は．L点と1つ前の点で結ばれる線分
            # 直交する辺の座標ペア
            if num1 == 0:
                choku_cords_1a = [cords[num1], cords[new_nodes - 1]]
            else:
                choku_cords_1a = [cords[num1], cords[num1 - 1]]
            # 対向する辺は，L点から２つ目と３つ目の点で結ばれる線分
            # 対向する辺の座標ペア
            taiko_cords_1a = []
            if (num1 + 2) > (new_nodes - 1):
                taiko_cords_1a.append(cords[num1 + 2 - new_nodes])
            else:
                taiko_cords_1a.append(cords[num1 + 2])
            if (num1 + 3) > (new_nodes - 1):
                taiko_cords_1a.append(cords[num1 + 3 - new_nodes])
            else:
                taiko_cords_1a.append(cords[num1 + 3])
            # 直交する直線1aと対向する辺との直交条件を確認する
            f_chokuko_check(choku_cords_1a, taiko_cords_1a)
            int_1a_x = int_x
            int_1a_y = int_y
            # 交差角度が制限範囲内でない場合は処理を中断する
            # if theta < 60 or theta > 120:
            #     continue
                # f_tri_mesh(cord2)
            # もう一方の直交する辺は．L点と次の点で結ばれる線分
            # 直交する辺の座標ペア
            if num1 == (new_nodes - 1):
                choku_cords_1b = [cords[num1], cords[0]]
            else:
                choku_cords_1b = [cords[num1], cords[num1 + 1]]
            # 対向する辺は，L点から５つ目と６つ目の点で結ばれる線分
            # 対向する辺の座標ペア
            taiko_cords_1b = []
            if (num1 + 5) > (new_nodes - 1):
                taiko_cords_1b.append(cords[num1 + 5 - new_nodes])
            else:
                taiko_cords_1b.append(cords[num1 + 5])
            if (num1 + 6) > (new_nodes - 1):
                taiko_cords_1b.append(cords[num1 + 6 - new_nodes])
            else:
                taiko_cords_1b.append(cords[num1 + 6])
            # 直交する直線1bと対向する辺との直交条件を確認する
            f_chokuko_check(choku_cords_1b, taiko_cords_1b)
            int_1b_x = int_x
            int_1b_y = int_y
            # 交差角度が制限範囲内でない場合は処理を中断する
            # if theta < 60 or theta > 120:
            #     continue
            # f_tri_mesh(cord2)

            num2 = order['L2']
            # ２つ目の直交する辺は．L点と1つ前の点で結ばれる線分
            # 直交する辺の座標ペア
            if num2 == 0:
                choku_cords_2a = [cords[num2], cords[new_nodes - 1]]
            else:
                choku_cords_2a = [cords[num2], cords[num2 - 1]]
            # 対向する辺は，L点から２つ目と３つ目の点で結ばれる線分
            # 対向する辺の座標ペア
            taiko_cords_2a = []
            if (num2 + 2) > (new_nodes - 1):
                taiko_cords_2a.append(cords[num2 + 2 - new_nodes])
            else:
                taiko_cords_2a.append(cords[num2 + 2])
            if (num2 + 3) > (new_nodes - 1):
                taiko_cords_2a.append(cords[num2 + 3 - new_nodes])
            else:
                taiko_cords_2a.append(cords[num2 + 3])
            # 直交する直線2aと対向する辺との直交条件を確認する
            f_chokuko_check(choku_cords_2a, taiko_cords_2a)
            int_2a_x = int_x
            int_2a_y = int_y
            # 交差角度が制限範囲内でない場合は処理を中断する
            # if theta < 60 or theta > 120:
            #     continue
            # f_tri_mesh(cord2)
            # もう一方の直交する辺は．L点と次の点で結ばれる線分
            # 直交する辺の座標ペア
            if num1 == (new_nodes - 1):
                choku_cords_2b = [cords[num1], cords[0]]
            else:
                choku_cords_2b = [cords[num1], cords[num1 + 1]]
            # 対向する辺は，L点から５つ目と６つ目の点で結ばれる線分
            # 対向する辺の座標ペア
            taiko_cords_2b = []
            if (num1 + 5) > (new_nodes - 1):
                taiko_cords_2b.append(cords[num1 + 5 - new_nodes])
            else:
                taiko_cords_2b.append(cords[num1 + 5])
            if (num1 + 6) > (new_nodes - 1):
                taiko_cords_2b.append(cords[num1 + 6 - new_nodes])
            else:
                taiko_cords_2b.append(cords[num1 + 6])
            # 直交する直線1bと対向する辺との直交条件を確認する
            f_chokuko_check(choku_cords_2b, taiko_cords_2b)
            int_2b_x = int_x
            int_2b_y = int_y
            # 交差角度が制限範囲内でない場合は処理を中断する
            # if theta < 60 or theta > 120:
            #     continue
            # f_tri_mesh(cord2)

            # L点から対向する二辺までの距離を比較する
            # L1点の座標
            print(cords[num1][1])
            print(cords[num1][0])
            # 交点1aの座標
            # print(int_1a_x)
            # print(int_1a_y)
            # 交点1aまでの距離
            div_line_1a = math.sqrt((cords[num1][1] - int_1a_x) ** 2 + (cords[num1][0] - int_1a_y) ** 2)
            print("div_line_b=", div_line_1a)
            # 交点1bの座標
            # print(int_1b_x)
            # print(int_1b_y)
            # 交点1bが L2-R5上にあるかチェックする
            if (taiko_cords_1b[0][1] < int_1b_x < taiko_cords_1b[1][1]) or (taiko_cords_1b[0][1] < int_1b_x < taiko_cords_1b[1][1]):
                # 交点1bまでの距離
                div_line_1b = math.sqrt((cords[num1][1] - int_1b_x) ** 2 + (cords[num1][0] - int_1b_y) ** 2)
                print("div_line_a=", div_line_1b)
            else:
                f_inf = float('inf')
                div_line_1b = f_inf
            # L2点の座標
            print(cords[num2][1])
            print(cords[num2][0])
            # 交点2aの座標
            # print(int_2a_x)
            # print(int_2a_y)
            # 交点2aが R6-L1上にあるかチェックする
            if (taiko_cords_2a[0][1] < int_2a_x < taiko_cords_2a[1][1]) or (
                    taiko_cords_2a[0][1] < int_2a_x < taiko_cords_2a[1][1]):
                # 交点2bまでの距離
                div_line_2a = math.sqrt((cords[num2][1] - int_2a_x) ** 2 + (cords[num2][0] - int_2a_y) ** 2)
                print("div_line_b=", div_line_2a)
            else:
                f_inf = float('inf')
                div_line_2a = f_inf
            # 交点2bの座標
            # print(int_2b_x)
            # print(int_2b_y)
            # 交点2bまでの距離
            div_line_2b = math.sqrt((cords[num2][1] - int_2b_x) ** 2 + (cords[num2][0] - int_2b_y) ** 2)
            print("div_line_a=", div_line_2b)

            # 距離の短い方の線分を分割線とする
            if div_line_1a < div_line_1b:
                print("分割線はdiv_line_a")
                # 分割点はD1a点（交点１）
                d1 = [int_1a_y, int_1a_x]
                # 座標値のリストにD1点の座標値を追加する
                cords.extend([d1])
                print(cords)
                # 頂点並びの辞書に分割点を追加する
                d1_num = new_nodes + 1
                order['D1'] = d1_num
                print('line_a', order)

                # 四角形L1-R1-R2-D1
                rect_1_name = ['L1', 'R1', 'R2', 'D1']

                # 距離の短い方の線分を分割線とする
                if div_line_2a < div_line_2b:
                    print("分割線はdiv_line_a")
                    # 分割点はD2a点（交点２）
                    d2 = [int_2a_y, int_2a_x]
                    # 座標値のリストにD1点の座標値を追加する
                    cords.extend([d2])
                    print(cords)
                    # 頂点並びの辞書に分割点を追加する
                    d2_num = new_nodes + 2
                    order['D2'] = d2_num
                    print('line_a', order)

                    # 四角形L2-R5-R6-D2
                    rect_2_name = ['L2', 'R5', 'R6', 'D2']
                    # 四角形R3-R4-D2-D1
                    rect_3_name = ['R3', 'R4', 'D2', 'D1']

                elif div_line_2a > div_line_2b:
                    print("分割線はdiv_line_b")
                    # 分割点はD2b点（交点２）
                    d2 = [int_2b_y, int_2b_x]
                    # 座標値のリストにD2点の座標値を追加する
                    cords.extend([d2])
                    print(cords)
                    # 頂点並びの辞書に分割点を追加する
                    d2_num = new_nodes + 2
                    order['D2'] = d2_num
                    print('line_b', order)

                    # 四角形L2-D2-R3-R4
                    rect_2_name = ['L2', 'D2', 'R3', 'R4']
                    # 四角形R5-R6-D1-D2
                    rect_3_name = ['R5', 'R6', 'D1', 'D2']

            elif div_line_2a > div_line_2b:
                print("分割線はdiv_line_b")
                # 分割点はD2b点（交点２）
                d2 = [int_2b_y, int_2b_x]
                # 座標値のリストにD2点の座標値を追加する
                cords.extend([d2])
                print(cords)
                # 頂点並びの辞書に分割点を追加する
                d2_num = new_nodes + 2
                order['D2'] = d2_num
                print('line_b', order)

                # 四角形L2-D2-R3-R4
                rect_1_name = ['L2', 'D2', 'R3', 'R4']

                # 距離の短い方の線分を分割線とする
                if div_line_1a < div_line_1b:
                    print("分割線はdiv_line_a")
                    # 分割点はD1a点（交点１）
                    d1 = [int_1a_y, int_1a_x]
                    # 座標値のリストにD1点の座標値を追加する
                    cords.extend([d1])
                    print(cords)
                    # 頂点並びの辞書に分割点を追加する
                    d1_num = new_nodes + 1
                    order['D1'] = d1_num
                    print('line_a', order)

                    # 四角形L1-R1-R2-D1
                    rect_2_name = ['L1', 'R1', 'R2', 'D1']
                    # 四角形D1-D2-R5-R6
                    rect_3_name = ['D1', 'D2', 'R5', 'R6']

                elif div_line_1a > div_line_1b:
                    print("分割線はdiv_line_b")
                    # 分割点はD1b点（交点１）
                    d1 = [int_1b_y, int_1b_x]
                    # 座標値のリストにD1点の座標値を追加する
                    cords.extend([d1])
                    print(cords)
                    # 頂点並びの辞書に分割点を追加する
                    d1_num = new_nodes + 1
                    order['D1'] = d1_num
                    print('line_b', order)

                    # 四角形L1-D1-R5-R6
                    rect_2_name = ['L1', 'D1', 'R5', 'R6']
                    # 四角形R1-R2-D2-D1
                    rect_3_name = ['R1', 'R2', 'D2', 'D1']

            # 辞書の中味に従ってリストの座標データで四角形を作る
            rect_1_list = []
            for name in rect_1_name:
                n = order[name]
                rect_1_list.append(cords[n])
                # tsuma_line =
                # yane_type =
                # f_make_roof(rect_1_list, tsuma_line, yane_type)
            print(rect_1_list)
            # 辞書の中味に従ってリストの座標データで四角形を作る
            rect_2_list = []
            for name in rect_2_name:
                n = order[name]
                rect_2_list.append(cords[n])
                # tsuma_line =
                # yane_type =
                # f_make_roof(rect_2_list, tsuma_line, yane_type)
            print(rect_2_list)
            # 辞書の中味に従ってリストの座標データで四角形を作る
            rect_3_list = []
            for name in rect_3_name:
                n = order[name]
                rect_3_list.append(cords[n])
                # tsuma_line =
                # yane_type =
                # f_make_roof(rect_3_list, tsuma_line, yane_type)
            print(rect_3_list)

        elif arr_lr_p == ['L', 'R', 'R', 'R', 'L', 'R', 'R', 'R']:
            oct_type = 'Ｓ型'
        print(oct_type)


    # 普通建物を１件ずつモデリングする（逐次処理）
    def main():
        list_len = len(hutsu_list)

        print('普通建物データ数＝', list_len)
        for d in range(list_len):
            print("データ番号=", d)

            # 傾斜屋根でモデリングする
            sloping_roof = True

            # リストから要素の値を抽出する
            data = hutsu_list[d]
            print(data)
            f_ext_elem(data)

            # 頂点数を数える，
            vert = len(cord2)
            print('頂点数', vert)

            # 頂点数をチェックする，２以下の場合は処理を中止して次の行に進む
            if vert <= 2:
                continue
                # 頂点数が２以下なのでモデリングしない

            # 閉じた図形かどうかを判断し頂点数を求める
            f_chk_close(vert)

            # 近接している頂点を削除する
            f_chk_vert_dist(nodes)

            # 近接する頂点の削除により頂点数が５以下となった場合も処理は中断しない．
            # if new_nodes < 6:
            #     continue
            # 処理を続けて４角形にする．４角形にならない場合は，陸屋根建物とするため３角形分割する．

            # 頂点数が奇数の場合は，偶数になるように最大鈍角の頂点を削除する
            if new_nodes % 2 != 0:
                f_flat_vert(new_nodes)

                # 頂点数が偶数とならなかった場合は，陸屋根建物とするため３角形分割する．
                if ret_nodes % 2 != 0:
                    sloping_roof = False
                    continue
                    # f_tri_mesh(cord2)

            # 頂点がL点かどうかチェックする（外積計算）
            f_ccw_check(new_nodes)

            # 凹角の角度制限
            print('凹角の角度制限', in_angle)
            for i in range(len(in_angle)):
                if in_angle[i] != 0:
                    print('内角', in_angle[i])
                    lo_ang = 135
                    up_ang = 315
                    if in_angle[i] < lo_ang or in_angle[i] > up_ang:
                        break

            # 左回りの頂点数と右回りの頂点数を比べて時計回りか反時計回りか判定する
            if LH < RH:
                print("左回り")

            # 頂点が時計回りの場合は，反時計回りに変更する
            if LH > RH:
                print("右回り")
                f_back_reverse(new_nodes)

            # 四角形分割する，四角形分割のために多角形から凹頂点のL点を抽出する
            # Ｎ角形　内角数：N=2x,x=N/2，凹角数：L=x-2=N/2-2
            l_cnt = new_nodes / 2 - 2
            # L点のリストとR点のリストを作成する
            global l_list
            l_list = []  # L点のリストを用意する
            global r_list
            r_list = []  # R点のリストを用意する
            global r_suslist
            r_suslist = []  # R点の予備のリストを用意する
            # 頂点並びのL点・R点の辞書を作成する
            global order
            order = {}  # 頂点データの並び順を格納する

            # L点とR点をリストおよび辞書に振り分ける
            gene_lr_listdic(new_nodes)

            # L点の数が凹角の数と一致しない場合は，陸屋根建物とするため３角形分割する．
            print(len(l_list))
            print(l_cnt)
            if len(l_list) != l_cnt:
                sloping_roof = False
                continue
                # f_tri_mesh(cord2)

            # ６角形の四角形分割
            if new_nodes == 6:
                hexagonal_divider(cord2)

            # ８角形の四角形分割
            elif new_nodes == 8:
                octagonal_divider(cord2)

            # 屋根タイプ別の比率を設定する
            # モデリングする
    main()


class MyForm(QDialog):

    def __init__(self, parent=None):
        # 「コンストラクタ」クラスの初期設定などを行うためのメソッド
        QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.fileOpenButton.clicked.connect(self.f_load_data)
        self.ui.fileOpenButton_2.clicked.connect(self.f_load_data_2)
        self.ui.buildStartButton_1.clicked.connect(f_build_start)

    def f_load_data(self):

        # デスクトップが表示される
        # 第二引数はダイアログのタイトル、第三引数は表示するパス
        filename = QFileDialog.getOpenFileName(self, 'Open file', os.path.expanduser('~') + '/Desktop',
                                               "GeoJSON files (*.geojson)")
        # ローカルディスクから開く
        # filename = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        # filename[0]は選択したファイルのパス（ファイル名を含む）
        if filename[0]:
            fr = open(filename[0], 'r', encoding='utf-8')
            # テキストブラウザにファイル内容書き込み
            with fr:
                data = fr.read()
                self.ui.textBrowser.setText(data)
                # print(data)

            fj = open(filename[0], 'r', encoding='utf-8')
            # JSONファイルを辞書型データに変換する
            with fj:
                src = json.load(fj)
                # print(src)

        # ラインエディットにファイル名書き込み
        fname = Path(filename[0]).name
        self.ui.loadFileName.setText(fname)

        # 辞書型データを読み取って建物種別ごとにリストに書き込む
        global hutsu_list
        hutsu_list = []
        global kenro_list
        kenro_list = []
        global sonota_list
        sonota_list = []

        for i in range(len(src.get('features'))):
            # キー「features」の中の値のデータ数を数えている
            ftr = src.get('features')[i]
            # print('No=', str(i))
            prop = ftr.get('properties')
            kind = prop.get('種別')

            if kind == "普通建物":
                hutsu_list.append(ftr)
            elif kind == "堅ろう建物":
                kenro_list.append(ftr)
            else:
                sonota_list.append(ftr)

    def f_load_data_2(self):
        # デスクトップが表示される
        # 第二引数はダイアログのタイトル、第三引数は表示するパス
        filename = QFileDialog.getOpenFileName(self, 'Open file', os.path.expanduser('~') + '/Desktop',
                                               "GeoJSON files (*.geojson)")
        # ローカルディスクから開く
        # filename = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        # filename[0]は選択したファイルのパス（ファイル名を含む）
        if filename[0]:
            fr = open(filename[0], 'r', encoding='utf-8')
            # テキストブラウザにファイル内容書き込み
            with fr:
                data = fr.read()
                self.ui.textBrowser_2.setText(data)

            fj = open(filename[0], 'r', encoding='utf-8')
            # JSONファイルを辞書型データに変換する
            with fj:
                src = json.load(fj)

        # ラインエディットにファイル名書き込み
        fname = Path(filename[0]).name
        self.ui.loadFileName_2.setText(fname)

        # GeoJSONファイルからfid，種別，coordinatesを取得して一時ファイルに出力する
        # 出力するファイルの形式をどうするか？
        with open('temp_2.txt', 'w', encoding='UTF-8') as ft:
            for i in range(len(src.get('features'))):
                ftr = src.get('features')[i]
                ft.write(str(i) + '\t')
                # prop = ftr.get('properties')
                # elevation = prop.get('標高')
                # ft.write(elevation + '\t')
                geom = ftr.get('geometry')
                cords = geom.get('coordinates')
                ft.write(str(cords) + '\n')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    # sys.exit(app.exec_())
    app.exec_()
