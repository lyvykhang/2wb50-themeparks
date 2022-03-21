import numpy as np

class Sim:
    travelTimes = [5, 8, 7, 6]

    def sim(self, nTrains, nCars):
        trains = [Train(i % 4, nCars[i]) for i in range(nTrains)]
        fes = FES()
        t = 0
        qCust, qTrain = [[] for i in range(4)], [[] for i in range(4)]
        # results = SimResults()

        # schedule first customer arrival(s)
        # schedule initial train "arrivals"

        
        while(t < 720): # 60 minutes * 12 hours - placeholder: eventually this will be changed to "until the system is empty of customers"
            e = fes.next()
            t = e.time
            if (e.type == Event.ARRIVAL_CUST): # cust enters queue, schedule next cust arrival
                cust = e.cust
                qCust[e.station].append(cust)
                # TODO: still need to handle customer boarding train
                # schedule next customer arrival(s)

            elif (e.type == Event.DEPARTURE_CUST):
                cust = e.cust
                qCust[e.station].remove(cust)
                # TODO: still need to handle customer boarding train

            elif (e.type == Event.ARRIVAL_TRAIN):
                train = e.train
                train.station = e.station
                qTrain[e.station].append(train)

                if qTrain[e.station][0] == train:
                    off = [cust for cust in train.custs if cust.deptStation == e.station]
                    train.custs = [c for c in train.custs if c not in off]
                    fes.add(Event(Event.DEPARTURE_TRAIN, t + 2, e.station, train=train))

            elif (e.type == Event.DEPARTURE_TRAIN):
                train = e.train
                qTrain[e.station].remove(train)
                fes.add(Event(Event.ARRIVAL_TRAIN, t + self.travelTimes[e.station], (e.station + 1) % 4, train=train))

                if len(qTrain[e.station]) > 0:
                    nextTrain = qTrain[e.station][0]
                    off = [cust for cust in nextTrain.custs if cust.deptStation == e.station]
                    nextTrain.custs.remove(off)
                    fes.add(Event(Event.DEPARTURE_TRAIN, t + 2, e.station, train=nextTrain))
