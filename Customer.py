from random import choices

class Customer:
    departureProbs = [
    [0, 40, 35, 25], \
    [37, 0, 39, 24], \
    [42, 29, 0, 29], \
    [41, 28, 31, 0]]

    def __init__(self, arrTime, arrStation):
        self.arrTime = arrTime
        self.arrStation = arrStation
        self.deptStation = choices([0, 1, 2, 3], weights=self.departureProbs[arrStation])[0]
