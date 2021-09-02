import sys
import os
import json
import itertools
import math
# import numpy as np
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
        print(val_id)
        # val_fid = prop.get('fid')
        # kind = prop.get('種別')
        # global name
        name = prop.get('名称')
        print(name)
        global elevation
        elevation = prop.get('median標高')
        print(elevation)
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
            cos_theta = (vect_ax * vect_ay + vect_bx * vect_by) / (vector_a * vector_b)
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

    # 外積を求めてL点かどうか判断する
    def f_ccw_check(ccw_nodes):
        global LH
        LH = 0  # 左回り（反時計回り）
        global RH
        RH = 0  # 右回り（時計回り）
        global S
        S = []
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
                print(naikaku)
                # 凹角の角度制限
                if naikaku > 280 or naikaku < 260:
                    continue
            elif S[j] < 0:  # 右回り
                RH += 1

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

    # 普通建物を１件ずつモデリングする（逐次処理）
    def main():
        list_len = len(hutsu_list)
        # if list_len == 0:
        #
        print('普通建物データ数＝', list_len)
        for d in range(list_len):
            print("データ番号=", d)

            # リストから要素の値を抽出する
            data = hutsu_list[d]
            print(data)
            f_ext_elem(data)

            # 頂点数を数える，
            vert = len(cord2)
            print(vert)

            # 頂点数をチェックする，２以下の場合は処理を中止して次の行に進む
            if vert <= 2:
                continue

            # 閉じた図形かどうかを判断し頂点数を求める
            f_chk_close(vert)

            # 近接している頂点を削除する
            f_chk_vert_dist(nodes)

            # 頂点数が奇数の場合は，偶数になるように最大鈍角の頂点を削除する
            if new_nodes % 2 != 0:
                f_flat_vert(new_nodes)
                # if (new_nodes % 2 != 0):
                #     continue

            # 頂点がL点かどうかチェックする（外積計算）
            f_ccw_check(new_nodes)

            # 左回りの頂点数と右回りの頂点数を比べて時計回りか反時計回りか判定する
            if LH < RH:
                print("左回り")

            # 頂点が時計回りの場合は，反時計回りに変更する
            if LH > RH:
                print("右回り")
                f_back_reverse(new_nodes)

            # 四角形分割する，四角形分割のために多角形から凹頂点のL点を抽出する
            # Ｎ角形　内角数：N=2x,x=N/2，凹角数：L=x-2=N/2-2
            # l_cnt = new_nodes / 2 - 2
            # L点のリストとR点のリストを作成する
            l_list = []  # L点のリストを用意する
            r_list = []  # R点のリストを用意する
            r_suslist = []  # R点の予備のリストを用意する
            # 頂点並びのL点・R点の辞書を作成する
            order = {}  # 頂点データの並び順を格納する
            l_num = 1
            r_num = 1

            for i in range(new_nodes):
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

            # L点の直交条件．対向する辺との交点の角度制限を確認する．
            for LR_key in order:
                ini = LR_key[0]
                if ini == 'L':
                    print(LR_key)
                    num = order[LR_key]
                    # print(num)

                    # 直交する辺は．L点と1つ前の点で結ばれる線分
                    # 直交する辺の座標ペア
                    choku_cords = [cord2[num], cord2[num - 1]]

                    # 対向する辺は，L点から２つ目と３つ目の点で結ばれる線分
                    # 対向する辺の座標ペア
                    # hen_coprds = [[] for _ in range(hen_cnt)]
                    taiko_cords = []
                    if (num + 2) > (new_nodes - 1):
                        taiko_cords.append(cord2[num + 2 - new_nodes])
                    else:
                        taiko_cords.append(cord2[num + 2])
                    if (num + 3) > (new_nodes - 1):
                        taiko_cords.append(cord2[num + 2 - new_nodes + 1])
                    else:
                        taiko_cords.append(cord2[num + 3])

                    print("choku_cords", choku_cords)
                    print("taiko_cords", taiko_cords)

                    # print(list(itertools.chain.from_iterable(choku_cords)))
                    # print(tuple(itertools.chain.from_iterable(choku_cords)))

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
                    int_x = ans[x]
                    int_y = ans[y]

                    # 内積を計算して交差する角度を求める
                    # ベクトルA　交点とL1点を結ぶベクトル
                    f_vector_length(choku_cords[0][1], choku_cords[0][0], int_x, int_y)
                    vect_ax = vect_x
                    vect_ay = vect_y
                    vector_a = vector

                    # ベクトルB　交点と２つ目の点を結ぶベクトル
                    f_vector_length(taiko_cords[0][1], taiko_cords[0][0], int_x, int_y)
                    vect_bx = vect_x
                    vect_by = vect_y
                    vector_b = vector

                    # ベクトルの交差角度
                    f_cross_angle(vect_ax, vect_ay, vect_bx, vect_by, vector_a, vector_b)
                    # 角度を求める
                    print("角度", theta)

                    if theta < 60 or theta > 120:
                        break
                else:
                    continue
                print("Break")
            print("END")

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

# def main():
#     print(fid)
#
# main()
