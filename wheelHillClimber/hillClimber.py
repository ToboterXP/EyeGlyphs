#Eye cipher hill climber
#by Toboter
#
#Under GPL v2 License
#

from frequencies import evaluateBasedOnNGrams, evaluateBasedOnWords, getRandomChar, ALPHABET
from messages import messages
from multiprocessing import Pool, freeze_support
import random
import math
import os
import time

KEY_LENGTH = 83     #how long is the homophonic cipher key?


MIN_SWAPS = 1 #minimum numbers of swaps attempted each randomization
MAX_SWAPS = 8 #maximum numbers of swaps attempted each randomization

MAX_STEPS = 400    #how many hillclimbing steps should be done every multi-processing iteration
STEPS_TILL_REVERT = MAX_STEPS     #how many unsuccesful hill-climbing steps till a solving process reverts to the last succesful result
MAX_ITERATIONS_TILL_REVERT = 10 #how many unsuccessful iterations till it gets reverted one step


PROC_COUNT = os.cpu_count() #how many solving processes?


#print proper exception tracebacks in the solving processes
import traceback, functools, multiprocessing

def trace_unhandled_exceptions(func):
    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            print ('Exception in '+func.__name__)
            traceback.print_exc()
    return wrapped_func


#full cipher key
class Key:
    def __init__(self):
        self.outerWheel = []
        self.innerWheel = []

    def copy(self):
        ret = Key()
        ret.outerWheel = self.outerWheel[:]
        ret.innerWheel = self.innerWheel[:]
        return ret

    def __str__(self):
        return f"{self.innerWheel}, {self.outerWheel}"


#generate a random starter key
rng = random.Random()

outerW = list(range(83))
#random.shuffle(outerW)

innerW = 3*ALPHABET+list("_"*(83-3*len(ALPHABET)))
random.shuffle(innerW)

currentKey = Key()
currentKey.outerWheel = outerW
currentKey.innerWheel = innerW



#decode a message using a key
def decodeMessage(m, key):
    s = ""

    #outerWheelReverse = [0]*83
    #for i in range(83):
        #outerWheelReverse[key.outerWheel[i]] = i
        
    offset = 0
    for tri in m:
        #i = outerWheelReverse[tri]
        i = key.outerWheel.index(tri)
        char = key.innerWheel[ (i-offset)%83 ]
        offset += 1
        s += char
           
    return s

    
#evaluation a key based on the ngram distributions  in the decoded messages
def evaluateKey(key):
    score = 0
    
    for m in messages:
        s = decodeMessage(m, key)
        e = evaluateBasedOnNGrams(s)
        score += e**2
    return score


#evaluate a key based on word occurences in the decoded eye messages
def evaluateKeyWithWords(key,printSeq=False):
    score = 0
    fs = ""
    for m in messages:
        s = decodeMessage(m, key)
        fs += s
    return 1+ evaluateBasedOnWords(fs,printSeq)


#the function inside every solver process
def checkBasedOn(key, score):

    currentKey = key.copy() #the current key

    currentScore = score #the score of the current best key

    currentBestKey = currentKey.copy() #the current best key

    stepsSinceRevert = 0 #how long the solver has gone without an improvement
    steps = 0 #how long the solver has gone

    rng = random.Random()


    while steps <= MAX_STEPS:

        maxSwaps_inner = MAX_SWAPS

        while random.random() < 0.1 and maxSwaps_inner < 80:
            maxSwaps_inner *= 2

##        maxSwaps_outer = MAX_SWAPS
##
##        while random.random() < 0.1 and maxSwaps_outer < 80:
##            maxSwaps_outer *= 2
##
##        #swap a random number of outer wheel positions    
##        for i in range(rng.randint(MIN_SWAPS,maxSwaps_outer)):
##            a = rng.randint(0,82)
##            b = rng.randint(0,82)
##            currentKey.outerWheel[a], currentKey.outerWheel[b] = currentKey.outerWheel[b], currentKey.outerWheel[a]

        #swap a random number of inner wheel positions    
        for i in range(rng.randint(MIN_SWAPS,maxSwaps_inner)):
            a = rng.randint(0,82)
            b = rng.randint(0,82)
            currentKey.innerWheel[a], currentKey.innerWheel[b] = currentKey.innerWheel[b], currentKey.innerWheel[a]
            
                        
                
        #evaluate new key
        newScore = evaluateKey(currentKey)

        #if it's better than the best known one, replace that one
        if newScore > currentScore:
            currentScore = newScore
            currentBestKey = currentKey.copy()
            stepsSinceImprovement = 0
            stepsSinceRevert = 0

        #otherwise, continue on
        else:
            stepsSinceRevert += 1

            #and revert if it's going nowhere
            if stepsSinceRevert >= STEPS_TILL_REVERT:
                stepsSinceRevert = 0
                currentKey = currentBestKey.copy()

        steps += 1

    #return best result
    return currentBestKey, currentScore



if __name__=="__main__":

    keyHistory = [currentKey]
    currentRevertPivot = 0
    currentUnrevertThreshold = 0 #how much score must be exceeded to warrant ending the current revert?
    stepsSinceImprovement = 0
    
    with Pool(PROC_COUNT) as pool:

        #score the starter key
        currentScore = evaluateKey(currentKey)

        print(f"Starting on {PROC_COUNT} processes...")
        
        while True:
            startTime = time.time()

            #run the solvers for MAX_STEPS steps
            newBests = pool.starmap(checkBasedOn, [(currentKey, currentScore)]*PROC_COUNT)

            print("\nProcessing Time:", time.time()-startTime,"seconds")

            writeToFile = False
            
            #replace the current key with any better keys found
            improved = False
            for k, s in newBests:
                if s > currentScore:
                    currentScore = s
                    currentKey = k
                    improved = True

            if improved:
                keyHistory.append(currentKey)
                stepsSinceImprovement = 0
                if currentScore > currentUnrevertThreshold:
                    currentRevertPivot = len(keyHistory) - 2
                    currentUnrevertThreshold = currentScore
                    writeToFile = True
                    
            else:
                stepsSinceImprovement += 1
                if stepsSinceImprovement >= MAX_ITERATIONS_TILL_REVERT:
                    print("Revert to",currentRevertPivot)
                    stepsSinceImprovement = 0
                    keyHistory = keyHistory[:currentRevertPivot+1]
                    currentKey = keyHistory[-1]
                    currentScore = evaluateKey(currentKey)
                    currentRevertPivot -= 1
                    if currentRevertPivot < 0:
                        currentRevertPivot = 0
                

            #print feedback, and save it to "progress.txt"
            msg = "\n" + f"Score: {currentScore} ({len(str(currentScore))})\n" + "Best solution:\n"

            msg += str(currentKey)+"\n\n"
            for m in messages:
                msg += decodeMessage(m, currentKey)
                msg += "\n\n"



            #msg+= "Word value: "
            #msg += str(evaluateKeyWithWords(currentKey)-1)

            print(msg)
            if writeToFile:
                with open("progress.txt", "w") as f:
                    f.write(msg)

            #repeat till you get bored!
