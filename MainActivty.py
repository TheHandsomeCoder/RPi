charset = "abcdefghijklmnopqrstuvwxyz0123456789"
 
base = 36
 
import hashlib
import struct
import argparse
from os import listdir
from os.path import isfile, join
from functools import partial

from RainbowTableFileInfo import RainbowChainInfo
from RTRainbowChain import RTRainbowChain
from RTRainbowChainLink import RTRainbowChainLink

hash = ""
filename = "/Users/scottomalley/RainbowTables/md5_loweralpha-numeric#1-7_0_2x50_0.rt"
blocksize = 8
filedirectory = ""
rainbowTables = []
candidateChains = []
foundHashResult = []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-hs', help="The Hash you wish to crack", required=True)
    parser.add_argument("-rt", help="The Directory containing your Rainbow Tables", required=True)
    args = parser.parse_args()
    hash = args.hs
    filedirectory = args.rt
    rainbowTables = [ f for f in listdir(filedirectory) if isfile(join(filedirectory,f)) and f.split(".").pop() == "rt"]
    print "{0} files containing rainbow tables found".format(len(rainbowTables))

    for rt in rainbowTables:
        rTable = RainbowChainInfo(join(filedirectory, rt))
        print "Using {0}".format(rTable.fileLocation)
        candidateHashes = preCalc(hash,rTable)
        searchFile(candidateHashes, rTable)

        hashfound = checkForFalseAlarms(hash, rTable)

        if(hashfound):
            print foundHashResult[0]
            break
        else:
            print "Hash Not found :'("

def checkForFalseAlarms(targetHash, rTable):
    for chain in candidateChains:
        if(chainWalkHashLookup(targetHash.decode("hex"), chain.start_point, 0, rTable.chainLength, rTable.tableIndex)):
            return True

    return False



def searchFile(candidateHashes, rTable):
    print "Begin searching file"
    chainsRead = 0;
    with open(rTable.fileLocation, 'rb') as f:
        for chunk in iter(partial(f.read, 16), ''):
            chainsRead += 16
            if chainsRead % 16000 == 0:
                print "{0} Chains read".format(chainsRead/16)
            try:
                endpoint = struct.unpack("<Q",chunk[8:16])[0]
                for x in candidateHashes:
                    if(x == endpoint):
                        candidateChains.append(RTRainbowChain(struct.unpack("<Q",chunk[0:8])[0], endpoint))

            except struct.error:
                break

    print "Finished Searching file {0} potential chains found".format(len(candidateChains))

def preCalc(hash, tempTable):

    print "starting preCalc"
    candidateHashes = chainWalkFromPositionToEnd(hash.decode("hex"),0,tempTable.chainLength, 0)
    print "preCalc Complete {0} candidate hashes created".format(len(candidateHashes))
    return candidateHashes


def chainWalkFromPositionToEnd(hash, position, chainLength, tableIndex):
    candidateHashes = []
    if position == (chainLength - 1):
        candidateHashes.append(hashToIndex(hash, position, tableIndex))
    else:
        index = hashToIndex(hash, position, tableIndex)
        candidateHashes.append(index)
        position += 1
        while position != chainLength:
            plain = indexToPlain(index)
            hash = plainToHash(plain)
            index = hashToIndex(hash,position, tableIndex)
            candidateHashes.append(index)
            position += 1
    return candidateHashes

def chainWalkHashLookup(targetHash, startPoint, position, chainLength, tableIndex):
    startDec = startPoint

    while position != chainLength:
        plain = indexToPlain(startDec)
        hash = plainToHash(plain)

        if(hash == targetHash):
            foundHashResult.append(RTRainbowChainLink(hashlib.md5(plain).hexdigest(),plain,startDec))
            return True
        startDec = hashToIndex(hash, position, tableIndex)
        position += 1

    return False
 
def get_md5_as_bytes(data):
    m = hashlib.md5()
    m.update(data)
    return m.digest()


def get_md5_as_hex_string(data):
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()
 
def get_str(a):
 
    if a < base:
        return charset[a]
    return get_str(int((a - a%base)/base - 1) ) + get_str(a % base)



 
 
def read_file():

    with open(filename, 'rb') as f:
         while True:
              try:
                  print struct.unpack_from("<Q",f.read(8))[0]
                 # `<` means little endian; `Q` means unsigned long long (8 bytes)
              except struct.error:
                 break

def getKeySpace(minPassLen, maxPassLen, charsetLen):
    keyspace = 0

    for x in range(minPassLen, maxPassLen + 1, 1):
        keyspace += pow(charsetLen,x)

    return keyspace


"""
print "keyspace size = " + str(getKeySpace(1,7, 36))

0
4458459792

print len(charset)

"""
"""read_file()"""


def indexToPlain(index):
    return get_str(index)

def plainToHash(plain):
    return get_md5_as_bytes(plain)

def hashToIndex(hash, chainPos, tableIndex):
    return (struct.unpack("<Q", hash[0:8])[0] + tableIndex + chainPos) % getKeySpace(1,7,len(charset))



def chainwalk(filename):

    index = struct.pack("<Q",0);
    print (index)
    print "keyspace " + str(getKeySpace(1,7,36))

    print "Index: " + str(index)
    binary = struct.unpack_from("<Q", index)[0]
    print "Index to binary:" + str(binary)
    plain = get_str(binary)
    print "binary to plain: " + plain
    hash = get_md5_as_bytes(plain)
    print "plain to hash: " + get_md5_as_hex_string(plain)
    print "\n"

    index = hash[0:8]
    index = (struct.unpack("<Q", index)[0] + 0 + 0) % getKeySpace(1,7,len(charset))
    print "Index: " + str(index)
    plain = get_str(index)
    print "binary to plain: " + plain
    hash = get_md5_as_bytes(plain)
    print "plain to hash: " + get_md5_as_hex_string(plain)
    print"\n"

    index = hash[0:8]
    index = (struct.unpack("<Q", index)[0] + 0 + 1) % getKeySpace(1,7,len(charset))
    print "Index: " + str(index)
    plain = get_str(index)
    print "binary to plain: " + plain
    hash = get_md5_as_bytes(plain)
    print "plain to hash: " + get_md5_as_hex_string(plain)



if __name__ == "__main__":
   main()


