#coding:utf-8
import os
import settings
from PyQt4 import QtGui
from PyQt4.QtGui import *
import register

class Register(QtGui.QWidget):
    def __init__(self, client):
        self.__client = client
        super(Register, self).__init__()
        self.__registerstate = {u"注册成功": "0", u"用户名错误": "1", u"密码错误": "2", u"密码不一致": "3", u"重复注册": "4"}
        self.__registerbkimg = "bk.png"  # 注册框背景图片
        self.__registerbkimgdir = os.path.join(settings.IMG_DIR, "registerimg")  # 注册框所放图片根目录
        self.__registerbkimgpath = os.path.join(self.__registerbkimgdir, self.__registerbkimg)
        self.initui()  # 初始化注册框ui界面

    def initui(self):
        self.__registerui = register.Ui_Form()
        self.__registerui.setupUi(self)
        self.setwindowsize()
        self.popup()
        self.setregisterlogo()
        self.setrregisterbkimg()
        self.pushbtnextend()

    # 设置窗口固定大小
    def setwindowsize(self):
        self.setFixedSize(self.width(), self.height())

    def pushbtnextend(self):
        self.__registerui.pushButton_register.setStyleSheet(
            "font: bold; font-size:20px; color: white; background-color: green")

    def popup(self):  # 提升其它控件显示级别，让背景图片显示在最下层
        self.__registerui.lineEdit_name.raise_()
        self.__registerui.lineEdit_passwdone.raise_()
        self.__registerui.lineEdit_passwdtwo.raise_()
        self.__registerui.pushButton_register.raise_()
        self.__registerui.label_name.raise_()
        self.__registerui.label_passwdone.raise_()
        self.__registerui.label_passwdtwo.raise_()

    # 设置注册框logo
    def setregisterlogo(self):
        self.setWindowIcon(QIcon(settings.LOGO_PATH))

    # 设置注册框背景
    def setrregisterbkimg(self):
        movie = QMovie(self.__registerbkimgpath)
        self.__registerui.label_bkimg.setMovie(movie)
        self.__registerui.label_bkimg.setScaledContents(True)  # gif自适应lable大小
        movie.start()

    def closeEvent(self, event):
        self.__client.nowwindow[0] = "login"  # 注册关闭或注册成功

    # 窗口注册成功
    def suc_register(self):
        self.close()  # 该函数会调用closeEvent函数

    # 统一注册窗口发送消息给窗口管理类
    def writetoclient(self, body, action):
        if not self.__client.readywrite(body):
            QMessageBox.information(None, u"错误警告", action)

    def dealRegister(self, content):
        if content == self.__registerstate[u"注册成功"]:
            self.suc_register()
        if content == self.__registerstate[u"用户名错误"]:
            QMessageBox.information(self, u"错误警告", u"用户名长度请大于1小于12")
        if content == self.__registerstate[u"密码错误"]:
            QMessageBox.information(self, u"错误警告", u"密码长度请大于1小于12")
        if content == self.__registerstate[u"密码不一致"]:
            QMessageBox.information(self, u"错误警告", u"两次密码不一致")
        if content == self.__registerstate[u"重复注册"]:
            QMessageBox.information(self, u"错误警告", u"重复注册")

    def checkregister(self, username, passwdone, passwdtwo):  # 客户端检查
        if len(username) <= 0 or len(username) > 12:
            return u"用户名要大于0小于等于12"
        if len(passwdone) <= 0 or len(passwdone) > 12:
            return u"密码要大于0小于等于12"
        if passwdone != passwdtwo:
            return u"两次密码不一致"
        return None

    # 点击提交注册
    def click_register(self):
        username = unicode(self.__registerui.lineEdit_name.text())  # myt3把QString类型转为unicode
        passwdone = unicode(self.__registerui.lineEdit_passwdone.text())
        passwdtwo = unicode(self.__registerui.lineEdit_passwdtwo.text())
        errormessge = self.checkregister(username, passwdone, passwdtwo)
        if errormessge != None:
            QMessageBox.information(self, u"错误警告", errormessge)
            return
        body = {"flag": settings.USER_FLAG["register"], "content": {"name": username, "passwdone": passwdone, "passwdtwo": passwdtwo}}
        self.writetoclient(body, "注册信息发送失败")


    