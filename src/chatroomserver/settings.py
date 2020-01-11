#coding:utf-8
# 定义一些各个文件都需要的变量
import os
# 项目根目录
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(PROJECT_DIR, "img")
SERVER_ADDR = {"IP": "127.0.0.1", "PORT": 7799}
# 用户给服务器发的包的类型
USER_FLAG = {"register": 0, "login": 1, "talk": 2, "gift": 3, "inroom": 4, "outroom": 5, "close": 6}
