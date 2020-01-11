#coding:utf-8
import select
import socket
import Queue

# select模型：只有两种事件（读事件和写事件），读事件包含对方的connect，send，close；写事件是我们的send

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)  # 设置非阻塞套接字

# 设置多路复用
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 9898)
server.bind(server_address)

server.listen(10)

# 监听套接字，对方的connect对我们的套接字来说也是读事件到来
inputs = [server]

# 我们要写的socket
outputs = []

# 放入阻塞的队列QUEUE
message_queues = {}

# 超时时间，暂时不用
timeout = 400

while inputs:
    print u"等待下一个事件的到来"
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    for s in readable:    # 读事件到来，包含对方connect，send和close或异常退出
        if s is server:   # 如何是对方connect
            connection, client_address = s.accept()
            print u"欢迎到来", client_address
            connection.setblocking(0)
            inputs.append(connection)   # 加入已经连上的某个客户端的套接字
            message_queues[connection] = Queue.Queue()  # 给该套接字对应一个发送消息的队列
        else:  # 对方的send或者对方的close或者异常退出
            try:
                data = s.recv(1024)
                if data: # 对方send
                    print " received ", data, "from ", s.getpeername()
                    message_queues[s].put(data)
                    if s not in outputs:
                        outputs.append(s)  # 触发写事件
                else:  # 对方close
                    print u"对方关闭", client_address
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    del message_queues[s]  # 移除消息队列
            except:  # 异常退出
                print u"客户端异常退出", client_address
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del message_queues[s]  # 移除消息队列

    for s in writable:  # 写事件
        try:
            next_msg = message_queues[s].get_nowait()
        except Queue.Empty:
            print " ", s.getpeername(), u'空队列'
            outputs.remove(s)
        else:
            print u" 发送 ", next_msg, u" 到 ", s.getpeername()
            s.send(next_msg)

    for s in exceptional:
        print " 异常情况 ", s.getpeername()
        inputs.remove(s)    # 停止监听
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queues[s]  # 移除消息队列