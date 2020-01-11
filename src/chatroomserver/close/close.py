#coding:utf-8
class Close(object):
    def __init__(self, server):
        self.__server = server

    def dealClose(self, serversock, currentuser, body):
        closeflag = body["content"]
        if closeflag == "0":  # 聊天室内用户关闭
            self.__server.readyclose(serversock)
            self.__server.delloginuser(currentuser)
        if closeflag == "1":  # 未登录用户关闭
            self.__server.readyclose(serversock)

