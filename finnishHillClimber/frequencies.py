
import random
import re

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"

NGRAM_LENGTH = 4

NGRAMS = {}

if not NGRAMS:
    with open("finnish_quadgrams.txt", "r") as f:
        line = f.readline()
        while line:
            qgram, freq = line.replace("Ã„","Ä").replace("Ã–","Ö").replace("Ã…","Å").split(" ")
            NGRAMS[qgram] = int(freq)
            line = f.readline()

WORDS = []
WORD_SET = set()

if not WORDS:
    with open("finnish_words.txt", "r") as f:
        line = f.readline()
        while line:
            word = line.replace("Ã„","Ä").replace("Ã–","Ö").replace("Ã…","Å").split(" ")[0]
            if len(word)>1:
                WORDS.append(word)
                WORD_SET.add(word)
            line = f.readline()

    WORDS.sort(key = lambda a: len(a), reverse=True)


CHAR_SUM = 0
CHARACTERS = []
if not CHARACTERS:
    with open("finnish_monograms.txt", "r") as f:
        line = f.readline()
        while line:
            char, freq = line.replace("Ã„","Ä").replace("Ã–","Ö").replace("Ã…","Å").split(" ")
            CHAR_SUM += int(freq)
            CHARACTERS.append([char, int(freq)])
            line = f.readline()


def getRandomChar(rng):
    i = rng.randint(0, CHAR_SUM)

    if random.random() < 0.1:
        return ""

    for c, f in CHARACTERS:
        i -= f
        if i <= 0:
            return c




def evaluateBasedOnNGrams(sequence):
    score = 0
    for i in range(len(sequence) - NGRAM_LENGTH + 1):
        score += NGRAMS.get(sequence[i : i+NGRAM_LENGTH], 0)
    return score


def evaluateBasedOnWords(sequence):
    score = 0
    for wordSize in range(len(sequence), 0, -1):
        for start in range(len(sequence)- wordSize + 1):
            w = sequence[start : start + wordSize]
            if not "@" in w and w in WORD_SET:
                score += wordSize*wordSize
                sequence = sequence[:start] + "@"*wordSize + sequence[start + wordSize:]
    return score/(len(sequence)**2)



def fullEvaluate(sequence):
    words = evaluateBasedOnWords(sequence)
    return words, (words) * evaluateBasedOnNGrams(sequence)
