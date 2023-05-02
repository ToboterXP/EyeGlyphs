import json
import itertools
import math
from dataclasses import dataclass

with open("atomicChains.json", "r") as f:
    atomicChains = json.load(f)



def getIsomorphName(isomorph):
    return (isomorph.count("."), len(isomorph))

nameTest = set()
for iso, s in atomicChains:
    if getIsomorphName(iso) in nameTest:
        print(f"Error: name collision {getIsomorphName(iso)}")
    print(iso, getIsomorphName(iso))
    nameTest.add(getIsomorphName(iso))


class ChainException(Exception):
    pass


@dataclass
class AtomicChain:
    isomorph : str
    sequence : list

    def __repr__(self):
        return f"[AtomicChain {self.isomorph} {self.sequence}]"

    def getInverted(self):
        return AtomicChain(isomorph = self.isomorph, sequence = self.sequence[::-1])

class AlphabetChain:
    def __init__(self, atomicChain = None, atomicChains=[]):
        if atomicChain:
            self.atomicChains = [(0,1,atomicChain)] #contains (offset, spread, atomicChain)
        else:
            self.atomicChains = atomicChains[:]
            

        self.compiledSequence = []
        self.compileSequence()

    def compileSequence(self):
        sequence = []

        placements = {} #contains pos : [atomicChains]

        for offset, spread, chain in self.atomicChains:
            for i in range(len(chain.sequence)):
                pos = offset + i * spread

                if pos >= len(sequence):
                    sequence += [None] * (pos - len(sequence) + 1)

                if sequence[pos] != None and sequence[pos] != chain.sequence[i]:
                    raise ChainException(f"Collision of {chain} and {placements[pos]} in {self}")

                sequence[pos] = chain.sequence[i]
                placements.setdefault(pos, [])
                placements[pos].append(chain)

        self.compiledSequence = tuple(sequence)

    def getInverted(self):
        newChains = []
        selfLen = len(self.compiledSequence)

        for offset, spread, chain in self.atomicChains:
            chainLen = (len(chain.sequence)-1) * spread + 1
            newChains.append((selfLen - offset - chainLen, spread, chain.getInverted()))

        return AlphabetChain(atomicChains = newChains)

    def getUsedIsomorphs(self):
        ret = set()

        for o, s, chain in self.atomicChains:
            ret.add(getIsomorphName(chain.isomorph))

        return ret
    

    def combine(self, other): #ignores possible matches for the inversion of other
        shared = []
        for c in self.compiledSequence:
            if c != None and c in other.compiledSequence:
                shared.append(c)

        if len(shared) < 2:
            return None

        possibleRelations = set() #contains (offsetOther, spreadOther, spreadSelf) for other in self

        for c1, c2 in itertools.combinations(shared, 2):
            i1self = self.compiledSequence.index(c1)
            i2self = self.compiledSequence.index(c2)
            i1other = other.compiledSequence.index(c1)
            i2other = other.compiledSequence.index(c2)

            selfDiff = i2self - i1self
            otherDiff = i2other - i1other
            if selfDiff < 0:
                selfDiff *= -1
                otherDiff *= -1

            gcd = math.gcd(selfDiff, otherDiff)
            selfDiff //= gcd
            otherDiff //= gcd

            possibleRelations.add((i1self - i1other, otherDiff, selfDiff))

        if not possibleRelations:
            return None

        possibleResult = []

        for relation in possibleRelations:
            newChains = []

            otherOffset, otherSpread, selfSpread = tuple(possibleRelations)[0]
            selfOffset = 0

            if otherSpread < 0:
                return self.combine(other.getInverted())

            
            if otherOffset < 0:
                selfOffset = -otherOffset
                otherOffset = 0
            

            for offset, spread, chain in self.atomicChains:
                newChains.append((offset + selfOffset, spread * selfSpread, chain))

            for offset, spread, chain in other.atomicChains:
                newChains.append((offset + otherOffset, spread * otherSpread, chain))

            try:
                possibleResult.append(AlphabetChain(atomicChains = newChains))
            except:
                continue
                #raise ChainException(f"Error merging {self} and {other} with {possibleRelations}")

        if len(possibleResult) != 1:
            raise ChainException(f"Error merging {self} and {other} with {possibleRelations}")
        return possibleResult[0]

    def __repr__(self):
        return f"[Alphabet Chain {self.atomicChains}]"


badIsomorphs = ["AB......A.C.D.BD.CB", "A...A......B.....C...C..B", "AB...C...C......D.A...E...EB.D", "A.....BCD.ED.BE.CA..F....F"] #literally never work in chaining, last one sometimes works

atomicChains = tuple(filter(lambda c: not c[0] in badIsomorphs, atomicChains))

foundChains = []

for ignoreLength in range(1, len(atomicChains), 1):
    print("New", ignoreLength)
    i=0
    for ignoreIsomorphs in itertools.combinations(atomicChains, ignoreLength):
        isomorphs = tuple(filter(lambda c: not c in ignoreIsomorphs, atomicChains[:]))

        #print(i)
        i += 1
        
        chains = []
        processedSequences = set()
        for isomorph, iChains in isomorphs:
            for chain in iChains:
                if tuple(chain) in processedSequences:
                    continue
                chains.append(AlphabetChain(atomicChain = AtomicChain(isomorph = isomorph, sequence = chain)))
                processedSequences.add(tuple(chain))

        if not chains:
            break

        try:
            while True:
                newChains = []
                newSequences = set()
                processed = set()
                for c1, c2 in itertools.combinations(chains, 2):
                    combined = c1.combine(c2)
                    if combined and not combined.compiledSequence in newSequences:
                        newChains.append(combined)
                        newSequences.add(combined.compiledSequence)
                        processed.add(c1)
                        processed.add(c2)

                for c in chains:
                    if not c in processed and not c.compiledSequence in newSequences:
                        newChains.append(c)
                        newSequences.add(c.compiledSequence)

                if not processed:
                    foundChains.append(newChains)
                    break

                chains = newChains
        except ChainException:
            continue

print(len(foundChains))

isoOccurences = {}

for iso, seqs in atomicChains:
    ocs = 0
    for chains in foundChains:
        for chain in chains:
            for o, s, aChain in chain.atomicChains:
                if aChain.isomorph == iso:
                    ocs += 1
                    break
            else:
                continue
            break
    isoOccurences[iso] =  ocs


isos = list(isoOccurences.keys())

isos.sort(reverse = True, key = lambda i: isoOccurences[i])

for iso in isos:
    print(iso, isoOccurences[iso])




##isomorphCombinations = set()
##
##for chains in foundChains:
##    comb = set()
##    for chain in chains:
##        comb.update(chain.getUsedIsomorphs())
##
##    comb = list(comb)
##    comb.sort(key=lambda a:a[1])
##    isomorphCombinations.add(tuple(comb))
##
##isomorphCombinations = list(map(lambda a: set(a), isomorphCombinations))
##
##isomorphCombinations.sort(key=lambda a: len(a))
##
##for comb in isomorphCombinations[:]:
##    for comb2 in isomorphCombinations[:]:
##        if len(comb2)>len(comb) and comb.issubset(comb2):
##            isomorphCombinations.remove(comb)
##            break
##
##isomorphCombinations = list(map(lambda a: list(a), isomorphCombinations))
##for l in isomorphCombinations:
##    l.sort(key=lambda a:a[1])
##
##
##print(isomorphCombinations)
    
    


        


                    
    
    
