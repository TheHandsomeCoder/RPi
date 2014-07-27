__author__ = 'scottomalley'
import os

class RainbowChainInfo:
    """simplest version of rainbowtable file info"""
    hashFunction = ""
    characterSet = ""
    minPasswordLength = 0
    maxPasswordLength = 0
    tableIndex = 0
    chainLength = 0
    numberOfChains = 0
    tablePartIndex = 0
    tableFormat = ""

    def __init__(self, file):
        filePath,fileName = os.path.split(file)

        if fileName.split(".").pop() == "rt":
            tableParams = []
            splitCharacters = "_#-__x_."

            for ch in splitCharacters:
                fileName = fileName.split(ch,1)
                tableParams.append(fileName[0])
                fileName = fileName[1]
            tableParams.append(fileName)
            self.assignVariables(tableParams)
        else:
            print "Tables in {0}{1} format aren't currently supported".format(".", fileName.split(".").pop())


    def assignVariables(self, params):
        self.hashFunction = params[0]
        self.characterSet = params[1]
        self.minPasswordLength = params[2]
        self.maxPasswordLength = params[3]
        self.tableIndex = params[4]
        self.chainLength = int(params[5])
        self.numberOfChains = params[6]
        self.tablePartIndex = params[7]
        self.tableFormat = params[8]

    def __str__(self):
        description = "Hash Function: {0}\nCharacterSet: {1}\nMin Password Length: {2}\nMax Password Length: {3}\nTable Index: {4}\nChain Length: {5}" \
               "\nNumber of Chains: {6}\nTable Part Index: {7}\nTable Format: {8}"
        return description.format(self.hashFunction, self.characterSet, self.minPasswordLength, self.maxPasswordLength, self.tableIndex, self.chainLength, self.numberOfChains, self.tablePartIndex, self.tableFormat)