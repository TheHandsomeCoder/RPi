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

charset = "abcdefghijklmnopqrstuvwxyz0123456789 "

# Take an index, check if it's in the the second to last
# position if not reduce until at the end of the chain return the last index
def chainWalkFromPositionToEnd(hash, position, rtable, keyspace):

    if position == (rtable.chainLength - 2):
        return hashToIndex(hash, position, rtable, keyspace)
    else:
        index = hashToIndex(hash, position, rtable, keyspace)
        position += 1
        while position <= rtable.chainLength -2:
            plain = indexToPlain(index)
            hash = plainToHash(plain)
            index = hashToIndex(hash,position, rtable,keyspace)

            position += 1
    return index



#Convert a long/int to it's character representation in the char set
def indexToPlain(index):
    return get_str(index)

#Convery a plaintext to MD5#
def plainToHash(plain):
    return get_md5_as_bytes(plain)

#Convert Hash to an index, Done by taking the first 8 Bytes of the hash,
#adding the tables index and chain position and modulusing the result by the keyspace
def hashToIndex(hash, chainPos, table, keyspace):
    return (struct.unpack("<Q", hash[0:8])[0] + table.tableIndex + chainPos) % keyspace

#Calculate the number of potential passwords in the keyspace
def getKeySpace(minPassLen, maxPassLen, charsetLen):
    keyspace = 0
    for x in range(minPassLen, maxPassLen + 1, 1):
        keyspace += pow(charsetLen,x)
    return keyspace

def get_md5_as_bytes(data):
    m = hashlib.md5()
    m.update(data)
    return m.digest()


#Take long/integer and convert it to a plaintext using the charset
def get_str(a):
    base = len(charset)
    if a < base:
        return charset[a]
    return get_str(int((a - a % base)/base - 1) ) + get_str(a % base)

#Binary Search the array
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

    with open("C:\RainbowTables\md5_loweralpha-numeric-space#1-8_0_10000x67108864_00.rt", 'rb') as file:

        dt = np.dtype([('startPoint', '<u8' ), ('endPoint', '<u8')])

        #Parse table info from table name
        rtable = RainbowChainInfo("md5_loweralpha-numeric-space#1-8_0_10000x67108864_distrrtgen[p][i]_00.rt", "/Users/scottomalley/RainbowTables/timeTest/")

        #Calculate the keyspace
        keyspace = getKeySpace(rtable.minPasswordLength, rtable.maxPasswordLength, len(charset))

        #Convert Hash to Binary for use as charset index
        index = binascii.a2b_hex("0cc175b9c0f1b6a831c399e269772661")

        #Read the chains from the file - Each chain is 16 bytes containing an 8 byte startPoint and End point"""
        rainbowChains = np.fromfile(file, dtype=dt)

        for x in reversed(range(0, rtable.chainLength -1 , 1)):
            #Reduce the index using the reduction function from chain position x till end of the chain"""
            reductionIndex = chainWalkFromPositionToEnd(index, x, rtable, keyspace)

            potenditalFound = np.searchsorted(rainbowChains['endPoint'],reductionIndex, side="left")
            if(potenditalFound != len(rainbowChains)):
                print "Do something with this array location"

            #potenditalFound = binarySearch(rainbowChains, index)"""
            #if(potenditalFound != -1)"""

