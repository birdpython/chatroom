# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.setWindowModality(QtCore.Qt.NonModal)
        Form.setEnabled(True)
        Form.resize(471, 359)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.lineEdit_name = QtGui.QLineEdit(Form)
        self.lineEdit_name.setGeometry(QtCore.QRect(180, 70, 141, 31))
        self.lineEdit_name.setObjectName(_fromUtf8("lineEdit_name"))
        self.lineEdit_passwdone = QtGui.QLineEdit(Form)
        self.lineEdit_passwdone.setGeometry(QtCore.QRect(180, 130, 141, 31))
        self.lineEdit_passwdone.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_passwdone.setObjectName(_fromUtf8("lineEdit_passwdone"))
        self.lineEdit_passwdtwo = QtGui.QLineEdit(Form)
        self.lineEdit_passwdtwo.setGeometry(QtCore.QRect(180, 190, 141, 31))
        self.lineEdit_passwdtwo.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_passwdtwo.setObjectName(_fromUtf8("lineEdit_passwdtwo"))
        self.pushButton_register = QtGui.QPushButton(Form)
        self.pushButton_register.setGeometry(QtCore.QRect(180, 280, 141, 31))
        self.pushButton_register.setObjectName(_fromUtf8("pushButton_register"))
        self.label_name = QtGui.QLabel(Form)
        self.label_name.setGeometry(QtCore.QRect(70, 70, 72, 15))
        self.label_name.setObjectName(_fromUtf8("label_name"))
        self.label_passwdone = QtGui.QLabel(Form)
        self.label_passwdone.setGeometry(QtCore.QRect(70, 140, 72, 15))
        self.label_passwdone.setObjectName(_fromUtf8("label_passwdone"))
        self.label_passwdtwo = QtGui.QLabel(Form)
        self.label_passwdtwo.setGeometry(QtCore.QRect(70, 200, 72, 15))
        self.label_passwdtwo.setObjectName(_fromUtf8("label_passwdtwo"))
        self.label_bkimg = QtGui.QLabel(Form)
        self.label_bkimg.setGeometry(QtCore.QRect(0, 0, 471, 361))
        self.label_bkimg.setText(_fromUtf8(""))
        self.label_bkimg.setObjectName(_fromUtf8("label_bkimg"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton_register, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.click_register)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "海同即时通讯系统", None))
        self.pushButton_register.setText(_translate("Form", "注册", None))
        self.label_name.setText(_translate("Form", "用 户 名", None))
        self.label_passwdone.setText(_translate("Form", "密    码", None))
        self.label_passwdtwo.setText(_translate("Form", "确认密码", None))

