class Event:
    ARRIVAL_CUST = 0
    ARRIVAL_TRAIN_OFF = 1
    ARRIVAL_TRAIN_ON = 2
    ARRIVAL_TRAIN = 3
    DEPARTURE_TRAIN = 4

    def __init__(self, typ, time, station, train=None, cust=None):
        self.type = typ
        self.time = time
        self.station = station
        self.train = train
        self.cust = cust
    
    def __lt__(self, other):
        return self.time < other.time
