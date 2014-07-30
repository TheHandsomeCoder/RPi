__author__ = 'scottomalley'

import numpy as np


dt = np.dtype([('sp', '<i8' ), ('ep', '<i8')])

with open("/Users/scottomalley/RainbowTables/timeTest/md5_loweralpha-numeric#1-7_0_2x50_0.rt", 'rb') as f:
    rainbowChains = np.fromfile(f, dtype=dt, count=50)



def binarySearch(rainbowChains, index):
    lowPoint = 0
    highpoint = len(rainbowChains) - 1

    while (lowPoint <= highpoint):
        midPoint = int((lowPoint + highpoint) / 2)
        if(index == midPoint):
            return midPoint
        elif(index < midPoint):
            highpoint = midPoint - 1
        else:
            lowPoint = midPoint + 1

    return -1

