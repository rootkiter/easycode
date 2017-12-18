#!/bin/python
###############################################
# File Name : iolib.py
#    Author : rootkiter
#    E-mail : rootkiter@rootkiter.com
#   Created : 2017-12-17 22:04:05 PST
###############################################

import sys,socket,time,select

class FDPool:
    def __init__(self,bindconsole = True):
        self.rfdpool = {}
        self.wfdpool = {}

    def append_wfd(self,fd,on_event,args):
        self.wfdpool[fd] = [on_event,args]

    def append(self,fd,on_event,args):
        self.rfdpool[fd] = [on_event,args]

    def remove_wfd(self,fd):
        del self.wfdpool[fd]

    def remove(self,fd):
        try:
            del self.rfdpool[fd]
        except Exception as e:
            print str(e)

    def start(self):
        self.runflag = True
        while (self.runflag):
            rfdlist = list(self.rfdpool)
            wfdlist = list(self.wfdpool)
            exceplist = rfdlist+wfdlist
            readable,writeable,exceptional = select.select(rfdlist,wfdlist,exceplist,10)
            for exceptfd in exceptional:
                print "exceptfd"
                del self.rfdpool[exceptfd]

            for readfd in readable:
                on_event = self.rfdpool[readfd][0]
                args     = self.rfdpool[readfd][1]
                flags    = {"rflag":True}
                on_event(self,flags,args)

            for wfd in writeable:
                on_event = self.wfdpool[wfd][0]
                args     = self.wfdpool[wfd][1]
                flags    = {"wflag":True}
                on_event(self,flags,args)

    def stop(self):
        self.runflag = False

UNKNOWN_SOCKET = 0
SERVER_SOCKET  = 1
CLIENT_SOCKET  = 2
SERVER_CLIENT  = 3

class MSocket:
    def __init__(self,pool,Protocol,appendflag=True):
        def onselect(fdpool,flags,self):
            if("wflag" in flags):
                fdpool.remove_wfd(self.sock)
                fdpool.append(self.sock,onselect,self)
                return
            if(self.ntype == CLIENT_SOCKET or self.ntype == SERVER_CLIENT):
                try:
                    data = self.sock.recv(65545)
                    if(len(data)>0):
                        self.on_recv(self,data,self.on_recv_args)
                except Exception as e:
                    self.close()
                    fdpool.remove(self.sock)
            elif(self.ntype == SERVER_SOCKET):
                try:
                    client,client_addr = self.sock.accept()
                    clientsock = self.copy()
                    clientsock.sock = client
                    clientsock.ntype = SERVER_CLIENT
                    clientsock.on_accept(clientsock,clientsock.on_accept_args)
                    client.setblocking(0)
                    fdpool.append_wfd(client,onselect,clientsock)
                except Exception as e:
                    self.close()
                    fdpool.remove(self.sock)
                    
        def onrecv(self,data,args):
            print "call on_recv ",self.getDaddr(),self.getLaddr(),data,args

        def onaccept(self,args):
            print "call on_accept",self,args

        self.onselect = onselect
        self.protocol = Protocol
        self.fdpool   = pool
        self.on_accept      = onaccept
        self.on_accept_args = None
        self.on_recv  = onrecv
        self.on_recv_args =None
        if(Protocol == "TCP"):
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.ntype = 0

        if(appendflag):
            pool.append(self.sock,onselect,self)

    def getDaddr(self):
        return self.sock.getpeername()

    def getLaddr(self):
        return self.sock.getsockname()

    def copy(self):
        new_sock = MSocket(self.fdpool,self.protocol,False)
        try:
            new_sock.onselect       = self.onselect
            new_sock.on_recv        = self.on_recv
            new_sock.on_recv_args   = self.on_recv_args
            new_sock.ntype          = self.ntype
            new_sock.sock           = self.sock
            new_sock.on_accept      = self.on_accept
            new_sock.on_accept_args = self.on_accept_args
        except Exception as e:
            print str(e)
        return new_sock

    def server_init(self,port,maxlisten = 20):
        self.ntype = SERVER_SOCKET
        self.sock.setblocking(0)
        self.sock.bind(("0.0.0.0",port))
        self.sock.listen(maxlisten)

    def set_onaccept(self,onaccept,args):
        self.on_accept      = onaccept
        self.on_accept_args = args
    
    def connect(self,address):
        self.ntype = CLIENT_SOCKET
        self.sock.setblocking(0)
        self.sock.connect_ex(address)
    
    def set_onrecv(self,onrecv,args):
        self.on_recv      = onrecv
        self.on_recv_args = args

    def close(self):
        self.sock.close()

class mconsole:
    def __init__(self,pool,fd):
        def onselect(fdpool,flags,self):
            try:
                data = self.fd.readline()
                self.on_recv(self,data,self.on_recv_args)
            except Exception as e:
                fdpool.remove(self.sock)
                print str(e)
                    
        def onrecv(self,data,args):
            print "call on_recv ",data,args

        self.fd = fd
        self.on_recv = onrecv
        self.on_recv_args = None
        pool.append(self.fd,onselect,self)

    def set_onrecv(self,onrecv,args):
        self.on_recv      = onrecv
        self.on_recv_args = args

    def exit(self):
        pass

import sys
if __name__=='__main__':
    fdpool = FDPool()
    console = mconsole(fdpool,sys.stdin)

    client = MSocket(fdpool,"TCP")
    client.connect(("192.168.119.1",8888))
    server = MSocket(fdpool,"TCP")
    server.server_init(6666,20)
    fdpool.start()
