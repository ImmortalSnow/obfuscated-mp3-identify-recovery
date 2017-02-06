# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 03:23:39 2016

@author: ImmortalSnow
"""

TRACE=True

from binascii import unhexlify
from BinaryConverter import StringConversion
import FrameHeadAnalysis as FHA

def Frame(RecoveryData, nxt_frame, RecoveryFile):
    ##  Gets the Frame header and analyse the bits to determine the bit rate, sampling frequency and if padding is set, 
    ##  then uses this to determine the framelength
    frameHeader = RecoveryData[nxt_frame : (nxt_frame + 8)]
    frameHeaderBin = StringConversion(unhexlify(frameHeader))
    Bitrate = FHA.BitrateCalc(frameHeaderBin)
    SampleRate = FHA.SampleFreqCalc(frameHeaderBin)
    Padding = FHA.PaddingBit(frameHeaderBin)
    FrameLength = 144*Bitrate/SampleRate+Padding
    ##  Based on the framelength calculated above, returns the entire next frame of the mp3 audio stream and appends it to the existing file started with the first frame
    frame = RecoveryData[nxt_frame:(nxt_frame+(FrameLength*2))]
    with open(RecoveryFile, 'ab') as RecoveredFrames:
        RecoveredFrames.write(unhexlify(frame))
    ##  Returns the location of the next frame, based upon where the current frame ends, as all frames should usually be contiguous
    nxt_frame = nxt_frame + (FrameLength * 2)
    return nxt_frame
    
def main():
    print 'This script cannot be used independently of the main code, please run the main program'
        
if __name__ == '__main__':
    if TRACE: print '[S] SecondaryFrames Module called as script, calling main()'
    main()
else:
    if TRACE: print '[L] SecondaryFrames Module imported as library, not calling main'