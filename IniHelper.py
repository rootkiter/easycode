#!/bin/python
###############################################
# File Name : IniHelper.py
#    Author : rootkiter
#    E-mail : rootkiter@rootkiter.com
#   Created : 2017-07-13 18:07:27
###############################################


import ConfigParser,os

IniHelperLogFunction=print

def LogFunction(tag,log):
    IniHelperLogFunction("[ %5s ] %s" % (tag,log))

def ResetLogFunction(function):
    IniHelperLogFunction = function

def LogError(log):
    LogFunction("Error",log)

class IniHelper:
    def __init__(self,configname,ext='config'):
        self.dirpath    = os.path.dirname(os.path.abspath(__file__))
        self.configname = configname
        self.ext        = ext
        self.handle     = ConfigParser.ConfigParser()

    def reset_dirpath(self,path):
        self.dirpath = path

    def saveconfig(self):
        try:
            filepath = os.path.join(self.dirpath,self.configname+"."+self.ext)
            self.handle.write(open(filepath,'w'))
        except Exception,e:
            LogError(str(e))

    def loadconfig(self):
        try:
            filepath = os.path.join(self.dirpath,self.configname+"."+self.ext)
            if(os.path.exists(filepath)):
                self.handle.read(filepath)
        except Exception,e:
            LogError(str(e))
    
    def set(self,section,key,value):
        self.loadconfig()
        if (section not in self.handle.sections()):
            self.handle.add_section(section)
        self.handle.set(section,key,str(value))
        self.saveconfig()

    def get(self,section,key):
        self.loadconfig()
        if(section not in self.handle.sections()):
            LogError("No section \""+section+"\"")
            return ""
        if(key not in self.handle.options(section)):
            LogError("No option \""+key+"\"")
            return ""
        return self.handle.get(section,key)
        
import sys
if __name__=='__main__':
    ini = IniHelper('test','ini')
    ini.set('section1','key1','300')
    ini.set('section1','key2','900')
    ini.set('section5','key9','900')
    print ini.get('section1','key2')
