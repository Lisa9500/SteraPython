import csv
import sys
import os
import json
import itertools
import math
import numpy as np

from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtCore import QDirIterator
# from PyQt5 import QDirIterator
from pathlib import Path
from SteraPyDialog import *


class MyForm(QDialog):

    def __init__(self, parent=None):
        # 「コンストラクタ」クラスの初期設定などを行うためのメソッド
        QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.fileOpenButton.clicked.connect(self.load_data)
        self.ui.fileOpenButton_2.clicked.connect(self.load_data_2)
        self.ui.buildStartButton_1.clicked.connect(self.build_start)


    def load_data(self):

        # デスクトップが表示される
        # 第二引数はダイアログのタイトル、第三引数は表示するパス
        filename = QFileDialog.getOpenFileName(self, 'Open file', os.path.expanduser('~') + '/Desktop', \
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
            id = prop.get('id')
            fid = prop.get('fid')
            kind = prop.get('種別')
            # name = prop.get('名称')
            # elevation = prop.get('median標高')
            # geom = ftr.get('geometry')
            # cords = geom.get('coordinates')

            if(kind == "普通建物"):
                hutsu_list.append(ftr)
            elif(kind == "堅ろう建物"):
                kenro_list.append(ftr)
            else:
                sonota_list.append(ftr)


    def load_data_2(self):
        # デスクトップが表示される
        # 第二引数はダイアログのタイトル、第三引数は表示するパス
        filename = QFileDialog.getOpenFileName(self, 'Open file', os.path.expanduser('~') + '/Desktop', \
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


        # 閉じた図形かどうかチェックする
        def chk_close(vert):
            if ((cord2[0][0] == cord2[vert-1][0]) and (cord2[0][1] == cord2[vert-1][1])):
                global nodes
                nodes = vert - 1

        # 頂点間の距離をチェックする，近接する頂点を削除する
        def chk_vert_dist(nodes):
            del_nodes_lst = []
            global new_nodes
            new_nodes = 0
            for j in range(nodes):
                # 次の頂点までの距離を求める
                if (j != (nodes - 1)):
                    # ベクトルAのX座標の差分
                    vect_x = cord2[j + 1][0] - cord2[j][0]
                    # ベクトルAのY座標の差分
                    vect_y = cord2[j + 1][1] - cord2[j][1]
                    print(j, "ベクトルX", vect_x)
                    print(j, "ベクトルY", vect_y)
                else:
                    vect_x = cord2[0][0] - cord2[j][0]
                    vect_y = cord2[0][1] - cord2[j][1]
                    print(j, "ベクトルX", vect_x)
                    print(j, "ベクトルY", vect_y)
                if(abs(vect_x) < 1.0 and abs(vect_y) < 1.0):
                    del_nodes_lst.append(j + 1)
            print('削除するノード', del_nodes_lst)

            del_cnt = len(del_nodes_lst)
            if(del_cnt != 0):
                in_cnt = 0
                for lst in range(del_cnt):
                    # print(del_nodes_lst[lst])
                    cord2.pop(del_nodes_lst[lst] - in_cnt)
                    in_cnt += 1
                new_nodes = nodes - del_cnt
                for j in range(new_nodes):
                    print(j, 'X', cord2[j][0])
                    print(j, 'Y', cord2[j][1])
            if(new_nodes == 0):
                new_nodes = nodes
            print('new_nodes=', new_nodes)

        # 頂点数が奇数の場合，最大鈍角の頂点を削除する
        def flat_vert(new_nodes):
            # 内積を求めて３点からなら角度を求める，
            max_deg = 0
            del_codes = 0
            for j in range(new_nodes):
                # 隣合う点との間の距離から辺の長さを求める
                if(j != (new_nodes - 1)):
                    # ベクトルAのX座標の差分
                    vect_ax = cord2[j + 1][0] - cord2[j][0]
                    # ベクトルAのY座標の差分
                    vect_ay = cord2[j + 1][1] - cord2[j][1]
                    # ベクトルAの長さ
                    vector_a = math.sqrt(vect_ax ** 2 + vect_ay ** 2)
                    print(j, "ベクトルAx", vect_ax)
                    print(j, "ベクトルAy", vect_ay)
                    print(j, "ベクトルA", vector_a)
                else:
                    vect_ax = cord2[0][0] - cord2[j][0]
                    vect_ay = cord2[0][1] - cord2[j][1]
                    vector_a = math.sqrt(vect_ax ** 2 + vect_ay ** 2)
                    print(j, "ベクトルAx", vect_ax)
                    print(j, "ベクトルAy", vect_ay)
                    print(j, "ベクトルA", vector_a)
                if (j != 0):
                    # ベクトルBのX座標の差分
                    vect_bx = cord2[j - 1][0] - cord2[j][0]
                    # ベクトルBのY座標の差分
                    vect_by = cord2[j - 1][1] - cord2[j][1]
                    # ベクトルBの長さ
                    vector_b = math.sqrt(vect_bx ** 2 + vect_by ** 2)
                    print(j, "ベクトルBx", vect_bx)
                    print(j, "ベクトルBy", vect_by)
                    print(j, "ベクトルB", vector_b)
                else:
                    vect_bx = cord2[new_nodes - 1][0] - cord2[0][0]
                    vect_by = cord2[new_nodes - 1][1] - cord2[0][1]
                    vector_b = math.sqrt(vect_bx ** 2 + vect_by ** 2)
                    print(j, "ベクトルBx", vect_bx)
                    print(j, "ベクトルBy", vect_by)
                    print(j, "ベクトルB", vector_b)
                # cosθを求める
                cos_theta = (vect_ax * vect_ay + vect_bx * vect_by) / (vector_a * vector_b)
                print(j, "cosθ", cos_theta)
                # 角度を求める
                theta = math.degrees(math.acos(cos_theta))
                print(j, "角度", theta)
                # 最大鈍角（175°～185°）の頂点を削除する
                if(theta > max_deg):
                    max_deg = theta
                    del_codes = j
            print('max_deg=', max_deg)
            if(max_deg > 175 and max_deg < 185):
                print('削除するノード', del_codes)
                cord2.pop(del_codes)
                new_nodes -= 1
            print('new_nodes=', new_nodes)
            for j in range(new_nodes):
                print(j, 'X', cord2[j][0])
                print(j, 'Y', cord2[j][1])

        # 頂点の並びが左回りかチェックする
        def ccw_chk(new_nodes):
            # global LH  # 左回り（反時計回り）
            LH = 0
            # global RH  # 右回り（時計回り）
            RH = 0
            # 外積を計算する
            for j in range(new_nodes):
                xs = cord2[j][0]
                ys = cord2[j][1]
                if(j == 1):
                    xp = cord2[new_nodes - 1][0]
                    yp = cord2[new_nodes - 1][1]
                    xn = cord2[j + 1][0]
                    yn = cord2[j + 1][1]
                elif(j == new_nodes - 1):
                    xp = cord2[j - 1][0]
                    yp = cord2[j - 1][1]
                    xn = cord2[0][0]
                    yn = cord2[0][1]
                else:
                    xp = cord2[j - 1][0]
                    yp = cord2[j - 1][1]
                    xn = cord2[j + 1][0]
                    yn = cord2[j + 1][1]
                S = (xp - xs) * (yn - ys) - (xn - xs) * (yp - ys)
                # 外積の結果で左回りか右回りか判断する
                if(S > 0):  # 左回り
                    LH += 1
                elif(S < 0): # 右回り
                    RH += 1
            print('LH=', LH)
            print('RH=', RH)
            if(LH > RH):
                print("左回り")

            # 左回りの頂点数と右回りの頂点数を比べて時計回りか反時計回りか判定する
            if(LH < RH):    # 時計回りなので反時計回りに並び変える
                print("右回り")
                rev_cords = [[] * 2 for j in range(new_nodes)]
                for j in range(1, new_nodes):
                    rev_cords[j][0] = cord2[new_nodes - j][0]
                    rev_cords[j][0] = cord2[new_nodes - j][1]
                for j in range(1, new_nodes):
                    cord2[j][0] = rev_cords[j][0]
                    cord2[j][1] = rev_cords[j][1]
                for j in range(new_nodes):
                    print(j, 'X', cord2[j][0])
                    print(j, 'Y', cord2[j][1])


    def build_start(self):

        # リストの要素から値を取得する
        def ext_elem(data):
            print(data)
            ftr = data
            prop = ftr.get('properties')
            id = prop.get('id')
            fid = prop.get('fid')
            kind = prop.get('種別')
            name = prop.get('名称')
            elevation = prop.get('median標高')
            geom = ftr.get('geometry')
            cords = geom.get('coordinates')

        # 普通建物を１件ずつモデリングする（逐次処理）
        list_len = len(hutsu_list)
        for d in range(list_len):
            # リストから要素の値を抽出する
            data = hutsu_list[d]
            ext_elem(data)
            # 頂点数をチェックする
            # 閉じた図形かチェックする
            # 頂点間の距離をチェックする
            # 最大鈍角をチェックする
            # 左回りをチェックする
            # 四角形分割する
            # 屋根タイプ別の比率を設定する
            # モデリングする


        # 建物種別ごとにモデリングを行う
        # elevation = prop.get('median標高')
        # geom = ftr.get('geometry')
        # cords = geom.get('coordinates')
        # cord2 = list(itertools.chain.from_iterable(cords))
        # global vert
        # vert = len(cord2)
        # print('vert=', vert)
        # 頂点数のチェック，２以下の場合は処理を中止して次の行に進む
        # if (vert <= 2):
        #     continue
        # 閉じた図形かどうかを判断し頂点数を求める
        # chk_close(vert)
        # print("頂点数=",nodes)
        # 近接している頂点を削除する
        # chk_vert_dist(nodes)
        # 頂点数が奇数の場合は，偶数になるように頂点を削除する
        # if(new_nodes % 2 != 0):
        #     flat_vert(new_nodes)
        # 頂点の並びが左回りかどうかチェックする
        # ccw_chk(new_nodes)


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

