class Event:
    ARRIVAL_CUST = 0
    ARRIVAL_TRAIN = 1
    DEPARTURE_TRAIN = 2

    def __init__(self, typ, time, station, train=None, cust=None):
        self.type = typ
        self.time = time
        self.station = station
        self.train = train
        self.cust = cust
    
    def __lt__(self, other):
        return self.time < other.time
