# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 21:33:17 2016

@author: Paul Flack

Desc: The modules of this script identify the different parts of a frame header
"""

#Calculates the MPEG version from the frame header
def VersionCalc(frameHeader):
    if frameHeader[11]== '1' and frameHeader[12] == '1':
        versionID = 1
    elif frameHeader[11]==  '1' and frameHeader[12] == '0':
        versionID = 2
    elif frameHeader[11]==  '0' and frameHeader[12] == '0':
        versionID = 2.5
    return versionID

#Calculates the Layer of the MPEG.
#By definition, this should always return a layer 3 for our use, as all
#MP3 files are layer 3
def LayerCalc(frameHeader):
    if frameHeader[13] =='0' and frameHeader[14] == '1':
            Layer = 3
    elif frameHeader[13] =='0' and frameHeader[14] == '0':
            Layer = 0
    elif frameHeader[13]=='1' and frameHeader[14] == '1':
            Layer = 1
    elif frameHeader[13] =='1' and frameHeader[14] == '0':
            Layer = 2
    return Layer
        
#Calculates if the protection bit is set for the CRC after the frame header
def ProtCalc(frameHeader):
    if frameHeader[15] == '1':
        ProtBit = False
    elif frameHeader[15] == '0':
        ProtBit = True
    return ProtBit
    
#Calculates the Bitrate of the frame, this is used alongside other items
#to calculate the length of the frame
def BitrateCalc(frameHeader):
    BitrateBits = frameHeader[16] + frameHeader[17] + frameHeader[18] + frameHeader[19]
    V1L3 = {'0000':'free','0001':32,
            '0010':40,'0011':48,
            '0100':56,'0101':64,
            '0110':80,'0111':96,
            '1000':112,'1001':128,
            '1010':160,'1011':192,
            '1100':224,'1101':256,
            '1110':320,'1111':"bad"}
    V2L3 = {'0000':'free','0001':8,
            '0010':16,'0011':24,
            '0100':32,'0101':40,
            '0110':48,'0111':56,
            '1000':64,'1001':80,
            '1010':96,'1011':112,
            '1100':128,'1101':144,
            '1110':160,'1111':"bad"}
    
    if VersionCalc(frameHeader)== 1 and LayerCalc(frameHeader) == 3:
        if BitrateBits in V1L3:
            return (V1L3[BitrateBits] * 1000)
    
    elif VersionCalc(frameHeader)== 2 and LayerCalc(frameHeader) == 3:
        if BitrateBits in V2L3:
            return (V2L3[BitrateBits] * 1000)
            
#Calculates the Sampling rate of the frame, this is used alongside other items
#to calculate the length of the frame
def SampleFreqCalc(frameHeader):
    SamplingBits = frameHeader[20] + frameHeader[21]
    MPEG1 ={'00':44100,'01':48000,'10':32000,'11':'reserved'}
    MPEG2 ={'00':22050,'01':24000,'10':16000,'11':'reserved'}
    MPEG25 ={'00':11025,'01':12000,'10':8000,'11':'reserved'}
    
    if VersionCalc(frameHeader) == 1:
        if SamplingBits in MPEG1:
            return MPEG1[SamplingBits]
    elif VersionCalc(frameHeader) == 2:
        if SamplingBits in MPEG2:
            return MPEG2[SamplingBits]

#Defines the padding Bit, used to calculate length of frame
def PaddingBit(frameHeader):
    if frameHeader[22]=='0':
        PaddingBit=0
    elif frameHeader[22] =='1':
        PaddingBit=1
    return PaddingBit