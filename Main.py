from Sim import Sim
import numpy as np
import pandas as pd
from scipy.stats import t
from timeit import default_timer as timer

def dfToLatex(df, caption):
    df.columns = ['Train configuration', 'Mean Que Length', 'Mean Waiting Time', 'Costs']
    print("\\begin{table}[h!]")
    print("\\resizebox{\textwidth}{!}{")
    print(df.to_latex())
    print("}")
    print(f"\\caption{{{caption}}}")
    print("\\end{table}")

def doRun(trains, cars):
    sim = Sim()
    results = sim.sim(trains, cars, extra=0)
    meanQLength = np.mean([qLength for station in results.qLengths for qLength in station])
    meanWaitTime = np.mean([waitTime for station in results.waitingTimes for waitTime in station])
    costs = (800*trains) + (sum(cars)*500)
    return [cars, meanQLength, meanWaitTime, costs]

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
        results = sim.sim(trains, cars, extra=0)
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

df = pd.DataFrame(columns=['Train configuration', 'Mean Que Length', 'Mean Waiting Time', 'Costs'])
for i in range(6, 13):
    run = doRun(i, np.full(i, 1))
    df = df.append({"Train configuration": ', '.join(str(i) for i in run[0]), "Mean Que Length": run[1], "Mean Waiting Time": run[2], "Costs": run[3]}, ignore_index=True)
    run = doRun(i, np.full(i, 2))
    df = df.append({"Train configuration": ', '.join(str(i) for i in run[0]), "Mean Que Length": run[1], "Mean Waiting Time": run[2], "Costs": run[3]}, ignore_index=True)
    run = doRun(i, np.full(i, 3))
    df = df.append({"Train configuration": ', '.join(str(i) for i in run[0]), "Mean Que Length": run[1], "Mean Waiting Time": run[2], "Costs": run[3]}, ignore_index=True)
print(df.to_string())
dfToLatex(df, "Different configurations of trains and cars for explorative research, using a single number of simulation runs")

# For the picked configuration we should do doRuns() to get a confidence interval