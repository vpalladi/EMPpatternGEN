#!/usr/bin/python3

import random  
import numpy as np


class EMPword :

    def __init__(self, word=0, valid=False, prec=64) :
        self.word = word
        self.prec = prec
        self.width = int( prec/4 )
        self.valid = valid
        
    def genRand(self) :
        self.valid = True
        self.word = random.randint( 1, pow(2, self.prec)-1 )

    def word(self, word, valid=False) :
        self.word = word
        self.valid = valid
        
    def printHex(self) :
        valid = 1 if self.valid else 0
        print( str(valid)+'v'+format(self.word, '0'+str(self.width)+'x' ), end='' )

        
class EMPchannel :
    def __init__(self) :
        self.chan = []

    def addFrame(self, data) :
        self.chan.append(data)
    
    def setFrame(self, frameId, data) :
        if frameId<len(self.chain) :
            self.chan[frameId] = data
        else :
            print('Frame index out of range. (EMPchannel)')
    
    def getFrame(self, frameId) :
        return self.chan[frameId]
            
    def genRand(self, nFrames) :
        for i in range(0, nFrames) :
            w  = EMPword()
            w.genRand()
            self.addFrame( w )

    def addSOF(self, nWords=6) :
        for i in range(0, nWords) :
            w = EMPword()
            self.addFrame(w)
            
    def nFrames(self) :
        l = len( self.chan )
        return l

    def print(self) :
        for fr in self.chan :
            fr.printHex()
            print()
        print()


class EMPpattern :

    def __init__(self, boardName, nChannels) :
        self.boardName = boardName

        self.header = 'Board '+boardName+'\n'

        self.header = self.header+' Quad/Chan :'
        for i in range(0, nChannels) :
            quad = int(i/4)
            chan = int(i%4)
            self.header = self.header+' '+('q'+format(quad,'02d')+'c'+str(chan)).ljust(18)
        self.header = self.header+'\n'

        self.header = self.header+'      Link :'
        for i in range(0, nChannels) :
            self.header = self.header+' '+format(i,'02d').ljust(18)
        self.header = self.header+'\n'

        self.channels = [EMPchannel() for i in range(0, nChannels)]
        

    def genRand( self, nFrames ) :
        for ch in self.channels :
            ch.addSOF()
            ch.genRand( nFrames )
            ch.addSOF()

    def genSeq( self, nFrames ) :
        for i,ch in enumerate(self.channels) :
            ch.addSOF()
            for c in range(0, nFrames) :
                value = c | (i<<56)
                w = EMPword( value, True, 64 )
                ch.addFrame( w )
            ch.addSOF()

    def print( self ) :
        print( self.header, end='' )
        nFrames = self.channels[0].nFrames()
        for iframe in range(0, nFrames) :
            print( 'Frame '+format(iframe, '04d')+' :', end='' )
            for ch in self.channels :
                print(' ', end='')
                ch.getFrame(iframe).printHex()
            print('')

            
EP = EMPpattern('test', 72)
EP.genSeq(100)
EP.print()
