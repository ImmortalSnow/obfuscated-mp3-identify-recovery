# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 21:30:04 2016
@author: Paul Flack

This is the main script for my honours project. This allows a user to scan a file or image of files for mp3 frames and recover them,
before hashing them using SSDEEP as a fuzzy hash comparison to find the original files
"""

TRACE=True


from VersionIdentifier import FrameID
import time, re, sys, FrameFind, os, ReadAsByte, ssdeep

def mp3_check(RecoveryData,RecoveryFile):
    frame_count = 0
    versions={'Version 1, unprotected':'fffa',
              'Version 1, protected':'fffb',
              'Version 2, unprotected':'fff2',
              'Version 2, protected':'fff3',
			  #'Version 2.5, unprotected':'ffe2',
			  #'Version 2.5, protected':'ffe3'
              }
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
	
def file_examiner():
    ObfFile = raw_input('\n[*]Enter the path of the potentially obfuscated file you want to identify frames from for recovery: \n[*]:')
    if os.path.exists(ObfFile):
        RecoveryFile = raw_input('\n\n[*]Enter filename for where you would like any recovered frames to be stored.\n[*]:')
        HashLibFile = raw_input('\n\n[*]Input the file to use as a hash comparison library for identification of MP3 frames.\n[*]:')
        if os.path.exists(HashLibFile):
			start=time.clock()
			with open(os.path.dirname(RecoveryFile)+os.sep+'Recovery Process - '+time.asctime()+'.txt','wb') as RecoveryProcess:
				print '\n[I]Process begun to identify frames in potentially obfuscated MP3 file \'%s\'. Recovered frames will be stored at \'%s\'.' % (ObfFile,RecoveryFile)
				fileTimeStart=time.clock()
				numberframes= mp3_check(ObfFile, RecoveryFile)
				FuzzHashLib=[]
				result=[]
				match=('',0)
				if type(numberframes) == int:
					RecoveryProcess.write('\n[T] Recovery process on file %s took: %s seconds' % ('\'%s\'' % ObfFile, round(time.clock() - fileTimeStart, 2)))
					RecoveryProcess.write('\n[R] No. of frames recovered: ' + str(numberframes))
					with open(HashLibFile) as MP3FuzzHash:
						next(MP3FuzzHash)
						for line in MP3FuzzHash:
							FuzzHashLib.append(line)
					hashRec=ssdeep.hash_from_file(RecoveryFile)
					for each in FuzzHashLib:
						result.append((each.split(',')[1][1:-2],ssdeep.compare(hashRec,each)))
						for each in result:
							if each[1] >> match[1]:
								match = each
					RecoveryProcess.write('\n[*] The MP3 data contents recovered from file %s  and written to %s, matches the MP3 \'%s\' at a %s' % (ObfFile,RecoveryFile,match[0],match[1]) + '\x25 consistency')
					RecoveryProcess.write('\n[**] Total processing and recovery time of specified file took %s seconds' % round(time.clock() - start, 2))
				elif type(numberframes)==str:
					RecoveryProcess.write('\n[-] CAUTION -- You attempted to recover MP3 frames from the file %s, which does not look like an MP3.' % ObfFile)
        else:
			print '[-]The file to use as a hash comparison library is missing.'
			sys.exit()
    else:
        print '\n[**] The file you wish to perform identity and recovery analysis on cannot be found at the location provided, please check and try again.'
        sys.exit()
	
def disk_examiner():
    tree=[]
    fileCount=1
    img_mnt = raw_input('\n[*]Enter mount point of the disk or image containing files you want to identify frames from for recovery.\n[*]:')
    if os.path.exists(img_mnt):
#        recoveryDir = raw_input('[*]Enter directory you would like any recovered files to be stored.\n[*]:')
        recoveryDir ='/home/Desktop/DemoRecoveries'
        if os.path.exists(recoveryDir):
#            HashLibFile = raw_input('[*]Input the file to use as a hash comparison library for identification of MP3 frames.\n[*]:')
            HashLibFile = '/home/immortalsnow/Desktop/Code/KnownMP3s.txt'
            if os.path.exists(HashLibFile):
                start=time.clock()
                with open(recoveryDir+os.sep+'Recovery Process - '+time.asctime()+'.txt','wb') as RecoveryProcess:
                    print '\n[I]Process begun to identify obfuscated MP3 files on \'%s\'. Recovered files will be stored at \'%s\'.' % (img_mnt,recoveryDir)
                    for root, dirs, files in os.walk(img_mnt):
                        for f in files:
                            if root.endswith(os.sep):
                                tree.append(root+f)
                            else:
                                tree.append(root+os.sep+f)
                        for branch in tree:
                            fileTimeStart=time.clock()
                            RecoveryFile = 'RecoveredMP3_%s.mp3' % str(fileCount)
                            if recoveryDir.endswith(os.sep):
                                RecoveryFileLoc = recoveryDir+RecoveryFile
                            else:
                                RecoveryFileLoc = recoveryDir+os.sep+RecoveryFile
                            numberframes= mp3_check(branch, RecoveryFileLoc)
                            FuzzHashLib=[]
                            result=[]
                            match=('',0)
                            if type(numberframes) == int:
                                RecoveryProcess.write('\n\n[T] Recovery process on file %s took: %s seconds' % ('\'%s\'' % branch, round(time.clock() - fileTimeStart, 2)))
                                RecoveryProcess.write('\n[R] No. of frames recovered: ' + str(numberframes))
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
                                RecoveryProcess.write('\n[M] The MP3 data contents recovered from file %s  and written to %s, matches the MP3 \'%s\' at a %s' % (branch,RecoveryFile,match[0],match[1]) + '\x25 consistency')
                                fileCount+=1
                            elif type(numberframes)==str:
                                RecoveryProcess.write('\n\n[-] CAUTION -- You attempted to recover MP3 frames from the file %s, which does not look like an MP3.' % branch)
                        RecoveryProcess.write('\n\n\n[**] Total processing and recovery time of specified disk or image contents took %s seconds' % round(time.clock() - start, 2))
            else:
                print '[-]The file to use as a hash comparison library is missing.'
                sys.exit()
    else:
        print '\n[**] The image or disk you wish to perform identity and recovery analysis on cannot be found at the location provided, please check and try again.'
        sys.exit()
    
def main():
#    sys.argv.append('-file')

#    sys.argv.append('/home/immortalsnow/Dropbox/HonoursProject/Code/TestCases/ObfuscatedMP3s/f/MP3Test1.jpg')
#    sys.argv.append('/home/immortalsnow/Dropbox/HonoursProject/Code/Honours-MP3_Recovery/KnownMP3s.txt')
# '/home/immortalsnow/Dropbox/HonoursProject/Code/Recovered/recd1.mp3'

    if len(sys.argv) != 2:
        print '\nUsage: FindObfuscation *mode*'
        print '\tProvide the operating mode:'
        print '\t\tTo check all files on a disk or image, use: -i or -image.'
        print '\t\tTo check an individual file, use: -f or -file'
        
    else:
        if sys.argv[1] == '-image' or sys.argv[1] == '-i':
			disk_examiner()
        elif sys.argv[1] == '-file' or sys.argv[1] == '-f':
            file_examiner()


        
    
if __name__ == '__main__':
    if TRACE: print '[S] FrameFinder Module called as script, calling main'
    main()
else:
    if TRACE: print '[L] FrameFinder Module imported as library, not calling main'
