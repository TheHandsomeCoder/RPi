
import numpy as np
import argparse
from RainbowTableFileInfo import RainbowChainInfo
from os import listdir
from os.path import isfile, join


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
    fileIndex = 0
    for file in rainbowTableFiles:
        count = 12500000
        fileLocation = filedirectory+file
        with open(fileLocation, 'rb') as f:
            chainsRead = 0
            rtable = RainbowChainInfo(file,filedirectory)
            while(chainsRead < rtable.numberOfChains):
                """Read the 250mb of chains from the file - Each chain is 16 bytes containing an 8 byte startPoint and End point"""
                rainbowChains = np.fromfile(f, dtype=dt, count=count)
                fileName = rtable.formatName(len(rainbowChains), fileIndex)

                newFileLocation = filedirectory+fileName
                rainbowChains.tofile(newFileLocation, "")
                fileIndex += 1
                chainsRead += count

if __name__ == "__main__":
    main()