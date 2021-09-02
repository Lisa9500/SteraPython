# -*- coding: utf-8 -*-

import os

# Qt for Pythonのクラスを使えるようにする
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


# 自作ダイアログクラス
class MyFirstDialog(QDialog):
    # ウィンドウの初期化処理
    def __init__(self, parent=None):
        # ベース・クラスの初期化
        super(MyFirstDialog, self).__init__(parent)

        # ウィンドウタイトルを設定
        self.setWindowTitle("Special Dialogs")

        layout = QVBoxLayout()

        # ファイル保存ダイアログを表示するためのボタンを設定
        fileSavingButton = QPushButton("Save file.")
        fileSavingButton.clicked.connect(self.saveFile)
        layout.addWidget(fileSavingButton)

        # ファイルオープンダイアログを表示するためのボタンを設定
        fileOpenButton = QPushButton("Open file.")
        fileOpenButton.clicked.connect(self.openFile)
        layout.addWidget(fileOpenButton)

        self.setLayout(layout)

    # ファイル保存ダイアログの表示
    def saveFile(self):
        (fileName, selectedFilter) = QFileDialog.getSaveFileName(self, 'Save file',
                                                                 os.path.expanduser('~') + '/Desktop')
        if fileName != "":
            QMessageBox.information(self, "File", fileName)

    # ファイルオープンダイアログの表示
    def openFile(self):
        # デスクトップが表示される
        # (fileName, selectedFilter) = QFileDialog.getOpenFileName(self, 'Open file',
        #                                                          os.path.expanduser('~') + '/Desktop')
        fileName = QFileDialog.getOpenFileName(self, 'Open file',
                                                                 os.path.expanduser('~') + '/Desktop', "GeoJSON files (*.geojson)")
        if fileName != "":
            QMessageBox.information(self, "File", fileName)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    # 自作ダイアログをインスタンス化して表示
    ui = MyFirstDialog()
    ui.show()

    app.exec_()
