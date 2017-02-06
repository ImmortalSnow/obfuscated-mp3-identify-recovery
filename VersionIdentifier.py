# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 00:44:16 2016

@author: ImmortalSnow
"""

import re, operator, sys
from binascii import hexlify

TRACE=True

def FrameID(FileToRead):
    ##  First dictionary is that of known possible permutations of how a frame header can start, this is determined from the first 16 bits of a frame header:
        ##  11 bits are sync header
        ##  2 bits are version identifier
        ##  2 bits are layer identifier
        ##  Final bit is the protection bit, defining if the frame has a CRC or not
    ##  An MP3 can be version 1 or 2, will always be layer 3, and will be always protected or unprotected, with a CRC
    KnownVersionID=['fffa','fffb','fff2','fff3']
    ##  Determines what each combination amounts to
    versions={'fffa':'Version 1, unprotected',
              'fffb':'Version 1, protected',
              'fff2':'Version 2, unprotected',
              'fff3':'Version 2, protected'}
    first={}
    count={}
    
    try:
        for each in KnownVersionID:
            first.setdefault(each, min([m.start() for m in re.finditer(each, FileToRead)]))
            count.setdefault(each, len([m.start() for m in re.finditer(each, FileToRead)]))
    
        if min(first.iteritems(), key=operator.itemgetter(1))[0] == max(count.iteritems(), key=operator.itemgetter(1))[0]:
            if max(count.iteritems(), key=operator.itemgetter(1))[0] in versions and min(first.iteritems(), key=operator.itemgetter(1))[0] in versions:
                return versions[min(first.iteritems(), key=operator.itemgetter(1))[0]]
        else:
            return 'File does not seem to be an MP3 file'
    except ValueError:
        return 'File does not seem to be an MP3 file'

def main():
#    sys.argv.append('L:/Hons Year/Honours Project/Code/TestCases/MP3Test.mp3')
#    sys.argv.append('L:/Hons Year/Honours Project/Code/TestCases/MP3TestObf.jpg')
#    sys.argv.append('L:/Hons Year/Honours Project/Code/TestCases/anigif_enhanced-15536-1460647028-14.mp4')
#    sys.argv.append('L:/Hons Year/Honours Project/Code/TestCases/1MrY0X.gif')
    if len(sys.argv) != 2:
        print 'Usage: VersionIdentifier.py *Name of file to identify*'
        print 'Please ensure you provide the name of the file whose version you want to identify'
    else:
        with open(sys.argv[1], 'rb') as ReadFile:
            RecoveryData = hexlify(ReadFile.read())
        VersionID = FrameID(RecoveryData)
        print VersionID
    
if __name__ == '__main__':
    if TRACE: print '[S] VersionIdentifier called as script, calling main()'
    main()
else:
    if TRACE: print '[L] VersionIdentifier imported as library, not calling main'
