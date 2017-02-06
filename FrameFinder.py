# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 21:30:04 2016
@author: ImmortalSnow
"""

TRACE=True


from VersionIdentifier import FrameID
import time, re, sys, FirstFrame, SecondaryFrames, os, ReadAsByte, ssdeep

def mp3_check(RecoveryData,RecoveryFile):
    frame_count = 0
    versions={'Version 1, unprotected':'fffa',
              'Version 1, protected':'fffb',
              'Version 2, unprotected':'fff2',
              'Version 2, protected':'fff3'}
    FileToRead = ReadAsByte.StringRead(RecoveryData)
    VID = FrameID(FileToRead)
    if VID in versions:
        Version = versions[VID]
        frame_count=find_frames(FileToRead,Version,frame_count,RecoveryFile)
        return frame_count
    elif VID == 'File does not seem to be an MP3 file':
       return 'File does not seem to be an MP3 file'
    
        
        
def find_frames(FileToRead, Version, frame_count, RecoveryFile):
    strt_frame = min([m.start() for m in re.finditer(Version, FileToRead)])
    last_indx = max([m.start() for m in re.finditer(Version, FileToRead)])
    while frame_count == 0:
        nxt_frame = FirstFrame.Frame(FileToRead,strt_frame, RecoveryFile)
        frame_count += 1
    while nxt_frame < last_indx:
        if FileToRead[nxt_frame: (nxt_frame +4)] == Version:
            nxt_frame = SecondaryFrames.Frame(FileToRead, nxt_frame, RecoveryFile)
            frame_count += 1
        ##On occasion, it has been noted that the padding bit may be set, but no padding is seen in the file.
        #In these instances, the figures for each frame are thrown off slightly.
        #To get round this, i have ibcluded code that will adjust the frame header retrieval by one byte,
        ## forwards or backwards, as needed to recover the correct frame
        elif FileToRead[(nxt_frame-2): (nxt_frame +2)] == Version:
            nxt_frame = SecondaryFrames.Frame(FileToRead, (nxt_frame-2), RecoveryFile)
            frame_count += 1
        elif FileToRead[(nxt_frame+2): (nxt_frame +6)] == Version:
            nxt_frame = SecondaryFrames.Frame(FileToRead, (nxt_frame+2), RecoveryFile)
            frame_count += 1
    return frame_count
    
def main():
    start=time.clock()
    ##Win Testing
#    sys.argv.append('L:/Hons Year/Honours Project/Code/TestCases/MP3Test.mp3')
#    sys.argv.append('L:/Hons Year/Honours Project/Code/TestCases/MP3TestObf.jpg')
#    sys.argv.append('L:/Hons Year/Honours Project/Code/TestCases/1MrY0X.gif')
#    sys.argv.append('L:/Hons Year/Honours Project/Code/TestCases/Test_Mp3_3.mp3')
#    sys.argv.append('L:/Hons Year/Honours Project/Code/Recovered/MP3Recd.mp3')
    ##Ubuntu Testing
    sys.argv.append('/home/immortalsnow/Documents/Code/TestCases/MP3Test.mp3')
#    sys.argv.append('/media/immortalsnow/MainUSB/Hons Year/Honours Project/Code/TestCases/05 - Everything I Do (I Do It for You).mp3')
#    sys.argv.append('/media/immortalsnow/MainUSB/Hons Year/Honours Project/Code/TestCases/MP3TestObf.jpg')
#    sys.argv.append('/media/immortalsnow/MainUSB/Hons Year/Honours Project/Code/TestCases/1MrY0X.gif')
#    sys.argv.append(/media/immortalsnow/MainUSB/Hons Year/Honours Project/Code/TestCases/Test_Mp3_3.mp3')
    sys.argv.append('/home/immortalsnow/Documents/Code/Recovered/MP3Recd.mp3')

    if len(sys.argv) != 3:
        print 'Usage: FrameFinder.py *Name of file to scan* *filename to write new frames to*'
        print 'Please ensure you provide the name of the file whose frames you need to find'
        print 'Followed by the filename you want to write the new frames to'
    else:
        if os.path.exists(sys.argv[1]):
            RecoveryData = sys.argv[1]
            RecoveryFile = sys.argv[2]
            numberframes= mp3_check(RecoveryData, RecoveryFile)
            if type(numberframes) == int:
                print '\n[*] No. of frames recovered: ' + str(numberframes)
                print '\n[*] Recovery process on this file took: %s seconds' % round(time.clock() - start, 2)
                hash1=ssdeep.hash_from_file(sys.argv[1])
                hash2=ssdeep.hash_from_file(sys.argv[2])
#                hash2=ssdeep.hash_from_file('/media/immortalsnow/MainUSB/Hons Year/Honours Project/Code/TestCases/05 - Everything I Do (I Do It for You).mp3')
                print '\n[*] The recovered file appears to match \'%s\' at a %s' % (sys.argv[1],ssdeep.compare(hash1,hash2)) + '\x25 consistency'
            elif type(numberframes)==str:
                print '\n[*] CAUTION -- The file you tried to recover from does not look like an MP3.'
        else:
            print '\n[*] The file you wish to perform recovery analysis on cannot be found at the location provided, please check and try again.'
            sys.exit()
        
    
if __name__ == '__main__':
    if TRACE: print '[S] FrameFinder Module called as script, calling main'
    main()
else:
    if TRACE: print '[L] FrameFinder Module imported as library, not calling main'
