# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\programming\welcomemsg.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 180)
        self.labelEnterName = QtWidgets.QLabel(Dialog)
        self.labelEnterName.setGeometry(QtCore.QRect(20, 30, 121, 16))
        self.labelEnterName.setObjectName("labelEnterName")
        self.labelMessage = QtWidgets.QLabel(Dialog)
        self.labelMessage.setGeometry(QtCore.QRect(140, 80, 111, 16))
        self.labelMessage.setText("")
        self.labelMessage.setObjectName("labelMessage")
        self.lineUserName = QtWidgets.QLineEdit(Dialog)
        self.lineUserName.setGeometry(QtCore.QRect(160, 30, 221, 21))
        self.lineUserName.setObjectName("lineUserName")
        self.ClickMeButton = QtWidgets.QPushButton(Dialog)
        self.ClickMeButton.setGeometry(QtCore.QRect(150, 120, 93, 28))
        self.ClickMeButton.setObjectName("ClickMeButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.labelEnterName.setText(_translate("Dialog", "Enter your name."))
        self.ClickMeButton.setText(_translate("Dialog", "Click Me"))

