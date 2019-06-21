#!/bin/python
###############################################
# File Name : hexmap.py
#    Author : rootkiter
#    E-mail : rootkiter@rootkiter.com
#   Created : 2017-03-21 12:36:59
###############################################


class hexmap:
    def __init__(self,raw):
        self.raw_bytes=raw

    def __str__(self):
        (offset,hexdata,charbuf)=(0,"","")
        result="\n------------------------> Data <------------------------\n"
        for b in self.raw_bytes:
            if b>=33 and b<=126:
                charbuf+=chr(b)
            elif b==0:
                charbuf+='.'
            else:
                charbuf+="*"

            hexdata += "%02x" % (b)
            offset+=1
            i=(offset)%16
            if i==0:
                buf="0x%04x:\t%-48s\t|%-16s|" % ((offset-1)//16*16,hexdata,charbuf)
                result += buf+"\n"
                hexdata=""
                charbuf=""
            elif (i%8==0):
                hexdata+="  "
            else:
                hexdata+=" "
        if len(charbuf) > 0:
            buf="0x%04x:\t%-48s\t|%-16s|\n" % ((offset)//16*16,hexdata,charbuf)
        else:
            buf = ""
        result += buf
        result += "---------> packet size :hex(0x%x),ord(%d) <-----------" % (len(self.raw_bytes),len(self.raw_bytes))
        return result


if __name__=='__main__':
    testdata = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    '''
    0x0000  41 42 43 44 45 46 47 48  49 4a 4b 4c 4d 4e 4f 50    ABCDEFGHIJKLMNOP
    0x0010  51 52 53 54 55 56 57 58  59 5a                      QRSTUVWXYZ      
    -----> packet size :hex(0x1a),ord(26) <-------
    '''
    print(str(hexmap(testdata)))
