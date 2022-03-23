class SimResults:
    def __init__(self):
        self.qLengths = [[] for i in range(4)]
    
    def registerQLength(self, value, station):
        self.qLengths[station].append(value)
