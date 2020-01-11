#coding:utf-8
import socket
import threading
import settings
from network_tools.stick_package import openpackage
from network_tools.protocol_package import closepackage
from register.register import Register
from login.login import Login
from talkroom.talkroom import TalkRoom
from close.close import Close
'''
author：老鸟python
version: 1.0
'''

'''
loginusers 主线程管理的变量，内容为已经登录的用户。
格式为：[{"socket":socket, "name":name},....]
案例：[{"socket":sock1, "name":"钟河东"}, {"socket":sock2, "name":"张艺馨"}]
'''

class ChatRoomServer(object):
    def __init__(self):
        self.loginusers = []             # 已登录用户（含套接字和用户名）
        self.serverlistensocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = settings.SERVER_ADDR["IP"]      # 服务器IP
        self.port = settings.SERVER_ADDR["PORT"]  # 服务器端口
        self.blockbuffercount = 5        # 协议栈阻塞中最大监听数
        self.login = Login(self)         # 客户端login处理类
        self.register = Register(self)   # 客户端register处理类
        self.talkroom = TalkRoom(self)   # 客户端聊天室处理类
        self.close = Close(self)         # 客户端关闭处理类
        self.lock = threading.Lock()     # 注册同时写文件加锁

    # 返回已登录用户
    def getloginusers(self):
        return self.loginusers

    # 客户端聊天室关闭，删除登录用户
    def delloginuser(self, user):
        self.loginusers.remove(user)

    # 客户端登录成功，加入该用户
    def addloginuser(self, user):
        self.loginusers.append(user)

    # 服务器端封包
    def closepackage(self, body):
        return closepackage(body)

    # 关闭和某个客户端通信的套接字
    def readyclose(self, serversock):
        serversock.close()

    # 发送协议包给某个客户端
    def readywrite(self, serversock, package):
        serversock.sendall(package)

    def readyread(self, serversock, addr):
        print u'新客户端连接到来：%s:%s' % addr
        currentuser = {u"socket": serversock, u"name": None}
        while True:
            try:
                version, body = openpackage(serversock)  # 服务器可以根据客户端version值做版本处理，在此我们暂不处理
                flag = body["flag"]
                if flag == settings.USER_FLAG["register"]:
                    self.register.dealRegister(self.lock, serversock, body)
                if flag == settings.USER_FLAG["login"]:
                    self.login.dealLogin(serversock, currentuser, body)
                if flag == settings.USER_FLAG["inroom"]:
                    self.talkroom.dealInroom(body)
                if flag == settings.USER_FLAG["outroom"]:
                    self.talkroom.dealOutroom(currentuser, body)
                if flag == settings.USER_FLAG["talk"]:
                    self.talkroom.dealTalk(currentuser, body)
                if flag == settings.USER_FLAG["gift"]:
                    self.talkroom.dealGift(currentuser, body)
                if flag == settings.USER_FLAG["close"]:
                    self.close.dealClose(serversock, currentuser, body)
                    print u"客户端正常退出"
                    break
            except:  # 客户端非正常关闭（任务管理器强制结束，直接关机等）
                try:
                    self.delloginuser(currentuser)  # 客户端异常退出,非正常关闭程序(有可能是在聊天室）需要异常聊天室名单
                    print u"聊天室异常退出"
                    body[u"flag"] = settings.USER_FLAG["outroom"]
                    body[u"content"] = currentuser[u"name"]
                    self.talkroom.dealOutroom(currentuser, body)  # 客户端异常退出,非正常关闭程序在聊天室，需要通知客户端去掉该用户
                except:
                    print u"非聊天室异常退出"
                serversock.close()
                print u"客户端异常退出"
                break

    def start(self):
        self.serverlistensocket.bind((self.ip, self.port))
        self.serverlistensocket.listen(self.blockbuffercount)
        print u'等待新的客户端连接...'
        while True:
            serversock, addr = self.serverlistensocket.accept()
            t = threading.Thread(target=self.readyread, args=(serversock, addr))
            t.start()

chatroomserver = ChatRoomServer()
chatroomserver.start()




