from frequencies import evaluateBasedOnNGrams, evaluateBasedOnWords, getRandomChar, fullEvaluate, ALPHABET
from messages import messages
from multiprocessing import Pool, freeze_support
import random
import os
import time

KEY_LENGTH = 29

STEPS_TILL_REVERT = 2000
CHARS_PER_REROLL = 2
STEPS_TILL_FINNISHED = 20000

MAX_STEPS = 100

PROC_COUNT = os.cpu_count()


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



rng = random.Random()
currentKey = []
for i in range(KEY_LENGTH):
    currentKey.append(getRandomChar(rng))



currentKey = list(ALPHABET)
random.shuffle(currentKey)
    

def evaluateKey(key):
    score = 0
    ws = 0
    for m in messages:
        s = ""
        for c in m:
            s += key[c]
        w, e = fullEvaluate(s)
        score += e
        ws += w
    return ws/len(messages), score

def evaluateKeyWithWords(key):
    score = 0
    fs = ""
    for m in messages:
        s = ""
        for c in m:
            s += key[c]
        fs += s
    return evaluateBasedOnWords(s)


def checkBasedOn(key, score):

    currentKey = key[:]

    currentBestWordScore = score
    currentScore = score

    currentBestKey = currentKey[:]

    stepsSinceImprovement = 0
    stepsSinceRevert = 0
    steps = 0

    rng = random.Random()


    while stepsSinceImprovement <= STEPS_TILL_FINNISHED and steps <= MAX_STEPS:
        for i in range(CHARS_PER_REROLL):
            #currentKey[random.randint(0,KEY_LENGTH-1)] = getRandomChar(rng)
            i1 = random.randint(0,KEY_LENGTH-1)
            i2 = random.randint(0,KEY_LENGTH-1)
            currentKey[i1], currentKey[i2] = currentKey[i2], currentKey[i1]

        wordsScore, newScore = evaluateKey(currentKey)

        if newScore > currentScore:
            currentScore = newScore
            currentBestKey = currentKey[:]
            currentBestWordScore = wordsScore
            stepsSinceImprovement = 0
            stepsSinceRevert = 0

        else:
            stepsSinceImprovement += 1
            stepsSinceRevert += 1
            if stepsSinceRevert >= STEPS_TILL_REVERT:
                stepsSinceRevert = 0
                currentKey = currentBestKey[:]

        steps += 1

    return currentBestKey, currentScore



if __name__=="__main__":
    with Pool(PROC_COUNT) as pool:

        currentScore = evaluateKey(currentKey)[1]

        print(f"Starting on {PROC_COUNT} processes...")
        while True:
            startTime = time.time()
            newBests = pool.starmap(checkBasedOn, [(currentKey, currentScore)]*PROC_COUNT)

            print("\nProcessing Time:", time.time()-startTime,"seconds")
            for k, s in newBests:
                if s > currentScore:
                    currentScore = s
                    currentKey = k

            msg = "\n" + f"Score: {currentScore}\n" + "Best solution:\n"

            msg += str(currentKey)+"\n\n"
            for m in messages:
                for c in m:
                    msg += currentKey[c]
                msg += "\n\n"



            msg+= "Word value: "
            msg += str(evaluateKeyWithWords(currentKey))

            print(msg)
            with open("progress.txt", "w") as f:
                f.write(msg)
