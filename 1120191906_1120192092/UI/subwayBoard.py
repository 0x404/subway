# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'subwayBoard.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(527, 453)
        self.imageBoard = QtWidgets.QLabel(Dialog)
        self.imageBoard.setGeometry(QtCore.QRect(100, 30, 311, 241))
        self.imageBoard.setObjectName("imageBoard")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.imageBoard.setText(_translate("Dialog", "TextLabel"))
