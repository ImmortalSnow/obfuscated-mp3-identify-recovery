# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 21:30:04 2016
@author: ImmortalSnow
"""

TRACE=True


from VersionIdentifier import FrameID
import time, re, sys, FrameFind, os, ReadAsByte, ssdeep

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
        nxt_frame = FrameFind.FirstFrame(FileToRead,strt_frame, RecoveryFile)
        frame_count += 1
    while nxt_frame < last_indx:
        if FileToRead[nxt_frame: (nxt_frame +4)] == Version:
            nxt_frame = FrameFind.SecondaryFrames(FileToRead, nxt_frame, RecoveryFile)
            frame_count += 1
        ##On occasion, it has been noted that the padding bit may be set, but no padding is seen in the file.
        #In these instances, the figures for each frame are thrown off slightly.
        #To get round this, i have ibcluded code that will adjust the frame header retrieval by one byte,
        ## forwards or backwards, as needed to recover the correct frame
        elif FileToRead[(nxt_frame-2): (nxt_frame +2)] == Version:
            nxt_frame = FrameFind.SecondaryFrames(FileToRead, (nxt_frame-2), RecoveryFile)
            frame_count += 1
        elif FileToRead[(nxt_frame+2): (nxt_frame +6)] == Version:
            nxt_frame = FrameFind.SecondaryFrames(FileToRead, (nxt_frame+2), RecoveryFile)
            frame_count += 1
    return frame_count
    
def main():
    start=time.clock()
    tree=[]
    fileCount=1
    ##Win Testing
#    sys.argv.append('L:/Hons Year/Honours Project/Code/TestCases/MP3Test.mp3')
#    sys.argv.append('L:/Hons Year/Honours Project/Code/TestCases/MP3TestObf.jpg')
#    sys.argv.append('L:/Hons Year/Honours Project/Code/TestCases/1MrY0X.gif')
#    sys.argv.append('L:/Hons Year/Honours Project/Code/TestCases/Test_Mp3_3.mp3')
#    sys.argv.append('L:/Hons Year/Honours Project/Code/Recovered/MP3Recd.mp3')
    ##Ubuntu Testing
#    sys.argv.append('/media/immortalsnow/MainUSB/Hons Year/Honours Project/Code/TestCases/MP3Test.mp3')
#    sys.argv.append('/media/immortalsnow/MainUSB/Hons Year/Honours Project/Code/TestCases/05 - Everything I Do (I Do It for You).mp3')
#    sys.argv.append('/media/immortalsnow/MainUSB/Hons Year/Honours Project/Code/TestCases/MP3TestObf.jpg')
#    sys.argv.append('/media/immortalsnow/MainUSB/Hons Year/Honours Project/Code/TestCases/1MrY0X.gif')
#    sys.argv.append(/media/immortalsnow/MainUSB/Hons Year/Honours Project/Code/TestCases/Test_Mp3_3.mp3')
#    sys.argv.append('/media/immortalsnow/MainUSB/Hons Year/Honours Project/Code/Recovered/MP3Recd.mp3')
    #New Tests
    #win
#    sys.argv.append('E:\\')
#    sys.argv.append('C:\\Users\\ImmortalSnow\\Dropbox\\HonoursProject\\Code\\Recovered\\')
    #ubuntu
#    sys.argv.append('/media/immortalsnow/01D279B6A4666B30')
#    sys.argv.append('/home/immortalsnow/Dropbox/HonoursProject/Code/Recovered')
#    sys.argv.append('/home/immortalsnow/Dropbox/HonoursProject/Code/Honours-MP3_Recovery/KnownMP3s.txt')
    

    if len(sys.argv) != 4:
        print '\nUsage: FindObfuscation.py *Mount point of disk to scan for obfuscated mp3 files* *Directory to write recovered files to* *Hash Library file*'
        print '\tPlease ensure you provide:'
        print '\t\tThe mount point of the disk or image to be scanned for MP3 files'
        print '\t\tThe directory you want any recovered files stored'
        print '\t\tThe location of the hash library to be used for comparison'
    else:
        if os.path.exists(sys.argv[1]):
            print '\n[I]Process begun to identify obfuscated MP3 files on %s. Recovered files will be stored at %s.' % (sys.argv[1],sys.argv[2])
            for root, dirs, files in os.walk(sys.argv[1]):
                for f in files:
                    if root.endswith(os.sep):
                        tree.append(root+f)
                    else:
                        tree.append(root+os.sep+f)
            for branch in tree:
                fileTimeStart=time.clock()
                
                RecoveryFile = 'RecoveredMP3_%s.mp3' % str(fileCount)
                
                if sys.argv[2].endswith(os.sep):
                    RecoveryFileLoc = sys.argv[2]+RecoveryFile
                else:
                    RecoveryFileLoc = sys.argv[2]+os.sep+RecoveryFile
                                              
                numberframes= mp3_check(branch, RecoveryFileLoc)
                
                FuzzHashLib=[]
                HashLibFile=sys.argv[3]
                result=[]
                match=('',0)
                if type(numberframes) == int:
                    print '\n[T] Recovery process on file %s took: %s seconds' % ('\'%s\'' % branch, round(time.clock() - fileTimeStart, 2))
                    print '[R] No. of frames recovered: ' + str(numberframes)
                    with open(HashLibFile) as MP3FuzzHash:
                        next(MP3FuzzHash)
                        for line in MP3FuzzHash:
                            FuzzHashLib.append(line)
                    hashRec=ssdeep.hash_from_file(RecoveryFileLoc)
                    for each in FuzzHashLib:
                        result.append((each.split(',')[1][1:-2],ssdeep.compare(hashRec,each)))
                        for each in result:
                            if each[1] >> match[1]:
                                match = each
                    print '[M] The MP3 data contents recovered from file %s  and written to %s, matches the MP3 \'%s\' at a %s' % (branch,RecoveryFile,match[0],match[1]) + '\x25 consistency'
                    fileCount+=1
                elif type(numberframes)==str:
                    print '\n[-] CAUTION -- You attempted to recover MP3 frames from the file %s, which does not look like an MP3.' % branch
        else:
            print '\n[**] The image or disk you wish to perform identity and recovery analysis on cannot be found at the location provided, please check and try again.'
            sys.exit()
        print '\n[**] Total processing and recovery time of specified disk or image contents took %s seconds' % round(time.clock() - start, 2)
        
    
if __name__ == '__main__':
    if TRACE: print '[S] FrameFinder Module called as script, calling main'
    main()
else:
    if TRACE: print '[L] FrameFinder Module imported as library, not calling main'
