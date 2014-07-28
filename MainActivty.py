charset = "abcdefghijklmnopqrstuvwxyz0123456789"
 
base = 36
 
import hashlib
import struct
import argparse
from os import listdir
from os.path import isfile, join

from RainbowTableFileInfo import RainbowChainInfo

hash = ""
filename = "/Users/scottomalley/RainbowTables/md5_loweralpha-numeric#1-7_0_2x50_0.rt"
blocksize = 8
filedirectory = ""
rainbowTables = []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-hs', help="The Hash you wish to crack", required=True)
    parser.add_argument("-rt", help="The Directory containing your Rainbow Tables", required=True)
    args = parser.parse_args()
    hash = args.hs
    filedirectory = args.rt
    rainbowTables = [ f for f in listdir(filedirectory) if isfile(join(filedirectory,f)) and f.split(".").pop() == "rt"]
    print rainbowTables

    """x = RainbowChainInfo(filename)
    print x"""


 
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

    decoded = []
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



def chainwalk():
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


