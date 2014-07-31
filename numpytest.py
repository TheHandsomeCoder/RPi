__author__ = 'scottomalley'

import numpy as np
import hashlib
import struct
import argparse
import binascii
from os import listdir
from os.path import isfile, join
from functools import partial

from RainbowTableFileInfo import RainbowChainInfo
from RTRainbowChain import RTRainbowChain
from RTRainbowChainLink import RTRainbowChainLink


charset = "abcdefghijklmnopqrstuvwxyz0123456789"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-hs', help="The Hash you wish to crack", required=True)
    parser.add_argument("-rt", help="The Directory containing your Rainbow Tables", required=True)
    args = parser.parse_args()
    hash = args.hs
    filedirectory = args.rt
    rainbowTableFiles = [ f for f in listdir(filedirectory) if isfile(join(filedirectory,f)) and f.split(".").pop() == "rt"]
    print "{0} files containing rainbow tables found".format(len(rainbowTableFiles))



    dt = np.dtype([('startPoint', '<u8' ), ('endPoint', '<u8')])
    for r in rainbowTableFiles:
        currentFile = RainbowChainInfo(r,filedirectory)
        print currentFile.fileLocation
        with open(currentFile.fileLocation, 'rb') as f:
            rainbowChains = np.fromfile(f, dtype=dt)
            print hash
            hash = binascii.a2b_hex(hash)
            print hash
            for x in reversed(range(0,currentFile.chainLength -1 ,1)):
                if(x % 1000 == 0):
                    print x
                index = chainWalkFromPositionToEnd(hash,x,currentFile)
                isMatchingIndex = binarySearch(rainbowChains, index)
                if(isMatchingIndex != -1):
                    match = chainWalkCheckHash(hash,rainbowChains[isMatchingIndex]['startPoint'], x, currentFile)
                    if(match != -1):
                        print "The password is {0}".format(match)
                        break




def chainWalkCheckHash(targetHash, index, potential_position, rtable):

        position = 0
        while position <= rtable.chainLength - 1:
            plain = indexToPlain(int(index))
            hash = plainToHash(plain)
            if(targetHash == hash):
                print(position,potential_position)
                return plain
            index = hashToIndex(hash,position, rtable)
            position += 1
        return -1



def chainWalkFromPositionToEnd(hash, position, rtable):

    if position == (rtable.chainLength - 2):
        return hashToIndex(hash, position, rtable)
    else:
        index = hashToIndex(hash, position, rtable)

        position += 1
        while position <= rtable.chainLength -2:
            plain = indexToPlain(index)
            hash = plainToHash(plain)
            index = hashToIndex(hash,position, rtable)

            position += 1
    return index



def indexToPlain(index):
    return get_str(index)

def plainToHash(plain):
    return get_md5_as_bytes(plain)

def hashToIndex(hash, chainPos, table):
    return (struct.unpack("<Q", hash[0:8])[0] + table.tableIndex + chainPos) % getKeySpace(table.minPasswordLength,table.maxPasswordLength,len(charset))

def getKeySpace(minPassLen, maxPassLen, charsetLen):
    keyspace = 0
    for x in range(minPassLen, maxPassLen + 1, 1):
        keyspace += pow(charsetLen,x)
    return keyspace

def get_md5_as_bytes(data):
    m = hashlib.md5()
    m.update(data)
    return m.digest()

def get_str(a):
    base = len(charset)
    if a < base:
        return charset[a]
    return get_str(int((a - a%base)/base - 1) ) + get_str(a % base)





def binarySearch(rainbowChains, index):
    lowPoint = 0
    highpoint = len(rainbowChains) - 1


    while (lowPoint <= highpoint):
        midPoint = int((lowPoint + highpoint) / 2)

        if(index == rainbowChains[midPoint]['endPoint']):
            return midPoint

        elif(index < rainbowChains[midPoint]['endPoint']):
            highpoint = midPoint - 1

        else:
            lowPoint = midPoint + 1

    return -1

if __name__ == "__main__":
    file = open("/Users/scottomalley/RainbowTables/timeTest/md5_loweralpha-numeric-space#1-8_0_10000x67108864_distrrtgen[p][i]_00.rt", "rb")
    rtable = RainbowChainInfo("md5_loweralpha-numeric-space#1-8_0_10000x67108864_distrrtgen[p][i]_00.rt","/Users/scottomalley/RainbowTables/timeTest/")
    index = binascii.a2b_hex("0cc175b9c0f1b6a831c399e269772661")
    dt = np.dtype([('startPoint', '<u8' ), ('endPoint', '<u8')])
    rainbowChains = np.fromfile(file, dtype=dt)
    endpoints = np.copy(rainbowChains["endPoint"])
    for x in reversed(range(0,rtable.chainLength -1 ,1)):

        if(x % 100 == 0): print (x)
        reduced = chainWalkFromPositionToEnd(index, x, rtable)
        """potentialFound = binarySearch(rainbowChains, reduced)"""

        l = np.searchsorted(rainbowChains['endPoint'],reduced, side="left")
        """ if(potentialFound != -1):
           print "We have a potential match @ position {0} in chain {1}".format(x, reduced)
           break
        else:
           print "Not this time"""""
        """print str(l) + ' ' +str(x)"""