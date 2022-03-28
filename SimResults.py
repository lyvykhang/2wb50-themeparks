class SimResults:
    def __init__(self):
        self.qLengths = [[] for i in range(4)]
        self.eventTimes = [[] for i in range(4)]
        self.waitingTimes = [[] for i in range(4)]
        self.unableToBoard = []
    
    def registerQLength(self, value, t, station):
        self.qLengths[station].append(value)
        self.eventTimes[station].append(t)
        
    def registerWaitingTime(self, customer, t):
        self.waitingTimes[customer.arrStation].append(t - customer.arrTime)
    
    def registerUnableToBoard(self, value):
        self.unableToBoard.append(value)
