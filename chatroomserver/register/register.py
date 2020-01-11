#coding:utf-8
import os
import json
import settings
import threading

'''
1.loginusers 主线程管理的变量，内容为已经登录的用户。
格式为：[{"socket":socket, "name":name},....]
案例：[{"socket":sock1, "name":"钟河东"}, {"socket":sock2, "name":"张艺馨"}]

2.currentuser是当前线程的变量，内容为当前线程的用户（还有未登录和已登录）。
格式为：{"socket":socket, "name":name}
未登录案例：{"socket":socket1, "name":None}
已登录案例：{"socket":socket1, "name":"钟河东"}

3.服务器端对客户端发来的协议包内容（body）的flag是"login"的包内容（body）
重组为{"flag":"login", "content":status}
例如：对客户端发来的协议包内容（body)：{"flag":"login", "content":{"name":"钟河东", "passwd":"11"}} 
登录成功的话，重组为：{"flag":"login", "content":"0"} 
登录密码失败，重组为：{"flag":"login", "content":"1"} 
登录用户名失败，重组为：{"flag":"login", "content":"2"} 
重复登录，重组为：{"flag":"login", "content":"3"} 

'''
class Register(object):
    def __init__(self, server):
        self.__server = server
        self.__registerstate = {u"注册成功": "0", u"用户名错误": "1", u"密码错误": "2", u"密码不一致": "3", u"重复注册": "4"}

        self.__friendsfilename = "friends.txt"  # 用户注册文件
        self.__friendsfiledir = os.path.join(settings.PROJECT_DIR, "friends")
        self.__friendsfilepath = os.path.join(self.__friendsfiledir, self.__friendsfilename)

    # 判断用户提交的用户名是否在已注册名单中
    def isRegistered(self, registername):
        for user in self.__server.getregisteredusers():
            if registername == user[u"name"]:
                return True
        return False

    # 把处理客户端注册的结果返回给客户端
    def sendRsttoClient(self, serversock, registerstatus, body):
        # 重组注册包
        body = {"flag": body["flag"], "content": registerstatus}
        package = self.__server.closepackage(body)
        self.__server.readywrite(serversock, package)

    # 检查客户端注册信息
    def checkRegister(self, serversock, registeredusers, body):
        print len(body['content']["name"])
        print body['content']["name"]
        if (len(body['content']["name"]) < 1) or (len(body['content']["name"]) > 12):
            self.sendRsttoClient(serversock, self.__registerstate[u"用户名错误"], body)
            return False
        if (len(body['content']["passwdone"]) < 1) or (len(body['content']["passwdone"]) > 12):
            self.sendRsttoClient(serversock, self.__registerstate[u"密码错误"], body)
            return False
        if body['content']["passwdone"] != body['content']["passwdone"]:
            self.sendRsttoClient(serversock, self.__registerstate[u"密码不一致"], body)
            return False
        for user in registeredusers:
            if body['content'][u"name"] == user[u"name"]:
                self.sendRsttoClient(serversock, self.__registerstate[u"重复注册"], body)
                return False
        self.sendRsttoClient(serversock, self.__registerstate[u"注册成功"], body)
        return True

    # 处理客户端发来的注册信息
    def dealRegister(self, lock, serversock, body):
        lock.acquire()
        f = open(self.__friendsfilepath, "r+")
        registeredusers = f.read()  # 刚开始文件不存在，读出来是空字符""而不是'""'，无法反序列化
        registeredusers = [] if not registeredusers else json.loads(registeredusers)  # 已注册用户
        if self.checkRegister(serversock, registeredusers,  body):  # 注册成功
            registeredusers.append({"name": body['content']['name'], "passwd": body['content']['passwdone']})
            f.seek(0)
            f.write(json.dumps(registeredusers))
        f.close()
        lock.release()
