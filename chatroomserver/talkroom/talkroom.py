#coding:utf-8

class TalkRoom(object):
    def __init__(self, server):
        self.__server = server

    '''服务器端对客户端发来的协议包内容（body）的flag是"inroom"的包内容（body）
        重组为{"flag":"inroom", "content":{u"inname": inname, u"allnames": allnames}}
        例如：对客户端发来的协议包内容（body)：{"flag":"inroom", "content":"钟河东"}
        重组为：{"flag":"talk", "content":{"inname":"钟河东","allnames":["钟河东", "张浩", "张艺馨"]}
    '''
    # 客户端进入房间处理
    def dealInroom(self, body):
        loginedusersname = []
        for loginuser in self.__server.getloginusers():
            loginedusersname.append(loginuser["name"])

        #重组inroom包
        body = {"flag": body[u"flag"], "content": {u"inname":body[u"content"], u"allnames":loginedusersname}}
        package = self.__server.closepackage(body)
        for user in self.__server.getloginusers():
            self.__server.readywrite(user["socket"], package)

    ''' 服务器端对客户端发来的协议包内容（body）的flag是"outroom"的包内容（body）
        重组为{"flag":"outroom", "content":{u"outname": outname, u"allnames": allnames}}
        例如：对客户端发来的协议包内容（body)：{"flag":"outroom", "content":"钟河东"}
        重组为：{"flag":"talk", "content":{"outname":"钟河东","allnames":["钟河东", "张浩", "张艺馨"]}
    '''
    # 客户端离开房间处理
    def dealOutroom(self, currentuser, body):
        loginedusersname = []
        for loginuser in self.__server.getloginusers():
            loginedusersname.append(loginuser["name"])

        # 重组outroom包
        body = {"flag": body[u"flag"], "content": {u"outname": body[u"content"], u"allnames": loginedusersname}}
        package = self.__server.closepackage(body)
        for user in self.__server.getloginusers():
            if user[u"name"] != currentuser[u"name"]:
                self.__server.readywrite(user[u"socket"], package)

    '''服务器端对客户端发来的协议包内容（body）的flag是"talk"的包内容（body）
       重组为{"flag": "talk", "content": {"name": name, "talk": talk}}
       例如：对客户端发来的协议包内容（body)：{"flag": "talk", "content": "hello byebye"}
       重组为：{"flag": "talk", "content": {"name": "钟河东", "talk": "hello byebye"}
    '''

    # 客户端发送聊天信息处理
    def dealTalk(self, currentuser, body):
        # 重组聊天包
        body = {"flag": body[u"flag"], "content": {u"name": currentuser[u"name"], u"talk": body[u"content"]}}
        package = self.__server.closepackage(body)
        for user in self.__server.getloginusers():
            if user[u"name"] != currentuser[u"name"]:
                self.__server.readywrite(user[u"socket"], package)

    '''
    服务器端对客户端发来的协议包内容（body）的flag是"gift"的包内容（body）
    重组为{"flag": "gift", {"content": {"name": name, "gift": gift}}
    例如：对客户端发来的协议包内容（body)：{"flag": "gift", "content": ["1", "3"]}
    重组为：{"flag": "gift", "content": {"name": "钟河东", "content": ["1", "3"]}
    '''
    # 客户端送礼物处理
    def dealGift(self, currentuser, body):
        #重组礼物包
        body = {"flag":body[u"flag"], "content":{u"name": currentuser[u"name"], u"gift": body[u"content"]}}
        package = self.__server.closepackage(body)
        for user in self.__server.getloginusers():
            self.__server.readywrite(user["socket"], package)