
from timeit import default_timer as timer
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

import sys
import os

def parseArgs(argv):
    '''parse out Command line options.'''
    try:
        
        parser = ArgumentParser(description="a program to calculate Fibonacci's number", formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-m", "--max_number", dest="maxnumber", action="store", help="max value to calculate Fibonacci number [default: %(default)s]")
    
        # Process arguments
        args = parser.parse_args()
    
        global maxNumber

        maxNumber = args.maxnumber
        
        print("max Fibonacci number to calculate is <" + str(maxNumber) + ">")
        
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        print(e)
        
        
def timeSimpleVersusDynamicFibo(nMax):
    '''
    compare times for simple and dynamic methods to calculate Fibonacci's number
    return fibonacciTimes
    '''
    n=0
    fibonacciTimes=[]
    while n<nMax:
        print("--- " + str(n))
        simpleStartTime = timer()
        fibSimple(n)
        simpleEndTime = timer()     
           
        dynamicStartTime = timer()
        fibDynamic(n)
        dynamicEndTime = timer()   
        
        fibonacciTimes.append({"n":n, "simple": (simpleEndTime-simpleStartTime), "dynamic": (dynamicEndTime-dynamicStartTime) })
        n+=1
        
    return fibonacciTimes
    
def generateTimingPlot(fibonacciTimes, nmax):
    import seaborn as sns
    import matplotlib
    import pandas as pd
    import matplotlib.pyplot as plt
    
    dfFibonacciTimes = pd.DataFrame(fibonacciTimes)
    dfMelt = dfFibonacciTimes.melt(id_vars=['n'], value_vars=['simple','dynamic'])
    
    #sns.lineplot(data=dfMelt, x="n", y="simple", hue='variable')
    plt.xlabel("Fibonacci number")
    plt.ylabel("runtime (s)",)
    sns.scatterplot(data=dfMelt, x="n", y="value", hue='variable').set(title='Title of Plot')
    
    timingPlotFile = os.path.join(os.getcwd(), "fibonacci_timing_0_to_" + str(nmax) + ".png")
    
    plt.savefig(timingPlotFile)
    

def fibSimple(n):

    # base case
    if n == 0:
        return(0)
    if n == 1:
        return(1)
    
    # pattern:
    # ith = (i-1)th + (i-2)th
    return(fibSimple(n-1) + fibSimple(n-2))
    
    
def writeTimingDataToFile(fiboTimes, nmax):  
    import csv

    timingDataFile = os.path.join(os.getcwd(), "fibonacci_timing_0_to_" + str(nmax) + ".tsv")
    print("timing data will be written to <" + timingDataFile + ">")
    with open(timingDataFile, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['n', 'recursive', 'dynamic'])
        for timing in fiboTimes:
            writer.writerow(timing.values())    
    
    print("---done")
    
def fibDynamic(n):

    
    # base case
    if n == 0:
        return(0)
    if n == 1:
        savedFibNumbers[1] = 1
        return(1)
    
    if savedFibNumbers[n] != 0:
        return savedFibNumbers[n]
    
    savedFibNumbers[n] = fibDynamic(n -1) + fibDynamic(n - 2)

    return(savedFibNumbers[n])    
        

def main(argv=None): # IGNORE:C0111

    if argv is None:
        argv = sys.argv
    nmax = 25

    global savedFibNumbers
    savedFibNumbers=[0]*nmax


    
    fibonacciTimes = timeSimpleVersusDynamicFibo(nmax)
    writeTimingDataToFile(fibonacciTimes, nmax)
    generateTimingPlot(fibonacciTimes, nmax)
    
    
    parseArgs(argv)


    

if __name__ == '__main__':

    sys.exit(main())

