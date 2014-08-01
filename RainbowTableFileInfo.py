__author__ = 'scottomalley'
import os

class RainbowChainInfo:
    """simplest version of rainbowtable file info"""


    def __init__(self, file, fileDirectory):
        self.fileLocation = fileDirectory + file
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
        self.minPasswordLength = int(params[2])
        self.maxPasswordLength = int(params[3])
        self.tableIndex = int(params[4])
        self.chainLength = int(params[5])
        self.numberOfChains = int(params[6])
        self.tablePartIndex = ""
        self.tableFormat = params[8]

    def formatName(self, count, newPartIndex):

        """md5_loweralpha-numeric-space#1-8_0_10000x67108864_distrrtgen[p][i]_00.rt"""
        "_#-__x_."
        return "{0}_{1}#{2}-{3}_{4}_{5}x{6}_{7}.{8}".format(self.hashFunction,self.characterSet,self.minPasswordLength,self.maxPasswordLength,self.tableIndex,self.chainLength,count, newPartIndex, self.tableFormat)

    def __str__(self):
        description = "Hash Function: {0}\nCharacterSet: {1}\nMin Password Length: {2}\nMax Password Length: {3}\nTable Index: {4}\nChain Length: {5}" \
               "\nNumber of Chains: {6}\nTable Part Index: {7}\nTable Format: {8}\nFile Location: {9}"
        return description.format(self.hashFunction, self.characterSet, self.minPasswordLength, self.maxPasswordLength, self.tableIndex, self.chainLength, self.numberOfChains, self.tablePartIndex, self.tableFormat, self.fileLocation)