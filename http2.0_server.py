"""
1. 主要功能 :
【1】 接收客户端(浏览器)请求
【2】 解析客户端发送的请求
【3】 根据请求组织数据内容
【4】 将数据内容形成http响应格式返回给浏览器
2. 升级点 :
【1】 采用IO并发,可以满足多个客户端同时发起请求情况
【2】 做基本的请求解析,根据具体请求返回具体内容,同时满足客户端简单的非网页请求情况
【3】 通过类接口形式进行功能封装

3. 技术分析:
    1.tcp通信 基于http协议
    2.select 多路复用

4. 类的接口设计:
    1. 在用户角度考量
        * 能替用户完成的功能,尽可能完成
        * 不能替用户决定的属性,让用户传入
        * 功能不能替用户决定,让用户重写

    2. 确定用户怎么用,需要什么参数,使用方法
"""
from select import select
from socket import *

"""
httpseerver2.0
env:python3.6
io多路复用 tcp协议
"""


class HttpServer:
    """
    你好
    """
    def __init__(self, host='0.0.0.0', post=80, path='/home/tarena/html_file'):
        self.__host = host
        self.__post = post
        self.__path = path
        self.__address = (self.__host, self.__post)
        self.__rlist = []
        self.__wlist = []
        self.__xlist = []
        self.__create_socket()
        self.__bind()

    def __create_socket(self):
        self.__sockfd = socket()
        self.__sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        pass

    def __bind(self):
        self.__sockfd.bind(self.__address)

    def server_forever(self):
        self.__sockfd.listen(5)
        print("Listen the port %d" % self.__post)
        self.__rlist.append(self.__sockfd)
        while True:
            rs, ws, xs = select(self.__rlist, self.__wlist, self.__xlist)
            for r in rs:
                if r == self.__sockfd:
                    c, addr = r.accept()
                    self.__rlist.append(c)
                else:
                    self.__handle(r)
        pass

    def __handle(self, connfd):
        request = connfd.recv(4096)
        if not request:
            self.__rlist.remove(connfd)
            connfd.close()
            return

        request_line = request.splitlines()[0]
        info = request_line.decode().split(' ')[1]
        print(info)

        if info == '/' or info.split('.')[-1] == 'html':
            self.__get_html(connfd, info)
        else:
            self.__get_data(connfd, info)
        pass

    def __get_html(self, connfd, info):
        if info == '/':
            with open(self.__path + '/main.html', 'r') as f:
                data = f.read()
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type: text/html\r\n"
            response += "\r\n"
            response += data
            connfd.send(response.encode())
            return
        try:
            with open(self.__path + info, 'r') as f:
                http_response = f.read()
        except FileNotFoundError:
            response = "HTTP/1.1 404 NOT FOUNT\r\n"
            response += "Content-Type: text/html\r\n"
            response += "\r\n"
            response += "<h1>Sorry</h1>"
            connfd.send(response.encode())
        else:
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type: text/html\r\n"
            response += "\r\n"
            response += http_response
            connfd.send(response.encode())
        pass

    def __get_data(self, connfd, info):
        try:
            with open(self.__path + info, 'rb') as f:
                error_data = f.read()
        except FileNotFoundError:
            with open(self.__path + '/' + 'error.jpeg', 'rb') as f:
                error_data = f.read()
        else:
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type: image/jpeg\r\n"
            response += "\r\n"
            response = response.encode() + error_data
            connfd.send(response)
        pass


if __name__ == '__main__':
    HOST = '0.0.0.0'
    POST = 9420
    PATH = '/home/tarena/html_file'
    http = HttpServer(HOST, POST, PATH)
    http.server_forever()
