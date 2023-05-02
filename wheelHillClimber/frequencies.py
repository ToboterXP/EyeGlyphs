
import random
import re
import math

ALPHABET = None #the alphabet of the current language

NGRAM_SCORE_DIVIDER_GROWTH = 100

LANGUAGE = "E" #F for finnish, E for english

WORD_STARTS = " \"-"
WORD_ENDS = " ,.:;!?\""
USE_WORD_DELIMITERS = False

if LANGUAGE == "E":
    NGRAM_FILES = (("english_quintgrams.txt",5),)#,("english_quadgrams.txt",4),("english_trigrams.txt",3),("english_bigrams.txt",2))   #the files with ngram frequencies
    WORD_FILE = "anagram_dictionary.txt"    #the file with the words
    CHARACTER_FILE = "english_monograms.txt"    #the file with monogram frequencies
    FILE_SEP = " "

##elif LANGUAGE == "EP":
##    NGRAM_LENGTH = 5    #the length of the ngrams
##    NGRAM_FILE = "english_quintgram_punctuation.txt"   #the file with ngram frequencies
##    WORD_FILE = "anagram_dictionary.txt"    #the file with the words
##    CHARACTER_FILE = "english_monograms_punctuation.txt"    #the file with monogram frequencies
##    FILE_SEP = "$$"
##    USE_WORD_DELIMITERS = True
##
##    
##elif LANGUAGE == "F":
##    NGRAM_LENGTH = 4
##    NGRAM_FILE = "finnish_quadgrams.txt"
##    WORD_FILE = "finnish_words.txt"
##    CHARACTER_FILE = "finnish_monograms.txt"
##    FILE_SEP = " "


RANDOM_NULL_CHANCE = 0 #chance that a random character for the homophonic key is a null (empty char)
IGNORE_OVERLAPPING_WORDS = True #if two words overlap, only count the longer one


#ngrams are stored in a dict, with their frequencies as value
NGRAMS = []

if not NGRAMS:
    print("Loading n-grams...")
    for NGRAM_FILE, ngramSize in NGRAM_FILES:
        NGRAMS.append(({},ngramSize))
        with open(NGRAM_FILE, "r") as f:
            line = f.readline()
            while line:
                qgram, freq = line.replace("Ã„","Ä").replace("Ã–","Ö").replace("Ã…","Å").split(FILE_SEP)
                NGRAMS[-1][0][qgram] = int(freq)
                line = f.readline()
        print(f"Loaded {len(NGRAMS[-1][0].keys())} ngrams size {ngramSize}")

#words are stored in a list, sorted largest to smallest, and a hash set (currently only hash set is used)
#words of length one are ignored, there are too many of those
WORDS = []
WORD_SET = set()

if not WORDS:
    print("Loading words...")
    with open(WORD_FILE, "r") as f:
        line = f.readline()
        while line:
            word = line.replace("Ã„","Ä").replace("Ã–","Ö").replace("Ã…","Å").replace("\n","").split(FILE_SEP)[0].upper()
            if len(word)>1:
                WORDS.append(word)
                WORD_SET.add(word)
            line = f.readline()

    WORDS.sort(key = lambda a: len(a), reverse=True)
    print(f"Loaded {len(WORDS)} words")

#monograms are stored as a list of (char, frequency) pairs. Used to properly randomize the homophonic key
CHAR_SUM = 0
CHARACTERS = []
if not CHARACTERS:
    print("Loading characters...")
    with open(CHARACTER_FILE, "r") as f:
        line = f.readline()
        while line:
            char, freq = line.replace("Ã„","Ä").replace("Ã–","Ö").replace("Ã…","Å").split(FILE_SEP)
            CHAR_SUM += int(freq)
            CHARACTERS.append([char, int(freq)])
            line = f.readline()
            
    ALPHABET = list(map(lambda a:a[0], CHARACTERS)) #create the ALPHABET based on the CHARACTERS
    print(f"Loaded {len(ALPHABET)} characters")


#get a random character, weighted by the monogram probabilities, or a null 
def getRandomChar(rng):
    i = rng.randint(0, CHAR_SUM)

    if random.random() < RANDOM_NULL_CHANCE:
        return ""

    for c, f in CHARACTERS:
        i -= f
        if i <= 0:
            return c





#evaluate any character sequence based on the frequencies of its ngrams
def evaluateBasedOnNGramSet(sequence, ngrams, ngramLength):
    score = 0
    for i in range(len(sequence) - ngramLength + 1):
        score += ngrams.get(sequence[i : i+ngramLength], 0)**2#//(i+1)
    return score

def evaluateBasedOnNGrams(sequence):
    score = 0
    divider = 1
    for ngrams,ngramLength in NGRAMS:
        score += evaluateBasedOnNGramSet(sequence, ngrams, ngramLength)#**2//divider
        divider *= NGRAM_SCORE_DIVIDER_GROWTH
    return score
        
        


#evaluate any character sequence based on what proportion of it is made up of actual words
def evaluateBasedOnWords(sequence,printSeq=False):
    score = 0

    if USE_WORD_DELIMITERS:
        for wordSize in range(len(sequence), 2, -1):
            for start in range(len(sequence)- wordSize + 1):
                w = sequence[start : start + wordSize]
                
                if not "@" in w and w[0] in WORD_STARTS and w[-1] in WORD_ENDS and w[1:-1] in WORD_SET:
                    score += wordSize
                    if IGNORE_OVERLAPPING_WORDS:
                        sequence = sequence[:start+1] + "@"*(wordSize-2) + sequence[start + wordSize-1:]

    else:
        for wordSize in range(len(sequence), 0, -1):
            for start in range(len(sequence)- wordSize + 1):
                w = sequence[start : start + wordSize]
                
                if not "@" in w and w in WORD_SET:
                    score += wordSize
                    if IGNORE_OVERLAPPING_WORDS:
                        sequence = sequence[:start] + "@"*wordSize + sequence[start + wordSize:]
        
    if printSeq:
        print(sequence)
    return score/(len(sequence))


