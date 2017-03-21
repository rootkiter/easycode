#!/bin/python
###############################################
# File Name : MyThread.py
#    Author : rootkiter
#    E-mail : rootkiter@rootkiter.com
#   Created : 2017-03-21 12:50:05
###############################################

import threading

class MyThread(threading.Thread):
    def __init__(self,function):
        threading.Thread.__init__(self)
        self.runflag = False
        self.function = function
        self.args = {}

    def update(self,args):
        self.args = args

    def run(self):
        if(self.function == None):
            return 
        self.runflag = True
        while(self.runflag):
            import time
            time.sleep(0.1)
            if(self.args != None and 
                len(self.args)>=0):
                args = self.args
                self.args = {}
                self.function(args)

    def stop(self):
        self.runflag = False

def TestPrint(args):
    print str(args)

import sys
if __name__=='__main__':
    thread = MyThread(TestPrint)
    thread.start()
    import time
    for i in range(0,10):
        thread.update({"arg":i})
        time.sleep(0.2)
    thread.stop()
    '''
    $ python MyThread.py
    {'arg': 0}
    {'arg': 1}
    {}
    {'arg': 2}
    {}
    {'arg': 3}
    {}
    {'arg': 4}
    {}
    {'arg': 5}
    {}
    {'arg': 6}
    {}
    {'arg': 7}
    {}
    {'arg': 8}
    {}
    {'arg': 9}
    {}
    {}
    '''
