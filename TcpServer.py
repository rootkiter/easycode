#!/bin/python
###############################################
# File Name : TcpServer.py
#    Author : rootkiter
#    E-mail : rootkiter@rootkiter.com
#   Created : 2017-10-19 05:22:01 PDT
###############################################


import SocketServer

class TcpHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            self.request.sendall(data.upper())

#// remember recode here
class TcpServer:
    def __init__(self):
        pass

import sys
if __name__=='__main__':
    HOST,PORT = "localhost", 5007

    server = SocketServer.ThreadingTCPServer((HOST,PORT), TcpHandler)

    server.serve_forever()
