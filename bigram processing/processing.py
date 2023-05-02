

def loadNgrams(fileName):
    total = 0
    ngramDict = {}
    with open(fileName) as f:
        for line in f.readlines():
            ngram, count = line.split(" ")
            count = int(count)
            total += count
            ngramDict[ngram] = count

    retDict = {}
    for ngram in ngramDict.keys():
        retDict[ngram] = ngramDict[ngram] / total

    return retDict


for file in ("finnish_bigrams.txt", "english_bigrams.txt"):
    ngrams = loadNgrams(file)
    doubleChance = 0
    for ngram in ngrams.keys():
        if ngram[0] == ngram[1]:
            doubleChance += ngrams[ngram]

    print(file, doubleChance)
