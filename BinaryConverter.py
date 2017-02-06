# -*- coding: utf-8 -*-
"""
Created on Thu Dec 01 16:07:04 2016

@author: ImmortalSnow
"""

TRACE=True

##Takes a hex byte from the read script and converts it to binary
#def SingleByte(hexByte):
##Test Code - more than likely can be removed   
##    BinaryByte=[]
##    BinaryStringLen = len(hexByte)*4
##    BinaryString = ( bin(int(hexByte, 16))[2:] ).zfill(BinaryStringLen)
##    for Bit in BinaryString:        
##        BinaryByte.append(Bit)
##    return BinaryByte
#    while hexByte != '':
#            #Converts the hex byte to binary and returns
#            BinaryByte = ('{0:08b}'.format(ord(hexByte)))
#            return BinaryByte
            
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