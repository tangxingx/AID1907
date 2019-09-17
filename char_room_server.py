"""
char room
env:python3.7
socket udp & fork exc
"""
import os
import string
import sys
from socket import *

ADDR = ("0.0.0.0", 9420)
USER = {}


def do_login(sock, name, addr):
    if name in USER or '管理员' in name:
        sock.sendto('\n用户名存在或不合法'.encode(), addr)
        return
    else:
        sock.sendto("OK".encode(), addr)

    msg = '\n欢迎%s加入群聊' % name
    for user_addr in USER.values():
        sock.sendto(msg.encode(), user_addr)
    USER[name] = addr


def do_char(sock, name, text):
    msg = "\n%s  :  %s" % (text, name)
    for user in USER:
        if user != name:
            sock.sendto(msg.encode(), USER[user])
    pass


def do_quit(sock, name):
    msg = "\n%s退出了群聊" % name
    for user in USER:
        if user == name:
            sock.sendto(b'EXIT', USER[user])
        else:
            sock.sendto(msg.encode(), USER[user])
    del USER[name]
    pass


def do_request(sock):
    while True:
        data, addr = sock.recvfrom(2048)
        request_type = data.decode().split(' ', 2)
        if request_type[0] == "L":
            do_login(sock, request_type[1], addr)
        elif request_type[0] == "C":
            do_char(sock, request_type[1], request_type[2])
        elif request_type[0] == "Q":
            do_quit(sock, request_type[1])



def char_server():
    s = socket(AF_INET, SOCK_DGRAM, 0)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR,0)
    s.bind(ADDR)
    print('服务器已启动…………')
    pid = os.fork()
    if pid < 0:
        sys.exit("Server Close")
    elif pid == 0:
        while True:
            text = input("Manager>>")
            msg = "C " + "管理员" + ' ' + text
            s.sendto(msg.encode(), ADDR)
        pass
    else:
        do_request(s)


if __name__ == '__main__':
    char_server()
