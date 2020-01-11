# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
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
        Form.resize(532, 402)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.lineEdit_username = QtGui.QLineEdit(Form)
        self.lineEdit_username.setGeometry(QtCore.QRect(170, 200, 221, 41))
        self.lineEdit_username.setObjectName(_fromUtf8("lineEdit_username"))
        self.lineEdit_passwd = QtGui.QLineEdit(Form)
        self.lineEdit_passwd.setGeometry(QtCore.QRect(170, 270, 221, 41))
        self.lineEdit_passwd.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_passwd.setObjectName(_fromUtf8("lineEdit_passwd"))
        self.lable_username = QtGui.QLabel(Form)
        self.lable_username.setGeometry(QtCore.QRect(90, 210, 72, 15))
        self.lable_username.setObjectName(_fromUtf8("lable_username"))
        self.label_passwd = QtGui.QLabel(Form)
        self.label_passwd.setGeometry(QtCore.QRect(90, 280, 72, 15))
        self.label_passwd.setObjectName(_fromUtf8("label_passwd"))
        self.pushButton_login = QtGui.QPushButton(Form)
        self.pushButton_login.setGeometry(QtCore.QRect(170, 340, 101, 41))
        self.pushButton_login.setObjectName(_fromUtf8("pushButton_login"))
        self.pushButton_register = QtGui.QPushButton(Form)
        self.pushButton_register.setGeometry(QtCore.QRect(290, 340, 101, 41))
        self.pushButton_register.setObjectName(_fromUtf8("pushButton_register"))
        self.label_upimg = QtGui.QLabel(Form)
        self.label_upimg.setGeometry(QtCore.QRect(0, 0, 531, 151))
        self.label_upimg.setText(_fromUtf8(""))
        self.label_upimg.setObjectName(_fromUtf8("label_upimg"))
        self.label_downimg = QtGui.QLabel(Form)
        self.label_downimg.setGeometry(QtCore.QRect(0, 150, 531, 251))
        self.label_downimg.setText(_fromUtf8(""))
        self.label_downimg.setObjectName(_fromUtf8("label_downimg"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton_register, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.click_register)
        QtCore.QObject.connect(self.pushButton_login, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.click_login)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "海同即时通讯系统", None))
        self.lable_username.setText(_translate("Form", "用户名：", None))
        self.label_passwd.setText(_translate("Form", "密  码：", None))
        self.pushButton_login.setText(_translate("Form", "登录", None))
        self.pushButton_register.setText(_translate("Form", "注册", None))

