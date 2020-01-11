#coding:utf-8
'''
author：老鸟python
version: 1.0
'''
import sys
import settings
from PyQt4 import QtGui
from PyQt4.QtCore import QObject
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import pyqtSignal

from clientsocket.clientsocket import ClientSocket
from register.registerdo import Register
from login.logindo import Login
from talkroom.talkroomdo import Talkroom

'''
窗口管理类：该类负责与底层套接字通信和管理窗口（登录，注册，聊天室）
1.与底层套接字通信采用消息通知机制
2.管理窗口形式为负责创建销毁窗口，以及分发底层套接字消息到各个窗口和把各个窗口消息转发到底层套接字
'''

class ChatRoomClient(QObject):
    sinConnect = pyqtSignal(list, int, int)  # 和实现连接服务器功能的协议层通信信号
    sinSend = pyqtSignal(list, dict)         # 和实现发送服务器功能的协议层通信信号
    sinClose = pyqtSignal(list)              # 和实现关闭服务器功能的协议层通信信号

    def __init__(self):
        super(ChatRoomClient, self).__init__()
        self.__app = QtGui.QApplication(sys.argv)  # 应用于所管理的窗口进入消息循环
        self.__trycount = 0
        self.__trymaxcount = 6  # 最多试验连接服务器端6次
        self.__clientsocket = ClientSocket(settings.SERVER_ADDR["IP"], settings.SERVER_ADDR["PORT"])
        self.__clientsocket.signalOut.connect(self.readyread)  # 接收协议层发来的消息

        self.sinConnect.connect(self.__clientsocket.connectxx)  # 发射信号到协议层去连接服务器
        self.sinSend.connect(self.__clientsocket.sendxx)        # 发射信号到协议层去发送数据到服务器同步
        self.sinClose.connect(self.__clientsocket.closexx)      # 发射信号到协议层去关闭服务器
        self.netok = [False]     # 底层套接字各种状态（connect, send, recv, close），需要底层套接字告知
        self.nowwindow = ["login"]  # 管理的窗口状态，需要其它窗口告知，默认值为第一个启动的窗口（登录窗口）
        self.myname = [""]       # 登录成功的名字有登录框告知，保存下来给聊天室窗口用

    # 进入注册界面
    def clientregister(self):
        self.__register = Register(self)
        self.__register.show()
        self.__app.exec_()

    # 进入登录界面
    def clientlogin(self):
        self.__login = Login(self, self.myname)
        self.__login.show()
        self.__app.exec_()

    # 进入聊天室界面
    def clienttalkroom(self):
        self.__talkroom = Talkroom(self, self.myname[0])
        self.__talkroom.show()
        self.__app.exec_()

    # 收到底层套接字recv（跨线程信号）
    def readyread(self, body):
        if not body:
            print u"服务器异常关闭"
            QMessageBox.information(None, u"错误警告", u"服务器异常关闭")
            self.sinClose.emit()
            return
        flag = body["flag"]
        if flag == settings.USER_FLAG["register"]:
            self.__register.dealRegister(body["content"])
        if flag == settings.USER_FLAG["login"]:
            self.__login.dealLogin(body["content"])
        if flag == settings.USER_FLAG["inroom"]:
            self.__talkroom.dealInroom(body["content"])
        if flag == settings.USER_FLAG["outroom"]:
            self.__talkroom.dealOutroom(body["content"])
        if flag == settings.USER_FLAG["talk"]:
            self.__talkroom.dealTalk(body["content"])
        if flag == settings.USER_FLAG["gift"]:
            self.__talkroom.dealGift(body["content"])

    # 发射同步信号到底层套接字close
    def readyclose(self):
        self.sinClose.emit()
        return True

    # 发射同步信号到底层套接字send
    def readywrite(self, body):
        self.sinSend.emit(self.netok, body)
        return self.netok[0]

    # 发射同步信号到底层套接字connect
    def readyconnect(self):
        self.sinConnect.emit(self.netok, self.__trycount, self.__trymaxcount)
        return self.netok[0]

    def managerwindow(self):  # 窗口管理负责管理登录框，注册框，聊天框的创建和销毁
        while True:
            if self.nowwindow[0] == "login":
                self.clientlogin()

            elif self.nowwindow[0] == "chatroom":  # 登录成功进入聊天室
                self.clienttalkroom()

            elif self.nowwindow[0] == "register":
                self.clientregister()
            else:
                break

    #运行客户端
    def run(self):
        if not chatroomclient.readyconnect():
            print "连接服务器失败"
            QMessageBox.information(None, u"错误警告", u"连接服务器失败")
            return
        else:
            self.__clientsocket.start()  # 子线程开启recv函数
            self.managerwindow()

if __name__ == '__main__':
    chatroomclient = ChatRoomClient()
    chatroomclient.run()


