"""
char room
env:python3.7
socket udp & fork exc
"""
import os
import string
import sys
from socket import *

ADDR = ("176.17.111.34", 9420)


def send_msg(s, name):
    while True:
        try:
            text = input('>>')
        except KeyboardInterrupt:
            text = "quit"
        if text.strip() == "quit":
            msg = "Q " + name
            s.sendto(msg.encode(), ADDR)
            sys.exit("退出聊天群")
        msg = "C " + name + ' ' + text
        s.sendto(msg.encode(), ADDR)
    pass


def recv_msg(s):
    while True:
        data, addr = s.recvfrom(4096)
        if data.decode() == "EXIT":
            sys.exit()
        print('\033[1;34m %30s \033[0m' % data.decode() + "\n>>",end='')
    pass


def is_legality(name):
    for i in name:
        if i in string.whitespace+string.punctuation:
            return True
    return False


def char_client():
    s = socket(AF_INET, SOCK_DGRAM, 0)

    while True:
        name = input('请输入你的昵称>>')
        if is_legality(name):
            print('用户名不合法')
            continue
        msg = 'L ' + name
        s.sendto(msg.encode(), ADDR)
        data, addr= s.recvfrom(1024)
        if data.decode() == 'OK':
            print('你已经进入聊天室')
            break
        else:
            print(data.decode())
            continue

    pid = os.fork()
    if pid < 0:
        sys.exit("ERROR")
    elif pid == 0:
        send_msg(s, name)
    else:
        recv_msg(s)


if __name__ == '__main__':
    char_client()