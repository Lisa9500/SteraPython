import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *
from OpenDialog import *

import glob
# import chardet
from chardet.universaldetector import UniversalDetector

class MyForm(QMainWindow):
    triggered = pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.actiionOpen.triggered.connect(self, openDialog)
        self.ui.actionPage_Layout.triggered.connect(self, openDialog)
        self.ui.actionFormat_Box.triggered.connect(self, openDialog)
        self.ui.actionCut.triggered.connect(self, openDialog)
        self.ui.actionCopy.triggered.connect(self, openDialog)

    def detect_character_code(pathname):
        files_code_dic = {}
        detector = UniversalDetector()
        for file in glob.glob(pathname):
            with open(file, 'rb') as f:
                detector.reset()
                for line in f.readlines():
                    if detector.done:
                        break
                    detector.close()
                    files_code_dic[file] = detector.result['encoding']
        return files_code_dic

    def openDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'OpenFile', '/home')
        files_code = detect_character_code(pathname)
        # path='.' filename='*' extension='txt' pathname=path+filename+'.'+exyension
        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.read()
                self.ui.textEdit.setText(data)

    def layoutmessage(self):

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    # sys.exit(app.exec_())
    app.exec_()

