#!/usr/bin/python3

from EPG import *
import os
import csv 
from optparse import OptionParser

import matplotlib.pyplot as plt

parser = OptionParser()
parser.add_option( "-i", "--ifile", dest="fileInName",
                   help="Input file name.", 
                   metavar="FILE" )

parser.add_option( "-o", "--ofile", dest="fileName",
                   help="Output file name.", 
                   metavar="FILE" )



(options, args) = parser.parse_args()

pattern = EMPpattern()

pattern.loadPattern( options.fileInName )

fileOpt    = 'a'
fileOut    = open(options.fileName, fileOpt)
fileWriter = csv.writer(fileOut, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

fileWriter.writerow( pattern.getLatency() )


#plt .savefig('./frame.png')

#
#for ch in pattern.channels :
#
#    ch.plotFrame
#
#
#    if not( ch.checkProgressive() ) :
#        print('not progressive on ch ', ch.getQuadStr(), ch.getLinkStr())
#
