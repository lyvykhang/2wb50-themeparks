class Train:
    def __init__(self, station, nCars, boarding):
        self.station = station
        self.capacity = 25*nCars
        self.custs = []
        self.boarding = boarding;
