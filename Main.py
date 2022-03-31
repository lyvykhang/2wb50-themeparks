from Sim import Sim
import numpy as np
from scipy.stats import t
from timeit import default_timer as timer

# sim = Sim()
# results = sim.sim(8, [2,2,2,2,2,2,2,2])
# print([np.mean(subarray) for subarray in results.qLengths])
# print([np.mean(subarray) for subarray in results.waitingTimes])
#print([np.mean(subarray) for subarray in results.qLengths])
#print(results.waitingTimes)

def getConfidenceInterval(array):
    confidence = 0.95
    m = array.mean() # mean
    s = np.array(array).std() # standard deviation
    dof = len(array)-1 # degrees of freedom
    t_crit = np.abs(t.ppf((1-confidence)/2, dof)) # calculate t_crit using inverse cdf 
    return (round((m-s*t_crit/np.sqrt(len(array))), 2), round((m+s*t_crit/np.sqrt(len(array))), 2))

def doRuns(N, trains, cars):
    runsQLengths = []
    runsMeanQLengths = []

    runsWaitingTimes = []
    runsMeanWaitingTimes = []

    runsEventTimes = []
    
    for i in range(N):
        sim = Sim()
        results = sim.sim(trains, cars)
        runsQLengths.append(results.qLengths)
        runsMeanQLengths.append([np.mean(subarray) for subarray in results.qLengths])

        runsWaitingTimes.append(results.waitingTimes)
        runsMeanWaitingTimes.append([np.mean(subarray) for subarray in results.waitingTimes])

        runsEventTimes.append(results.eventTimes)
    
    runsMeanQLenghtsPerStation = np.array(runsMeanQLengths).transpose()
    for i, means in enumerate(runsMeanQLenghtsPerStation):
        print(f"Mean Q Length Station: {i+1}")
        print(np.mean(means))
        print(getConfidenceInterval(means))

    runsMeanWaitingTimesPerStation = np.array(runsMeanWaitingTimes).transpose()
    for i, waitingTimes in enumerate(runsMeanWaitingTimesPerStation):
        print(f"Mean Waiting Time Station: {i+1}")
        print(np.mean(waitingTimes))
        print(getConfidenceInterval(waitingTimes))

start = timer()
doRuns(3, 8, [2,2,2,2,2,2,2,2])
print(timer() - start)