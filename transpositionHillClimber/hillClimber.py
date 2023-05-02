#Homophonic and Transposition hill climber
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

TRANS_KEY_START_LENGTH = 1     #what length should the starter key for the transposition cipher have?
TRANS_KEY_MIN_LENGTH = 1    #what's the minimum size of the transposition key?
TRANS_KEY_MAX_LENGTH = 1   #what's the maximum size of the transposition key?

CHARS_PER_REROLL = 7        #how many chars in the homophonic key should be replaced every hill climbing step?
LARGER_REROLL_CHANCE = 0.1  #how big is the chance that larger sections of tehe homophonic and transposition keys get changed
                            #(to break out of local maxima)
TRANS_SWAPS_PER_REROLL = 0.2    #what proportion of the transposition key should get swapped around every hill climbing step
TRANS_SIZE_CHANGE_CHANCE = 0.1  #What's the chance that the size of the transposition key gets changed every step
TRANS_SIZE_CHANGE_MAGN_RANGE = (1,5)    #range of transposition size change

MAX_STEPS = 500    #how many hillclimbing steps should be done every multi-processing iteration
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
        self.hKey = None #key for homophonic cipher, maps 83 trigrams to alphabetical characters
        self.tKey = None #key for transposition cipher, maps each clear text position to a cipher text position

    def copy(self):
        ret = Key()
        ret.hKey = self.hKey[:]
        ret.tKey = self.tKey[:]
        return ret

    def __str__(self):
        return f"{self.hKey}, {self.tKey}"


#generate a random starter key
rng = random.Random()
hKey = []
for i in range(KEY_LENGTH):
    hKey.append(getRandomChar(rng))


tKey = list(range(TRANS_KEY_START_LENGTH))
random.shuffle(tKey)

currentKey = Key()
currentKey.hKey = hKey
currentKey.tKey = tKey



#decode a message using a key
def decodeMessage(m, key):
    s = ""

    sectionLength = len(key.tKey)

    for j in range(0, len(m), sectionLength):
        for k in range(sectionLength):
            i = j + key.tKey[k]
            if i < len(m):
                s += key.hKey[ m[i]]
                  
    return s

    
#evaluate a key based on the ngram distributions and word occurences in the decoded eye messages
def evaluateKey(key):
    score = 0
    
    for m in messages:
        s = decodeMessage(m, key)
        e = evaluateBasedOnNGrams(s)
        score += e
    return score #* (evaluateKeyWithWords(key))


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
        
        noLimit = random.random() < LARGER_REROLL_CHANCE #should a large reroll happen?
        
        #change homophonic key
        n = CHARS_PER_REROLL
        
        if noLimit: #if large reroll, reroll a random number of tris
            n = random.randint(0, len(currentKey.hKey))

        #replace the given number of chars in the homophonic key
        for i in range(n):
            currentKey.hKey[random.randint(0,KEY_LENGTH-1)] = getRandomChar(rng)

        #change transposition key

        #change the size of the transposition key
        if random.random() < TRANS_SIZE_CHANGE_CHANCE:

            #decide to make it smaller or larger
            if random.random() < 0.5 and len(currentKey.tKey) > TRANS_KEY_MIN_LENGTH or len(currentKey.tKey) == TRANS_KEY_MAX_LENGTH:
                
                #make trans key smaller
                for i in range(random.randint(*TRANS_SIZE_CHANGE_MAGN_RANGE)):
                    if len(currentKey.tKey) == TRANS_KEY_MIN_LENGTH:
                        break
                    currentKey.tKey.remove(max(currentKey.tKey))
                    
            else:
                #make trans key larger
                for i in range(random.randint(*TRANS_SIZE_CHANGE_MAGN_RANGE)):
                    if len(currentKey.tKey) == TRANS_KEY_MAX_LENGTH:
                        break
                    p = random.randint(0, len(currentKey.tKey)-1)
                    currentKey.tKey.insert(p, len(currentKey.tKey))

        #if the transposition key is longer than 1, swap some positions
        if len(currentKey.tKey) > 1:
            
            n = math.ceil(TRANS_SWAPS_PER_REROLL * len(currentKey.tKey))
            
            if noLimit: #if you do a large reroll, do lots of swaps
                n = random.randint(0, len(currentKey.tKey))
                
            for i in range(n):
                i1 = random.randint(0,len(currentKey.tKey)-1)
                i2 = i1
                while i2==i1:
                    i2 = random.randint(0,len(currentKey.tKey)-1)
                currentKey.tKey[i1], currentKey.tKey[i2] = currentKey.tKey[i2], currentKey.tKey[i1]
            
                        
                
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
                    currentUnrevertThreshold = currentScore
                    currentRevertPivot = len(keyHistory) - 2
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
            msg = "\n" + f"Score: {currentScore}\n" + "Best solution:\n"

            msg += str(currentKey)+"\n\n"
            for m in messages:
                msg += decodeMessage(m, currentKey)
                msg += "\n\n"



            msg+= "Word value: "
            msg += str(evaluateKeyWithWords(currentKey)-1)

            print(msg)
            with open("progress.txt", "w") as f:
                f.write(msg)

            #repeat till you get bored!
