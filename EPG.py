#!/usr/bin/python3

import random  
import numpy as np
import re

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

    def __init__(self, quad=0, ch=0, link=0) :
        self.chan = []
        self.link = int(link)
        self.ch   = int(ch)
        self.quad = int(quad)
        
    def getQuadStr( self ) :
        return ( 'q'+format(self.quad,'02d')+'c'+str(self.ch) )

    def getLinkStr( self ) :
        return format(self.link,'02d')

    def addFrame ( self, data ) :
        self.chan.append(data)
    
    def setFrame( self, frameId, data ) :
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

    def __init__(self, boardName='', nChannels=0) :
        self.boardName = boardName
        self.nChannels = nChannels

        self.channels = []
        
        for i in range(0, nChannels) :
            quad = int(i/4)
            chan = int(i%4)
            self.channels.append( EMPchannel( quad=q, ch=c, link=l ) )
        
    def loadPattern( self, fileName ) :
        fileIn = open(fileName)
        for line in fileIn.readlines() : 
            if re.search( '^Board', line ) :
                print( 'Board' )

            elif re.search( '^Frame', line ) :
                words = line.split(':')[1].split()
                for i,word in enumerate(words):
                    v = word.split('v')[0].replace(' ', '')
                    w = word.split('v')[1].replace(' ', '')
                    dataFormat = len( w.replace(' ', '') )*4
                    empW = EMPword(int(w, 16), int(v), dataFormat)
                    self.channels[i].addFrame( empW )
                                        
            elif re.search( '^\s*Quad', line ) :
                quads = line.split(':')[1]
                quads = re.sub( '^\s+' , '', quads ) 
                quads = re.sub( '\s+' , ' ', quads ) 
                
                for q in quads.split() :
                    self.nChannels = self.nChannels+1
                    quad = re.search('q[0-9]+', q)
                    ch   = re.search('c[0-9]+', q)
                    q = int( quad.group().replace('q','') )
                    c = int( ch.group().replace('c','') )
                    self.channels.append( EMPchannel( quad=q, ch=c ) ) 
                    
            elif re.search( '^\s*Link', line ) :
                links = line.split(':')[1]
                links = re.sub( '^\s+' , '', links ) 
                links = re.sub( '\s+' , ' ', links ) 
                
                for i,l in enumerate( links.split() ) :
                    self.channels[i].link = int(l)
 
            else :
                print( 'Error' )

                
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

        self.header = 'Board '+self.boardName+'\n'

        self.header = self.header+' Quad/Chan :      '
        for c in self.channels :
            self.header = self.header+' '+c.getQuadStr().ljust(18)
        self.header = self.header+'\n'

        self.header = self.header+'      Link :        '
        for c in self.channels :
            self.header = self.header+' '+c.getLinkStr().ljust(18)
        self.header = self.header+'\n'

        print( self.header, end='' )

        nFrames = self.channels[0].nFrames()
        for iframe in range(0, nFrames) :
            print( 'Frame '+format(iframe, '04d')+' :', end='' )
            for ch in self.channels :
                print(' ', end='')
                ch.getFrame(iframe).printHex()
            print('')


def main() :
    EP = EMPpattern()
    EP.loadPattern('injected_data.txt')

    #EP = EMPpattern(nChannels=10)
    #EP.genSeq(100)

    EP.print()


main()
