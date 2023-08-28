import json

with open("atomicChains.json", "r") as f:
    atomicChains = json.load(f)


chains = []

for iso in atomicChains:
    chains += iso[1]


def getDistance(alphabet, a, b):
    return (alphabet.index(b) - alphabet.index(a)) % 83



#returns value in [0,1]
def scoreAlphabet(alphabet):
    if not len(alphabet) in ():
        return -1
    for i in range(1,83):
        if not i in alphabet:
            return -1

    total = 0
    score = 0
    for chain in chains:
        if getDistance(alphabet, chain[0], chain[1]) == getDistance(alphabet, chain[1], chain[2]):
            score += 1
        total += 1

    return score/total


def getBestAlphabet(alphabetGenerator, bestCount=5):
    best = []
    for alphabet in alphabetGenerator:
        score = scoreAlphabet(alphabet)
        if score != -1:
            best.append((alphabet, score))
            best.sort(key=lambda a:a[1], reverse=True)
            if len(best) > bestCount:
                best.pop()

    return best




if __name__ == "__main__":
    def alphGen():
        for a in range(1, 83):
            print(a)
            for b in range(1, 83):
                yield [(a**i + b*i)%83 for i in range(83)]
    print(getBestAlphabet(alphGen()))
    
