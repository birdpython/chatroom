#coding:utf-8
import os
import settings
from PyQt4 import QtGui
from PyQt4.QtGui import *
import login
'''
对客户端发送的协议包内容（body)：{"flag":"login", "content":{"name":name, "passwd":passwd}} 
例子：{"flag":"login", "content":{"name":"钟河东", "passwd":"11"}} 
登录成功的话，服务器返回：{"flag":"login", "content":"0"} 
登录密码失败，服务器返回：{"flag":"login", "content":"1"} 
登录用户名失败，服务器返回：{"flag":"login", "content":"2"} 
重复登录，服务器返回：{"flag":"login", "content":"3"} 
'''
class Login(QtGui.QWidget):
    def __init__(self, client, myname):
        super(Login, self).__init__()
        self.__client = client      # 窗口管理类
        self.__myname = myname      # 窗口管理类需要知道的登录成功的名字
        self.__closestatus = "1"    # 登录框协议包body的点击关闭content
        self.__loginstate = {u"登录成功": "0", u"密码错误": "1", u"用户名错误": "2", u"重复登录": "3"}
        self.__loginupimg = "up.gif"  # 登录框上方图片名称
        self.__logindownimg = "down.png"  # 登录框上方图片名称
        self.__loginimgdir = os.path.join(settings.IMG_DIR, "loginimg")  # 登录框上方图片所在路径
        self.__loginupimgpath = os.path.join(self.__loginimgdir, self.__loginupimg)
        self.__logindownimgpath = os.path.join(self.__loginimgdir, self.__logindownimg)
        self.initui()

    def initui(self):
        self.__loginui = login.Ui_Form()
        self.__loginui.setupUi(self)
        self.setloginlogo()
        self.setloginupimg()
        self.setlogindowimg()
        self.setwindowsize()
        self.pushbtnextend()
        self.popup()

    # 设置button控件颜色
    def pushbtnextend(self):
        self.__loginui.pushButton_register.setStyleSheet(
            "font: bold; font-size:20px; color: white; background-color: green")

        self.__loginui.pushButton_login.setStyleSheet(
            "font: bold; font-size:20px; color: white; background-color: green")

    # 让控件层级大于downimg
    def popup(self):
        self.__loginui.label_passwd.raise_()
        self.__loginui.lable_username.raise_()
        self.__loginui.lineEdit_username.raise_()
        self.__loginui.lineEdit_passwd.raise_()
        self.__loginui.pushButton_register.raise_()
        self.__loginui.pushButton_login.raise_()

    # 设置窗口固定大小
    def setwindowsize(self):
        self.setFixedSize(self.width(), self.height())

    # 设置登录框上方gif
    def setloginupimg(self):
        movie = QMovie(self.__loginupimgpath)
        self.__loginui.label_upimg.setMovie(movie)
        self.__loginui.label_upimg.setScaledContents(True)  # gif自适应lable大小
        movie.start()

    # 设置登录框下方图片
    def setlogindowimg(self):
        self.__loginui.label_downimg.setPixmap(QPixmap(self.__logindownimgpath))
        self.__loginui.label_downimg.setScaledContents(True)  # 图片自适应lable大小

    # 设置登录框logo
    def setloginlogo(self):
        self.setWindowIcon(QIcon(settings.LOGO_PATH))

    # 统一登录窗口发送消息给窗口管理类
    def writetoclient(self, body, action):#
        if not self.__client.readywrite(body):
            QMessageBox.information(None, u"错误警告", action)

    # 处理登录窗口登录成功关闭和直接退出关闭
    def closeEvent(self, event):
        if self.__client.nowwindow[0] == "login":  # 关闭登录窗口，退出程序
            body = {"flag": settings.USER_FLAG["close"], "content": self.__closestatus}
            self.writetoclient(body, "关闭登录框发送信息失败")
            self.__client.nowwindow[0] = "over"    # 关闭登录框

    # 窗口登录成功
    def suc_login(self):
        self.__client.nowwindow[0] = "chatroom"  # 登录成功进入聊天室
        self.close()

    def dealLogin(self, content):
        if content == self.__loginstate[u"登录成功"]:
            self.suc_login()
        if content == self.__loginstate[u"密码错误"]:
            QMessageBox.information(self, u"错误警告", u"密码错误")
        if content == self.__loginstate[u"用户名错误"]:
            QMessageBox.information(self, u"错误警告", u"用户名错误")
        if content == self.__loginstate[u"重复登录"]:
            QMessageBox.information(self, u"错误警告", u"重复登录")

    # 点击注册
    def click_register(self):
        self.__client.nowwindow[0] = "register"  # 进入注册界面
        self.close()

    # 点击登录
    def click_login(self):
        username = unicode(self.__loginui.lineEdit_username.text())  # myt3把QString类型转为unicode
        passwd = unicode(self.__loginui.lineEdit_passwd.text())
        self.__myname[0] = username
        body = {"flag": settings.USER_FLAG["login"], "content": {"name": username, "passwd": passwd}}
        self.writetoclient(body, "登录信息发送失败")








