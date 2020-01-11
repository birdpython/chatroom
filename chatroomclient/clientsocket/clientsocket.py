#coding:utf-8
'''
负责和服务器网络通信的客户端套接字
'''
import socket
import time
import settings
from PyQt4.QtCore import QThread
from PyQt4.QtCore import pyqtSignal
from network_tools.protocol_package import closepackage
from network_tools.stick_package import openpackage

class ClientSocket(QThread):
    signalOut = pyqtSignal(dict)
    def __init__(self, ip, port):
        super(ClientSocket, self).__init__()
        self.socketxx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip          # 服务器IP
        self.port = port      # 服务器端口

    # 关闭服务器
    def closexx(self):
        self.socketxx.close()

    # 发送服务器
    def sendxx(self, netok, body):
        package = closepackage(body)
        try:
            self.socketxx.sendall(package)
            netok[0] = True
        except:
            netok[0] = False

    # 连接服务器
    def connectxx(self, netok, trycount, trymaxcount):
        while trycount < trymaxcount:
            try:
                self.socketxx.connect((self.ip, self.port))
                netok[0] = True
                break
            except:
                trycount += 1
                netok[0] = False
                time.sleep(0.4)

    # 接收服务器端信息
    def recvxx(self):
        while True:
            try:
                version, body = openpackage(self.socketxx)  # 版本号暂时不用
            except:
                self.signalOut.emit({})  # 服务器异常关闭告诉客户端
                break                    # 底层协议退出
            if body[u"flag"] == settings.USER_FLAG["close"]:
                print u"正常关闭客户端套接字"
                self.closexx()
                break  # 退出循环
            if body[u"flag"] == settings.USER_FLAG["gift"]:
                giftbody = body
                for giftname in body[u"content"][u"gift"]:  # 礼物处理在子线程中，主线程中间隔时间是卡
                    giftbody[u"content"][u"gift"] = giftname
                    self.signalOut.emit(giftbody)
                    time.sleep(2)
            else:
                self.signalOut.emit(body)

    def run(self):
        self.recvxx()