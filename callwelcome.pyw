import sys
from PyQt5.QtWidgets import QApplication, QDialog, QWidget
from welcomemsg import *
class MyForm(QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui =   Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.ClickMeButton.clicked.connect(self.dispmessage)

    def dispmessage(self):
        self.ui.labelMessage.setText("Hello "+ self.ui.lineUserName.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
