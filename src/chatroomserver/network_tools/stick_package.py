#coding:utf-8
import json
from protocol_package import ptl_headerlen, bgpos_bodylen, bgpos_retention, bgpos_version

alldata = ""
def openpackage(sock):
    global alldata
    while True:
        if len(alldata) < ptl_headerlen:
            alldata += sock.recv(100)
        else:
            header = json.loads(alldata[:ptl_headerlen])  # 反序列化包头
            indexversion = header.find("V")
            version = header[bgpos_version:indexversion]  # 取出版本号
            indexbodylen = header.find("C")
            bodylen = int(header[bgpos_bodylen:indexbodylen])  # 取出包内容长度
            indexretention = header.find("R")
            retension = header[bgpos_retention:indexretention]  # 取出保留字段
            break

    while True:
        if len(alldata) < ptl_headerlen + bodylen:
            alldata += sock.recv(1024)
            continue
        else:
            bodydata = json.loads(alldata[ptl_headerlen:(ptl_headerlen + bodylen)])
            print u"body内容:", bodydata
            alldata = alldata[ptl_headerlen + bodylen:]
            print u"多余部分:", alldata
            return version, bodydata
