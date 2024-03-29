from collections import deque
from scipy import stats
import numpy as np

from FES import FES
from Train import Train
from Event import Event
from SimResults import SimResults
from Customer import Customer

class Sim:
    # travel times between each stations
    travelTimes = [5, 8, 7, 6]

    # projected customer arrivals (arrivals per hour)
    lambdas = [[450, 300, 275, 285, 310, 320, 280, 260, 290, 315, 385, 415], \
        [400, 350, 250, 275, 290, 305, 300, 280, 310, 320, 360, 405], \
        [325, 340, 260, 210, 240, 280, 290, 275, 295, 330, 395, 430], \
        [385, 320, 280, 265, 290, 315, 300, 320, 280, 310, 360, 395]]


    def lam(self, t, stationArr):
        return stationArr[int(t/60)]/60


    def simArrival(self, stationArr, T):
        # Function to do Poisson process to get arrival times for simulation
        lambdaMax = (max(stationArr))/60

        arrivalTimes = deque()
        expDist = stats.expon(scale=1/lambdaMax)
        udist = stats.uniform(0, 1)
        t = expDist.rvs()

        while t < T:
            if udist.rvs() < self.lam(t, stationArr)/lambdaMax:
                arrivalTimes.append(t)
            t += expDist.rvs()

        return np.ma.core.asarray(arrivalTimes)


    def sim(self, nTrains, nCars, extra=None):
        # set the trains such that the customers cannot board yet
        trains = [Train(i % 4, nCars[i], False) for i in range(nTrains)]
        fes = FES()
        t = 0
        qCust, qTrain = [[] for i in range(4)], [[] for i in range(4)]
        results = SimResults()
    
        for train in trains: # schedule initial train "arrivals".
            if extra:
                fes.add(Event(Event.ARRIVAL_TRAIN_OFF, t, train.station, train=train))
            else:
                fes.add(Event(Event.ARRIVAL_TRAIN, t, train.station, train=train))

        for idx, station in enumerate(self.lambdas): # pre-schedule all customer arrivals from the start.
            for arr in self.simArrival(station, 720):
                fes.add(Event(Event.ARRIVAL_CUST, arr, idx, cust=Customer(arr, idx)))

        while(True): # Run untill break clause is triggered
            e = fes.next()
            t = e.time

            if not extra: # the simulation is run without the extra features
                if (e.type == Event.ARRIVAL_CUST):
                    cust = e.cust
                    qCust[e.station].append(cust)

                    if (len(qTrain[e.station]) > 0 and t < 720): # there is a train at the platform and t is less than 720
                        train = qTrain[e.station][0]
                        if (qCust[e.station][0] == cust and len(train.custs) < train.capacity): # customer is at head of q and train is not full.
                            train.custs.append(cust) # then they can immediately board the train.
                            qCust[e.station].remove(cust)
                            results.registerWaitingTime(cust, t)

                    results.registerQLength(len(qCust[e.station]), t, e.station)

                elif (e.type == Event.ARRIVAL_TRAIN):
                    train = e.train
                    train.station = e.station
                    qTrain[e.station].append(train)

                    if qTrain[e.station][0] == train: # there is no other train at the platform.
                        off = [cust for cust in train.custs if cust.deptStation == e.station] # offload customers who want to get off at this station.
                        train.custs = [cust for cust in train.custs if cust not in off]

                        if t < 720: # do not fill if t is not less than 720
                            remainingCapacity = train.capacity - len(train.custs)
                            on = qCust[e.station][:remainingCapacity] # fill train to min(current q length, remaining capacity).
                            for cust in on:
                                train.custs.append(cust)
                                qCust[e.station].remove(cust)
                                results.registerWaitingTime(cust, t)
                            results.registerQLength(len(qCust[e.station]), t, e.station) 

                        fes.add(Event(Event.DEPARTURE_TRAIN, t + 2, e.station, train=train))
                        
                elif (e.type == Event.DEPARTURE_TRAIN):
                    train = e.train
                    qTrain[e.station].remove(train)
                    results.registerUnableToBoard(len(qCust[e.station])>0)
                    fes.add(Event(Event.ARRIVAL_TRAIN, t + self.travelTimes[e.station], (e.station + 1) % 4, train=train))

                    if len(qTrain[e.station]) > 0: # there is another train waiting to offload at this station.
                        nextTrain = qTrain[e.station][0]
                        off = [cust for cust in nextTrain.custs if cust.deptStation == e.station]
                        nextTrain.custs = [cust for cust in nextTrain.custs if cust not in off]

                        if t < 720: # do not fill if t is not less than 720
                            remainingCapacity = nextTrain.capacity - len(nextTrain.custs)
                            on = qCust[e.station][:remainingCapacity]
                            for cust in on:
                                nextTrain.custs.append(cust)
                                qCust[e.station].remove(cust)
                                results.registerWaitingTime(cust, t)
                            results.registerQLength(len(qCust[e.station]), t, e.station)

                        fes.add(Event(Event.DEPARTURE_TRAIN, t + 2, e.station, train=nextTrain))
            else: # the simulation is run with the extra features
                if (e.type == Event.ARRIVAL_CUST):
                    cust = e.cust
                    qCust[e.station].append(cust)

                    if (len(qTrain[e.station]) > 0 and t < 720): # there is a train at the platform and t is less than 720
                        train = qTrain[e.station][0]
                        if (qCust[e.station][0] == cust and len(train.custs) < train.capacity): # customer is at head of q and train is not full.
                            if train.boarding:
                                train.custs.append(cust) # then they can immediately board the train.
                                qCust[e.station].remove(cust)
                                results.registerWaitingTime(cust, t)

                    results.registerQLength(len(qCust[e.station]), t, e.station)

                elif (e.type == Event.ARRIVAL_TRAIN_OFF):
                    train = e.train
                    train.station = e.station
                    train.boarding = False;
                    qTrain[e.station].append(train)

                    if qTrain[e.station][0] == train: # there is no other train at the platform.
                        off = [cust for cust in train.custs if cust.deptStation == e.station] # offload customers who want to get off at this station.
                        train.custs = [cust for cust in train.custs if cust not in off]

                        fes.add(Event(Event.ARRIVAL_TRAIN_ON, t + 0.5, e.station, train=train))

                elif (e.type == Event.ARRIVAL_TRAIN_ON):
                    train = e.train
                    train.station = e.station
                    train.boarding = True;

                    if t < 720: # do not fill if t is not less than 720
                        remainingCapacity = train.capacity - len(train.custs)
                        on = qCust[e.station][:remainingCapacity] # fill train to min(current q length, remaining capacity).
                        for cust in on:
                            train.custs.append(cust)
                            qCust[e.station].remove(cust)
                            results.registerWaitingTime(cust, t)
                        results.registerQLength(len(qCust[e.station]), t, e.station) 

                    fes.add(Event(Event.DEPARTURE_TRAIN, t + 0.75, e.station, train=train))
                        
                elif (e.type == Event.DEPARTURE_TRAIN):
                    train = e.train
                    train.boarding = False;
                    qTrain[e.station].remove(train)
                    results.registerUnableToBoard(len(qCust[e.station])>0)
                    fes.add(Event(Event.ARRIVAL_TRAIN_OFF, t + self.travelTimes[e.station], (e.station + 1) % 4, train=train))

                    if len(qTrain[e.station]) > 0: # there is another train waiting to offload at this station.
                        nextTrain = qTrain[e.station][0]

                        off = [cust for cust in nextTrain.custs if cust.deptStation == e.station]
                        nextTrain.custs = [cust for cust in nextTrain.custs if cust not in off]

                        #schedule the arrival of the train waiting in the queue at that station 30s later
                        fes.add(Event(Event.ARRIVAL_TRAIN_ON, t + 0.5, e.station, train=nextTrain)) 
        

            # If t is after 720 check if all trains are empty
            if (t > 720):
                done = True
                for train in trains:
                    if (len(train.custs) > 0):
                        done = False
                        break # break for loop
                if done:
                    break # break while loop
            
        return results
