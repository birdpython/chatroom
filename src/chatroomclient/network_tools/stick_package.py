# coding:utf-8
import json
import settings
from protocol_package import ptl_headerlen, bgpos_bodylen, bgpos_retention, bgpos_version

alldata = ""
def openpackage(sock):
    global alldata
    while True:
        if len(alldata) < ptl_headerlen:
            alldata += sock.recv(16)
            if not alldata:  # 收到服务器的套接字的close消息
                bodydata = {u"flag": settings.USER_FLAG["close"], u"content": "close"}
                return 0, bodydata  # 版本号已经没有意义随便设一个0
        else:
            print alldata[:ptl_headerlen]
            header = json.loads(alldata[:ptl_headerlen])  # 反序列化包头
            indexversion = header.find("V")
            version = header[bgpos_version:indexversion]  # 取出版本号
            indexbodylen = header.find("C")
            bodylen = int(header[bgpos_bodylen:indexbodylen])  # 取出包内容长度
            indexretention = header.find("R")
            retension = header[bgpos_retention:indexretention]  # 取出保留字段
            print "版本号，body长度，保留字段:", version, bodylen, retension
            break

    while True:
        if len(alldata) < ptl_headerlen + bodylen:
            alldata += sock.recv(1024)
            continue
        else:
            bodydata = json.loads(alldata[ptl_headerlen:(ptl_headerlen + bodylen)])
            print "body内容:", bodydata
            alldata = alldata[ptl_headerlen + bodylen:]
            print "多余部分:", alldata
            return version, bodydata
