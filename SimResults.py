class SimResults:
    def __init__(self):
        self.qLengths = [[] for i in range(4)]
        self.eventTimes = [[] for i in range(4)]
    
    def registerQLength(self, value, t, station):
        self.qLengths[station].append(value)
        self.eventTimes[station].append(t)
