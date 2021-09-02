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

        # ファイルオープンダイアログ（複数選択可能）を表示するためのボタンを設定
        filesOpenButton = QPushButton("Open files.")
        filesOpenButton.clicked.connect(self.openFiles)
        layout.addWidget(filesOpenButton)

        # ディレクトリ選択ダイアログを表示するためのボタンを設定
        dirSelectionButton = QPushButton("Select directory.")
        dirSelectionButton.clicked.connect(self.selectDirectory)
        layout.addWidget(dirSelectionButton)

        # フォント選択ダイアログを表示するためのボタンを設定
        fontSelectionButton = QPushButton("Select font.")
        fontSelectionButton.clicked.connect(self.selectFont)
        layout.addWidget(fontSelectionButton)

        # 色選択ダイアログを表示するためのボタンを設定
        colorSelectionButton = QPushButton("Select color.")
        colorSelectionButton.clicked.connect(self.selectColor)
        layout.addWidget(colorSelectionButton)

        self.setLayout(layout)

    # ファイル保存ダイアログの表示
    def saveFile(self):
        (fileName, selectedFilter) = QFileDialog.getSaveFileName(self, 'Save file',
                                                                 os.path.expanduser('~') + '/Desktop')
        if fileName != "":
            QMessageBox.information(self, "File", fileName)

    # ファイルオープンダイアログの表示
    def openFile(self):
        (fileName, selectedFilter) = QFileDialog.getOpenFileName(self, 'Open file',
                                                                 os.path.expanduser('~') + '/Desktop')
        if fileName != "":
            QMessageBox.information(self, "File", fileName)

    # ファイルオープンダイアログ（複数選択可能）の表示
    def openFiles(self):
        (fileNames, selectedFilter) = QFileDialog.getOpenFileNames(self, 'Open files',
                                                                   os.path.expanduser('~') + '/Desktop')
        if 0 < len(fileNames):
            message = ""
            for name in fileNames:
                message += name
                message += ", "

            QMessageBox.information(self, "Files", message)

    # ディレクトリ選択ダイアログの表示
    def selectDirectory(self):
        dirName = QFileDialog.getExistingDirectory(self, 'Select Directory', os.path.expanduser('~') + '/Desktop')
        if dirName != "":
            QMessageBox.information(self, "Directory", dirName)

    # フォント選択ダイアログの表示
    def selectFont(self):
        (ok, font) = QFontDialog.getFont(QFont("MS UI Gothic"), self, "Select font")
        if ok:
            fontInfo = font.toString()
            QMessageBox.information(self, "Font", fontInfo)

    # 色選択ダイアログの表示
    def selectColor(self):
        color = QColorDialog.getColor(Qt.green, self)
        if color.isValid():
            name = color.name()
            QMessageBox.information(self, "RGB color", name)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    # 自作ダイアログをインスタンス化して表示
    ui = MyFirstDialog()
    ui.show()

    app.exec_()
