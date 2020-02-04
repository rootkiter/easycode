#!/bin/python
###############################################
# File Name : tool.py
#    Author : rootkiter
#    E-mail : rootkiter@rootkiter.com
#   Created : 2020-02-04 19:11:46 CST
###############################################

import sys

def datadump(filepath, offset, size):
    print(filepath, offset, size)
    result = None
    with open(filepath, 'rb') as f:
        result = f.read()
    return result[offset: offset+size]

def patchfile(filepath, offset, patchdata, outfile):
    filedata = ""
    with open(filepath, 'rb') as f:
        filedata = f.read()

    result = filedata[:offset]
    result += patchdata
    result += filedata[offset+len(patchdata):]

    with open(outfile, 'wb') as f:
        f.write(result)

if __name__=='__main__':
    dumpdata = datadump("patch.bin", 0xa64, 0xc98-0xa64)
    patchfile("slient_b", 0xb610, dumpdata, "slient_b_python_dump")
