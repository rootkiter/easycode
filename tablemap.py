#!/bin/python
###############################################
# File Name : tablemap.py
#    Author : rootkiter
#    E-mail : rootkiter@rootkiter.com
#   Created : 2017-03-21 12:39:09
###############################################

import json

class tablemap:
    def __init__(self):
        self.tableTitle=None

        self.title={}
        self.titlelist=[]

        self.itemnamelen=0
        self.itemlist = []

        self.item = {}

    def setTitle(self,title):
        self.tableTitle = title

    def additem(self,title,itemname,itemvalue):
        if(title not in self.title):
            self.title[title]=len(title)
            self.titlelist.append(title)
        if(itemname not in self.item):
            self.item[itemname] = {}
            self.itemlist.append(itemname)
        self.item[itemname][title]=str(itemvalue)


        valueMaxLen = 0
        if len(str(itemvalue).split("\n")) > 0:
            valueMaxLen = max([len(i)+2 for i in str(itemvalue).split("\n")])

        if(self.title[title] < valueMaxLen):
            self.title[title] = valueMaxLen
        if(len(itemname)+2 > self.itemnamelen):
            self.itemnamelen = len(itemname)+2
        return True

    def getTblen( self ):
        blenList = [self.itemnamelen]
        tblen    = self.itemnamelen
        for tname in self.title:
            blenList.append(self.title[tname])
            tblen+=self.title[tname]
        return tblen+len(blenList)-1


    def getFormatString( self, nameList, splitchr = '+' ):
        fmtList = ['',('%%-%ds' % self.itemnamelen)]
        for citem in nameList:
            item = citem
            if citem.startswith('-'):
                item = citem[1::]
            fmtList.append("%%-%ds" % self.title[item])
        fmtList.append('')
        return splitchr.join(fmtList)

    def getFormLine( self, nameList ):
        formFormat  = self.getFormatString (nameList, '+')
        formValue = ['-'*self.itemnamelen]
        for name in nameList:
            item = name
            if name.startswith('-'):
                item = name[1::]
            formValue.append('-'*self.title[item])
        return formFormat % tuple(formValue)

    def getTitleValue( self, nameList ):
        numstr = str(len(self.item))
        numoff = int((self.itemnamelen - len(numstr))/2)
        titleValue = [ ' '*(numoff) + numstr ]
        for item in nameList:
            name = item
            if item.startswith('-'):
                name = item[1::]
            tlen = self.title[name]
            off  = int((tlen - len(name)) / 2)
            titleValue.append(' '*(off)+name)
        return titleValue

    def getItemValueList( self, itemname, nameList ):
        valueList = [[" "+itemname]]
        maxline = 0
        for name in nameList:
            item = name
            reverse = False
            if name.startswith('-'):
                item=name[1::]
                reverse = True
            value = self.item[itemname][item]
            totlen = self.title[item]
            vlist = []
            countline = 0
            for line in value.split('\n'):
                off = 0
                if reverse :
                    off = totlen - len(line)-2
                vlist.append(' '*(off+1)+line)
                countline += 1
            valueList.append(vlist)
            if countline> maxline:
                maxline = countline
        return maxline,valueList

    def printMap(self,titleList=None):
        result = []
        if titleList == None:
            titleList = self.titlelist
        valueFormat = self.getFormatString(titleList, '|')
        formLine    = self.getFormLine(titleList)

        if self.tableTitle != None:
            spaceNum = self.getTblen()
            result.append("+"+spaceNum*'-'+"+")
            toff = int((spaceNum - len(self.tableTitle))/2)
            tformat = "|%%-%ds|" % spaceNum
            result.append(tformat % (toff*' '+self.tableTitle))
        result.append(formLine)
        result.append(valueFormat % tuple(self.getTitleValue( titleList )))
        result.append(formLine)
        formLineFlag = False
        for itemname in self.itemlist:
            if formLineFlag:
                result.append(formLine)
                formLineFlag = False
            lineNum, valueList = self.getItemValueList( itemname, titleList )
            for i in range(lineNum):
                curvalue = []
                for k in valueList:
                    if len(k)>i:
                        curvalue.append(k[i])
                    else:
                        curvalue.append(' ')
                result.append(valueFormat % tuple(curvalue))
            if lineNum>1:
                formLineFlag = True
        result.append(formLine)
        return "\n".join(result)

import sys
if __name__=='__main__':
    tbmap = tablemap()
    #tbmap.additem("title1",'item1',"Hello 1*1")
    #tbmap.additem("title2",'item1',"Hello 1*2 AAAAA")
    #tbmap.additem("title1",'item2',"Hello 2*1 BBBBB")
    #tbmap.additem("title2",'item2',"Hello 2*2")
    #'''
    #+-------+-----------------+-----------------+
    #|       |      title1     |      title2     |
    #+-------+-----------------+-----------------+
    #| item1 |       Hello 1*1 | Hello 1*2 AAAAA |
    #| item2 | Hello 2*1 BBBBB |       Hello 2*2 |
    #+-------+-----------------+-----------------+
    #'''
    #print (tbmap.printMap())
#############################################################
    #'''
    #+-------+-----------------+-----------------+
    #|       |      title2     |     title1      |
    #+-------+-----------------+-----------------+
    #| item1 | Hello 1*2 AAAAA | Hello 1*1       |
    #| item2 |       Hello 2*2 | Hello 2*1 BBBBB |
    #+-------+-----------------+-----------------+
    #'''
    #tbmap.setTitle("Hello Table")
    #print (tbmap.printMap(['title2','-title1']))

    payload = {
        "crc32": 0x3ad60a53,
        "cmd_code": 3,
        "duation": 10,
        "sip_low": 0,
        "sip_high": 0,
        "cmd_body":[{
            "dip": "1.1.1.1",
            "dport": 53,
            "domain": "dns.google.com",
            "atk_type": 4,
            "fake_sip": "10.0.0.1",
            "payload_size": 0x100
        }]
    }
    tbmap.setTitle("Hello Table")
    tbmap.additem("title1",'item2',"Hello 2*1 BBBBB")
    tbmap.additem("title2",'item2',"Hello 2*2")
    tbmap.additem("title1", "item1", "DNS")
    tbmap.additem("title2", "item1", json.dumps(payload, indent = 4))
    print(tbmap.printMap(['title2', 'title1']))
