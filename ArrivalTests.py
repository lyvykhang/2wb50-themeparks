from statistics import mean
from numpy.ma.core import asarray, append, mean, min, max
from scipy import stats
from scipy.constants import pi
import matplotlib.pyplot as plt

from collections import deque

from datetime import datetime
import time

# TODO: Implement this in Sim.py
# TODO: Implement other station arrays

# Array for projected customer arrival per hour for stations
frogPondArr = [450, 300, 275, 285, 310, 320, 280, 260, 290, 315, 385, 415]

def lam(t, stationArr):
    return stationArr[int(t/60)]/60

def simArrival(stationArr, T):
    # Function to do Poisson process to get arrival times for simulation
    lambdaMax = (max(stationArr))/60

    arrivalTimes = deque()
    expDist = stats.expon(scale=1/lambdaMax)
    udist = stats.uniform(0, 1)
    t = expDist.rvs()

    while t < T:
        if udist.rvs() < lam(t, stationArr)/lambdaMax:
            arrivalTimes.append(t)
        t += expDist.rvs()

    return asarray(arrivalTimes)

# def thinning(allArrivals, stationArr):
#     # Function to make the Poisson process non-homogeneous matching the projected customer arrival per hour
#     stationArr = [x / max(stationArr) for x in stationArr]
#     return [(stationArr[int(t/60)]) for t in allArrivals]

def generatePlot(arr):
    # Generate plot mostly copied from lecture notes
    ys = range(0, len(arr) + 1)
    ys = append(ys, [len(arr)])
    xs = append(append([0], arr), [T])
    plt.figure()
    plt.step(xs, ys, 'b', where='post')
    date = datetime.now().strftime("%Y%m%d_%H%M%S")
    plt.savefig("results_{0}.png".format(date))
    plt.clf()

T = 720
# # All Arrivals is homogeneous
# allArrivals = simArrival(frogPondArr, T)

# # The next steps are here to make it non-homogeneous
# udist = stats.uniform(0, 1)
# u = udist.rvs(len(allArrivals))
# maxLam = 1 # I am unsure what this value should be currently, it heavily impacts the amount of accepted arrivals
# accept = u * maxLam < thinning(allArrivals, frogPondArr)
# acceptedArrivals = allArrivals[accept]
acceptedArrivals = simArrival(frogPondArr, T)

# generatePlot(allArrivals)
time.sleep(1)
generatePlot(acceptedArrivals)
