# -*- coding: utf-8 -*-
"""
Created on Thu Dec 01 16:07:04 2016

@author: ImmortalSnow

This script loads a file as binary, one byte at a time and sends it off to the rest of the project
"""

import sys
from binascii import hexlify

TRACE=True
#sys.argv.append('L:\Hons Year\Honours Project\Code\TestCases\MP3Test.mp3')

def fileReader(FileToRead):
    RecoveryData=[]
    with open(FileToRead, "rb") as hexFile:
        hexByte = hexlify(hexFile.read(1))
        while hexByte != '':
            RecoveryData.append(hexByte)
            hexByte = hexlify(hexFile.read(1))
    return RecoveryData
        
def StringRead(FileToRead):
    ##  Reads the entire file into memory as hex, used by other parts of the code
    with open(FileToRead,'rb') as hexFile:
        RecoveryData = hexlify(hexFile.read())
    return RecoveryData
    del RecoveryData
        
    
def main():
    if len(sys.argv) != 2:
        print 'Usage: ReadAsByte.py *Name of file to read*'
        print 'Please ensure you provide the name of the file you want to read'
    else:
        fileReader(sys.argv[1])
        
      
    
if __name__ == '__main__':
    if TRACE: print '[S] Recovery Module called as script, calling main()'
    main()
else:
    if TRACE: print '[L] Recovery Module imported as library, not calling main'