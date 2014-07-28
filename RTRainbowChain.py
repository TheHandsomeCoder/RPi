__author__ = 'scottomalley'

class RTRainbowChain:

    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

    def __str__(self):
        return "Start Point: {0} \tEnd Point: {1}\n".format(self.start_point, self.end_point)
