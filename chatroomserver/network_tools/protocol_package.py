#coding:utf-8
import json
ptl_servervesion = "1.0"
ptl_headerlen = 28
ptl_retention = ""
ptl_header = "VVVVVVCCCCCCCCCCRRRRRRRRRR"
ptl_body = {"flag": None, "content": None}
bgpos_version = 0
bgpos_bodylen = 6
bgpos_retention = 16

def ptl_dealheader(replacebodylen):
    header = ptl_header
    header = header[0:bgpos_version] + ptl_servervesion + header[bgpos_version + len(ptl_servervesion):]
    header = header[0:bgpos_bodylen] + replacebodylen + header[bgpos_bodylen + len(replacebodylen):]
    header = header[0:bgpos_retention] + ptl_retention + header[bgpos_retention + len(ptl_retention):]
    return json.dumps(header)

def ptl_dealbody(body):
    return json.dumps(body)

def closepackage(body):
    body = ptl_dealbody(body)
    header = ptl_dealheader(str(len(body)))
    return header + body


'''
总纲：协议包（package）由包头(header)和包内容(body)组成

一：协议包包头（header）说明
1.说明：
协议包包头（header)共占用28个字符，协议包头包含有版本号和内容长度值以及保留字段
其中版本号占6个字符（以V为补充识别结束）
内容长度值占10个字符（以C为补充识别结束）
保留字段值占10个字符（以R为补充识别结束）
注意对包头json序列化后，会多出两个引号，所以包头的总长度为28（是个固定值）

2.模型：
header = "VVVVVVCCCCCCCCCCRRRRRRRRRR"
其中V代表实际版本号，值自己确定但要以V结束；C代表包内容（body)实际长度值，值自己确定但要以C结束；R代表保留字段，值自己确定但要以R结束；

3.样例：
header = "1.0VVV78CCCCCCCCRRRRRRRRRR" 。我们自己组成包头（header)共26个字符，其中版本号为"1.0"，包内容（body）长度为"78"，保留字段为""。

4.注意事项
对header序列化后为：'"1.0VVV78CCCCCCCCRRRRRRRRRR" '   共28个字符

二：协议包内容（body）说明：
1.说明：
其中内容（body）是一个字典，里面含有两个元素：第一个元素是发送的内容类型，第二个元素是发送的有效内容。

2.模型：
body = {"flag":None, "content":None}
其中"flag"键对应的值是发送的body的类型，"content"对应的值是发送的有效内容。

3.客户端发送样例：
{"flag":"register", "content":{"name":"钟河东", "passwd":"11"}} #注册包的body
{"flag":"login", "content":{"name":"钟河东", "passwd":"11"}}    #登录包的body
{"flag":"inroom", "content":name}                               #进入聊天室的body
{"flag":"outroom", "content":name}                              #离开聊天室的body
{"flag":"talk", "content":"hello byebye"}                       #聊天包的body
{"flag":"gift", "content":["1", "3"]}                           #礼物包的body

礼物包说明："0"代表花；"1"代表汽车；"2"代表火箭；"3"代表美女。
{"flag":"close", "content":"0"}                                 #客户端应用层关闭
客户端应用层关闭说明："0"代表聊天室关闭；"1"代表登录框关闭
"0"聊天室关闭，我们认为是登录后的用户关闭，服务器需要在登录用户列表删除该用户（包含套接字和用户名）
"1"登录框关闭，我们认为用户没有登录，只是关闭套接字，服务器只需要关闭套接字。
flag代表协议包内容（body）的类型：flag值register代表注册，flag值login代表登录，
flag值talk代表聊天，flag值gift代表送礼物，flag值close代表客户端关闭


4.服务器端发送样例
服务器端对客户端发来的协议包内容（body）的flag是"login"的包内容（body）
重组为{"flag":"login", "content":status}
例如：对客户端发来的协议包内容（body)：{"flag":"login", "content":{"name":"钟河东", "passwd":"11"}} 
登录成功的话，重组为：{"flag":"login", "content":"0"} 
登录密码失败，重组为：{"flag":"login", "content":"1"} 
登录用户名失败，重组为：{"flag":"login", "content":"2"} 
重复登录，重组为：{"flag":"login", "content":"3"} 

服务器端对客户端发来的协议包内容（body）的flag是"inroom"的包内容（body）
重组为{"flag":"inroom", "content":{u"inname": inname, u"allnames": allnames}}
例如：对客户端发来的协议包内容（body)：{"flag":"inroom", "content":"钟河东"}
重组为：{"flag":"talk", "content":{"inname":"钟河东","allnames":["钟河东", "张浩", "张艺馨"]}

服务器端对客户端发来的协议包内容（body）的flag是"outroom"的包内容（body）
重组为{"flag":"outroom", "content":{u"outroom": inname, u"allnames": allnames}}
例如：对客户端发来的协议包内容（body)：{"flag":"outroom", "content":"钟河东"}
重组为：{"flag":"talk", "content":{"outroom":"钟河东","allnames":["钟河东", "张浩", "张艺馨"]}

服务器端对客户端发来的协议包内容（body）的flag是"talk"的包内容（body）
重组为{"flag":"talk", "content":{"name":name, "talk":talk}}
例如：对客户端发来的协议包内容（body)：{"flag":"talk", "content":"hello byebye"}
重组为：{"flag":"talk", "content":{"name":"钟河东","talk":"hello byebye"}

服务器端对客户端发来的协议包内容（body）的flag是"gift"的包内容（body）
重组为{"flag":"gift", {"content":{"name":name, "gift":gift}}
例如：对客户端发来的协议包内容（body)：{"flag":"gift", "content":["1", "3"]}
重组为：{"flag":"gift", "content":{"name":"钟河东","content":["1", "3"]}


注意事项：
flag为register的情况下自己写，还有服务器对用户管理写操作和注册用户写操作要加锁或者用其他解决方案
'''