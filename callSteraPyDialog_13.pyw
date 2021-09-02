import sys
import os
import json
import itertools

from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtCore import QDirIterator
# from PyQt5 import QDirIterator
from pathlib import Path
from SteraPyDialog import *


class MyForm(QDialog):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.fileOpenButton.clicked.connect(self.load_data)
        self.ui.fileOpenButton_2.clicked.connect(self.load_data_2)

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
                print(src)

        # ラインエディットにファイル名書き込み
        fname = Path(filename[0]).name
        self.ui.loadFileName.setText(fname)

        # GeoJSONファイルからfid，種別，coordinatesを取得して一時ファイルに出力する
        # 出力するファイルの形式をどうするか？
        with open('temp.txt', 'w', encoding='UTF-8') as ft:
        # ft = open('temp.txt', 'w', encoding='UTF-8')
            for i in range(len(src.get('features'))):
                ftr = src.get('features')[i]
                ft.write(str(i) + '\t')
                print(str(i))
                prop = ftr.get('properties')
                fid = prop.get('fid')
                ft.write(fid + '\t')
                print(fid)
                kind = prop.get('種別')
                ft.write(kind + '\t')
                print('種別')
                elevation = prop.get('median標高')
                ft.write(str(elevation) + '\t')
                print('median標高')
                geom = ftr.get('geometry')
                cords = geom.get('coordinates')
                cord2 = list(itertools.chain.from_iterable(cords))
                vert = len(cord2)
                ft.write(str(vert) + '\t')
                print(vert)
                ft.write(str(cord2) + '\n')
                for i in range(vert):
                    print(cord2[i][0])
                    print(cord2[i][1])
        # ft.close()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    # sys.exit(app.exec_())
    app.exec_()
