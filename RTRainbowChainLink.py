__author__ = 'scottomalley'

class RTRainbowChainLink:

    def __init__(self, hash, plainText, index):
        self.hash = hash.encode("utf-8")
        self.plainText = plainText
        self.index = index

    def __str__(self):
        return "Plain Text: {0}\nHash: {1}\nDecimal Index:{2}".format(self.plainText, self.hash, self.index)
