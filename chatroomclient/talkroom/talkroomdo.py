#coding:utf-8
import os
import settings
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import QString
import talkroom

class Talkroom(QtGui.QWidget):
    def __init__(self, client, myname):
        super(Talkroom, self).__init__()
        self.__client = client  # 窗口管理类
        self.__myname = myname  # 当前进入聊天室的我自己的名字
        self.__giftmap = {"0": "flower.png", "1": "car.png", "2": "rocket.png", "3": "beauty.gif"}
        self.__giftshowname = {"flower.png": u"鲜花", "car.png": u"跑车", "rocket.png": u"火箭", "beauty.gif": u"美女"}
        self.__closestatus = "0"        # 协议包body的content的关闭值

        self.__talkroombkimg = "bk.gif"  # 聊天室框背景图片名称
        self.__talkroomimgdir = os.path.join(settings.IMG_DIR, "talkroomimg")  # 聊天室框图片根目录
        self.__talkroombkimgpath = os.path.join(self.__talkroomimgdir, self.__talkroombkimg)
        self.initui()  # 初始化聊天室界面
        self.inroom()  # 登录成功发个包告诉聊天室成员我进来了

    def initui(self):
        self.__talkroomui = talkroom.Ui_Form()
        self.__talkroomui.setupUi(self)
        self.settalkroomlogo()
        self.setwindowsize()
        self.pushbtnextend()
        self.popup()
        self.settalkroombkimg()

    # 让控件层级大于背景图片
    def popup(self):
        self.__talkroomui.textEdit_talkuser.raise_()
        self.__talkroomui.textEdit_talkall.raise_()
        self.__talkroomui.lineEdit_talk.raise_()
        self.__talkroomui.pushButton_talksend.raise_()
        self.__talkroomui.label_giftimg.raise_()
        self.__talkroomui.checkBox_flower.raise_()
        self.__talkroomui.checkBox_flower.raise_()
        self.__talkroomui.checkBox_car.raise_()
        self.__talkroomui.checkBox_rocket.raise_()
        self.__talkroomui.checkBox_beauty.raise_()
        self.__talkroomui.pushButton_giftsend.raise_()
        self.__talkroomui.label_giftuser.raise_()
        self.__talkroomui.label_username.raise_()

    def pushbtnextend(self):
        self.__talkroomui.pushButton_giftsend.setStyleSheet(
            "font: bold; font-size:20px; color: white; background-color: green")

        self.__talkroomui.pushButton_talksend.setStyleSheet(
            "font: bold; font-size:20px; color: white; background-color: green")

    # 设置窗口固定大小
    def setwindowsize(self):
        self.setFixedSize(self.width(), self.height())

    # 设置聊天框logo
    def settalkroomlogo(self):
        self.setWindowIcon(QIcon(settings.LOGO_PATH))

    # 设置登录框背景图片
    def settalkroombkimg(self):
        movie = QMovie(self.__talkroombkimgpath)
        self.__talkroomui.label_bkimg.setMovie(movie)
        self.__talkroomui.label_bkimg.setScaledContents(True)  # gif自适应lable大小
        movie.start()

    # 统一聊天室窗口发送消息给窗口管理类
    def writetoclient(self, body, action):
        if not self.__client.readywrite(body):
            QMessageBox.information(None, u"错误警告", action)

    # 发送关闭聊天室信息
    def closeEvent(self, event):
        self.outroom()      # 先告诉大家离开房间
        body = {"flag": settings.USER_FLAG["close"], "content": self.__closestatus}
        self.writetoclient(body, u"异常退出")
        self.__client.nowwindow[0] = "over"

    # 发送离开房间信息
    def outroom(self):
        body = {"flag": settings.USER_FLAG["outroom"], "content": self.__myname}
        self.writetoclient(body, u"异常离开聊天室")

    # 发送进入房间信息
    def inroom(self):
        self.__talkroomui.label_username.setText(QString(u"我是：" + self.__myname))
        body = {"flag": settings.USER_FLAG["inroom"], "content": self.__myname}
        self.writetoclient(body, u"进入聊天室失败")

    # 发送聊天信息
    def clicked_talksend(self):
        talkcontent = unicode(self.__talkroomui.lineEdit_talk.text())
        body = {"flag": settings.USER_FLAG["talk"], "content": talkcontent}
        self.writetoclient(body, u"发送聊天信息失败")
        self.__talkroomui.textEdit_talkall.append(QString(u"我说:" + talkcontent))

    # 发送礼物处理
    def getgift(self):
        flowercheck = self.__talkroomui.checkBox_flower.isChecked()
        carcheck = self.__talkroomui.checkBox_car.isChecked()
        rocketcheck = self.__talkroomui.checkBox_rocket.isChecked()
        beautycheck = self.__talkroomui.checkBox_beauty.isChecked()
        return [flowercheck, carcheck, rocketcheck, beautycheck]

    # 发送礼物
    def clicked_giftsend(self):
        giftcontent = []
        gifts = self.getgift()
        for index, gift in enumerate(gifts):
            if gift:
                giftcontent.append(str(index))

        body = {"flag": settings.USER_FLAG["gift"], "content": giftcontent}
        self.writetoclient(body, u"发送礼物失败")

    # 接收礼物处理
    def dealGift(self, content):
        giftname = content[u"gift"]
        giftuser = content[u"name"]
        self.__talkroomui.label_giftuser.setText(QString(giftuser + u"送了一个"
                                                        + self.__giftshowname[self.__giftmap[giftname]]))

        # 支持gif
        movie = QtGui.QMovie(os.path.join(self.__talkroomimgdir, self.__giftmap[giftname]))
        self.__talkroomui.label_giftimg.setMovie(movie)
        self.__talkroomui.label_giftimg.setScaledContents(True)  # gif自适应lable大小
        movie.start()


    # 接收进入房间处理
    def dealInroom(self, content):
        self.__talkroomui.textEdit_talkuser.clear()
        for loginuser in content[u"allnames"]:   # 刷新登录用户列表
            self.__talkroomui.textEdit_talkuser.append(QString(loginuser))
        self.__talkroomui.textEdit_talkall.append(QString(u"系统消息：欢迎" + content[u"inname"] + u"进入聊天室"))

    # 接收离开房间处理
    def dealOutroom(self, content):
        self.__talkroomui.textEdit_talkuser.clear()
        outstause = u"正常离开聊天室"
        try:content[u"allnames"].remove(content[u"outname"])  # 去除离开聊天室的用户
        except:outstause = u"崩溃离开聊天室"

        for loginuser in content[u"allnames"]:                # 刷新登录用户列表
            self.__talkroomui.textEdit_talkuser.append(QString(loginuser))
        self.__talkroomui.textEdit_talkall.append(QString(u"系统消息：" + content[u"outname"] + outstause))

    # 接收聊天信息处理
    def dealTalk(self, content):
        self.__talkroomui.textEdit_talkall.append(QString((content[u'name']) + u"说:" + (content[u'talk'])))
