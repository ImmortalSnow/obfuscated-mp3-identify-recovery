'''Obfuscation Tool, developed by P Flack 2017, must be edited to change the obfuscation types'''
from binascii import hexlify, unhexlify
import os

tree=[]
OBFhead='ffd8'
OBFfoot='ffd9'
filecount=0

for root, dirs, files in os.walk('/home/immortalsnow/Dropbox/HonoursProject/Code/TestCases/My\ ripped\ audio'):
    for f in files:
        tree.append(root+os.sep+f)
        
for branch in tree:
    filecount+=1
    obfFile ='/home/immortalsnow/Dropbox/HonoursProject/Code/TestCases/ObfuscatedMP3s/JPG/ObfMP3_%s.jpg' % str(filecount)
    with open(branch,'rb') as fBranch:
        mp3=hexlify(fBranch.read())
    with open(obfFile,'wb') as obfBranch:
        obfBranch.write(unhexlify(OBFhead+mp3+OBFfoot))
        
