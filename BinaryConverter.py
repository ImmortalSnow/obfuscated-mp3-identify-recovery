# -*- coding: utf-8 -*-
"""
Created on Thu Dec 01 16:07:04 2016

@author: Paul Flack

Loaded as part of my Honours Project, do not use seperately
"""

TRACE=True


            
def StringConversion(hexString):
#    converts a string of hex bytes to binary
    BinaryString = ''
    for hexByte in hexString:
        BinaryByte = ('{0:08b}'.format(ord(hexByte)))
        BinaryString = BinaryString + BinaryByte
    return BinaryString
    
def main():
    exit

if __name__ == '__main__':
    if TRACE: print '[S] BinaryConverter Module called as script, calling main()'
    main()
else:
    if TRACE: print '[L] BinaryConverter Module imported as library, not calling main'