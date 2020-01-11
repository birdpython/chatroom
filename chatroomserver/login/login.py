#coding:utf-8
import os
import json


'''
1.loginusers 主线程管理的变量，内容为已经登录的用户。
格式为：[{"socket":socket, "name":name},....]
案例：[{"socket":sock1, "name":"钟河东"}, {"socket":sock2, "name":"张艺馨"}]

2.currentuser是当前线程的变量，内容为当前线程的用户（含有未登录和已登录）。
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
class Login(object):
    def __init__(self, server):
        self.__server = server
        self.__loginstate = {u"登录成功": "0", u"密码错误": "1", u"用户名错误": "2", u"重复登录": "3"}
        self.__friendsfile = "friends.txt"
        self.__friendsfilepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "friends")
        self.__friendsfilepath = os.path.join(self.__friendsfilepath, self.__friendsfile)

    # 判断用户提交的用户名是否在已登录名单中
    def isLogined(self, loginname):
        for user in self.__server.getloginusers():
            if loginname == user[u"name"]:
                return True
        return False

    # 处理客户端发来的登录信息
    def dealLoginxx(self, serversock, loginstatus, body):
        # 重组登录包
        body = {"flag": body["flag"], "content": loginstatus}
        package = self.__server.closepackage(body)
        self.__server.readywrite(serversock, package)

    # 处理客户端发来的登录信息
    def dealLoginyy(self, serversock, registeredusers, currentuser, body):
        for user in registeredusers:
            if body[u"content"][u"name"] == user[u"name"]:
                if body[u"content"][u"passwd"] == user[u"passwd"]:
                    print u"登录成功"  # 成功登录
                    currentuser[u"name"] = body[u"content"][u"name"]
                    self.__server.addloginuser(currentuser)  # 登录成功保存用户
                    self.dealLoginxx(serversock, self.__loginstate[u"登录成功"], body)
                    return
                else:
                    print u"密码错误"  # 用户名正确，密码错误
                    self.dealLoginxx(serversock, self.__loginstate[u"密码错误"], body)
                    return
        print u"用户名错误"
        self.dealLoginxx(serversock, self.__loginstate[u"用户名错误"], body)

    # 处理客户端发来的登录信息
    def dealLogin(self, serversock, currentuser, body):
        f = open(self.__friendsfilepath, "r+")
        registeredusers = json.loads(f.read())  # 已注册用户

        if not self.isLogined(body[u"content"][u"name"]):
            self.dealLoginyy(serversock, registeredusers, currentuser, body)
        else:
            self.dealLoginxx(serversock, self.__loginstate[u"重复登录"], body)
        f.close()
