import sys
import os
import json
import itertools

from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtCore import QDirIterator
# from PyQt5 import QDirIterator
# from pathlib import Path
from SteraPyDialog import *


class MyForm(QDialog):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.fileOpenButton.clicked.connect(self.openfile)

    def openfile(self):
        # デスクトップが表示される
        # 第二引数はダイアログのタイトル、第三引数は表示するパス
        filename = QFileDialog.getOpenFileName(self, 'Open file', os.path.expanduser('~') + '/Desktop', \
                                               "GeoJSON files (*.geojson)")
        # ローカルディスクから開く
        # filename = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        # filename[0]は選択したファイルのパス（ファイル名を含む）
        if filename[0]:
            f = open(filename[0], 'r', encoding='utf-8')
            # テキストブラウザにファイル内容書き込み
            with f:
                src = json.load(f)
        # print(filename[0])
        # print(f)

        # 辞書インデックス確認
        # print(src.keys())   # ['type', 'name', 'crs', 'features']
        # フィーチャーの総数
        # print(len(src.get('features')))
        # ftr = src.get('features')[0]
        # featuresの辞書インデックスの確認
        # print(ftr.keys())   # ['type', 'properties', 'geometry']
        # properties情報の取得
        # prop = ftr.get('properties')
        # propertiesの辞書インデックスの確認
        # print(prop.keys())
        # ['id', 'fid', '整備データ', '整備デーA', '整備完了日', 'orgGILvl', 'orgMDId', '表示区分', '種別', '名称']
        # fid = prop.get('fid')
        # print(fid)
        # kind = prop.get('種別')
        # print(kind)
        # geometry情報の取得
        # geom = ftr.get('geometry')
        # geometryの辞書インデックスの確認
        # print(geom.keys())  # ['type', 'coordinates']
        # cords = geom.get('coordinates')
        # print(cords)
        # cord2 = list(itertools.chain.from_iterable(cords))
        # print(cord2)
        # vert = len(cord2)
        # print(vert)

        for i in range(len(src.get('features'))):
            ftr = src.get('features')[i]
            print(i)
            prop = ftr.get('properties')
            fid = prop.get('fid')
            print(fid)
            kind = prop.get('種別')
            print(kind)
            geom = ftr.get('geometry')
            cords = geom.get('coordinates')
            cord2 = list(itertools.chain.from_iterable(cords))
            vert = len(cord2)
            print(vert)
            print(cord2)



        # print(fd)
        # print(jsn2)
        # for jsn_key in jsn2:
        #     print(jsn_key)
        # for jsn_val in jsn2.values():
        #     print(jsn_val)


        # ラインエディットにファイル名書き込み
        # fname = Path(filename[0]).name
        # self.ui.loadFileName.setText(fname)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    # sys.exit(app.exec_())
    app.exec_()
