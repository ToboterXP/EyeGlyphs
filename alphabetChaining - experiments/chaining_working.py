import json
import itertools
import math
import traceback
from dataclasses import dataclass

with open("atomicChains.json", "r") as f:
    atomicChains = json.load(f)



def getIsomorphName(isomorph):
    return (isomorph.count("."), len(isomorph))
##
##nameTest = set()
##for iso, s in atomicChains:
##    if getIsomorphName(iso) in nameTest:
##        print(f"Error: name collision {getIsomorphName(iso)}")
##    print(iso, getIsomorphName(iso))
##    nameTest.add(getIsomorphName(iso))


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
                pos = (offset + i * spread) % 83

                if pos >= len(sequence):
                    sequence += [None] * (pos - len(sequence) + 1)

                if sequence[pos] != None and sequence[pos] != chain.sequence[i]:
                    print(sequence)
                    raise ChainException(f"Collision of {chain} and {placements[pos]} in {self} on {sequence[pos]} and {chain.sequence[i]}")

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

    def getFlattened(self):
        return AlphabetChain(atomicChain = AtomicChain(isomorph = None, sequence = self.compiledSequence))

    def getForceSpread(self,newSpread):
        newChains = []

        if newSpread < 0:
            return self.getInverted().getForceSpread(-newSpread)
        
        for offset, spread, chain in self.atomicChains:
            newChains.append((offset * newSpread, spread * newSpread, chain))

        return AlphabetChain(atomicChains = newChains)

    def getForceMerged(self, other, mergeOffset):
        if mergeOffset < 0:
            return other.getForceMerged(self, -mergeOffset)

        newChains = self.atomicChains[:]
        for offset, spread, chain in other.atomicChains:
            new = (offset + mergeOffset, spread, chain)
            if not new in newChains:
                newChains.append(new)

        return AlphabetChain(atomicChains = newChains)

    def mergeOnSingleMatch(self, other): #ignores spread
        shared = []
        for c in self.compiledSequence:
            if c != None and c in other.compiledSequence:
                shared.append(c)

        if len(shared) < 1:
            return None

        return self.getForceMerged(other, self.compiledSequence.index(shared[0]) - other.compiledSequence.index(shared[0]))

    def merge(self, other, selfSpread, otherSpread, selfPivot, otherPivot):
        #print(self)
        #print(other)
        #print(selfPivot, otherPivot, selfSpread, otherSpread)
        newChains = []

        if otherSpread < 0:
            return self.merge(other.getInverted(), selfSpread, -otherSpread, selfPivot, len(other.compiledSequence) - otherPivot - 1)

        if selfSpread < 0:
            return self.getInverted().merge(other, -selfSpread, otherSpread, len(self.compiledSequence) - selfPivot - 1, otherPivot)

        
        otherOffset = selfPivot * selfSpread - otherPivot * otherSpread

        if otherOffset < 0:
            return other.merge(self, otherSpread, selfSpread, otherPivot, selfPivot)
        

        for offset, spread, chain in self.atomicChains:
            new = (offset, spread * selfSpread, chain)
            if not new in newChains:
                newChains.append(new)

        for offset, spread, chain in other.atomicChains:
            new = (offset + otherOffset, spread * otherSpread, chain)
            if not new in newChains:
                newChains.append(new)

        return AlphabetChain(atomicChains = newChains)
    

    def combine(self, other): #ignores possible matches for the inversion of other
        shared = []
        for c in self.compiledSequence:
            if c != None and c in other.compiledSequence:
                shared.append(c)

        if len(shared) < 2:
            return None

        possibleRelations = set() #contains (offsetOther, spreadOther, spreadSelf) for other in self

        for c1, c2 in itertools.combinations(shared, 2):
            if c1 != c2:
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

                exists = False
                for p in possibleRelations:
                    if p[0]-p[1] == i1self - i1other and p[2] == selfDiff and p[3] == otherDiff:
                        exists = True

                if exists:
                    continue

                possibleRelations.add((i1self, i1other, selfDiff, otherDiff))

                #possibleRelations.add((i1self - i1other, otherDiff, selfDiff))

        if not possibleRelations:
            return None

        possibleResult = []

        for relation in possibleRelations:
            selfPivot, otherPivot, otherSpread, selfSpread = relation
            
            try:
                possibleResult.append(self.merge(other, selfSpread, otherSpread, selfPivot, otherPivot))
            except:
                raise ChainException(f"Error merging {self} and {other} with {possibleRelations}")
##            newChains = []
##
##            otherOffset, otherSpread, selfSpread = relation
##            selfOffset = 0
##
##            if otherSpread < 0:
##                return self.combine(other.getInverted())
##
##            
##            if otherOffset < 0:
##                selfOffset = -otherOffset
##                otherOffset = 0
##            
##
##            for offset, spread, chain in self.atomicChains:
##                new = ((offset + selfOffset) * selfSpread, spread * selfSpread, chain)
##                if not new in newChains:
##                    newChains.append(new)
##
##            for offset, spread, chain in other.atomicChains:
##                new = ((offset + otherOffset) * otherSpread, spread * otherSpread, chain)
##                if not new in newChains:
##                    newChains.append(new)
##
##            try:
##                possibleResult.append(AlphabetChain(atomicChains = newChains))
##            except:
##                continue
##                #raise ChainException(f"Error merging {self} and {other} with {possibleRelations}")

        if len(possibleResult) != 1:
            raise ChainException(f"Error merging {self} and {other} with {possibleRelations}")
        return possibleResult[0]
            

    def __repr__(self):
        return f"[Alphabet Chain {self.compiledSequence} {self.atomicChains}]"


#badIsomorphs = ["AB......A.C.D.BD.CB", "A...A......B.....C...C..B", "AB...C...C......D.A...E...EB.D", "A.....BCD.ED.BE.CA..F....F"] #literally never work in chaining, last one sometimes works
badIsomorphs = ["AB......A.C.D.BD.CB", "A...A......B.....C...C..B", "AB...C...C......D.A...E...EB.D"]#, "A.BA..B"] #literally never work in chaining, last one sometimes works

#badIsomorphs.append("AB.CB..C.A.D....D")
#badIsomorphs.append("A........B.C.AC.BA") 
#badIsomorphs.append("A.BA..B.....C....C") 
#badIsomorphs.append("ABC.DC.AD.B.E....E") 
#badIsomorphs.append("AB.CB..C.A...D....D") 
#badIsomorphs.append("ABC.DC.AD.B...E....E") 
#badIsomorphs.append("A.....BCD.ED.BE.CAF....F") 
#badIsomorphs.append("A...B...B......C.....D...DA.C") 
#badIsomorphs.append("ABC..D...D......E.A...F...FB.EC.F") 

atomicChains = tuple(filter(lambda c: not c[0] in badIsomorphs, atomicChains))


foundChains = []

isomorphs = atomicChains[:]

chains = []
processedSequences = set()
for isomorph, iChains in isomorphs:
    for chain in iChains:
        if tuple(chain) in processedSequences:
            continue
        chains.append(AlphabetChain(atomicChain = AtomicChain(isomorph = isomorph, sequence = chain)))
        processedSequences.add(tuple(chain))

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


##for c in chains:
##    print(c.compiledSequence)
##print()

shareCounts = {}

for i in range(83):
    a = 0
    for c in chains:
        if i in c.compiledSequence:
            a+=1
    shareCounts[i] = a

chainShareValue = {}
for c in chains:
    a=0
    for i in c.compiledSequence:
        if i:
            a+=shareCounts[i]
    chainShareValue[c] = a


chains.sort(reverse=True, key=lambda c:chainShareValue[c])

for c1 in chains:
    excludes = set()
    for c2 in chains:
        i = tuple(set(c1.compiledSequence).intersection(c2.compiledSequence))
        if i:
            i = i[0]
        else:
            continue
        p1 = c1.compiledSequence.index(i)
        p2 = c2.compiledSequence.index(i)
        l1 = len(c1.compiledSequence)
        l2 = len(c2.compiledSequence)

        excludes.add(p2)
        excludes.add(l2-p2-1)
    if 0 in excludes:
        excludes.remove(0)
    print(c1.compiledSequence, max(excludes))



##messages = ((50, 66, 5, 48, 62, 13, 75, 29, 24, 61, 42, 70, 66, 62, 32, 14, 81, 8, 15, 78, 2, 29, 13, 49, 1, 80, 82, 40, 63, 81, 21, 19, 0, 40, 51, 65, 26, 14, 21, 70, 47, 44, 48, 42, 19, 48, 13, 47, 19, 49, 72, 31, 5, 24, 3, 43, 59, 67, 33, 49, 41, 60, 21, 26, 30, 5, 25, 20, 71, 11, 74, 56, 4, 74, 19, 71, 4, 51, 41, 43, 80, 72, 54, 63, 79, 81, 15, 16, 44, 31, 30, 12, 33, 57, 28, 13, 64, 43, 48), (80, 66, 5, 48, 62, 13, 75, 29, 24, 61, 42, 70, 66, 62, 32, 14, 81, 8, 15, 78, 2, 29, 13, 49, 1, 29, 11, 30, 52, 81, 21, 19, 0, 25, 26, 54, 20, 14, 21, 70, 47, 44, 48, 42, 19, 48, 13, 47, 19, 49, 44, 26, 59, 77, 64, 43, 79, 28, 72, 64, 1, 30, 73, 23, 67, 6, 33, 25, 64, 81, 68, 46, 17, 36, 13, 17, 21, 68, 13, 9, 46, 67, 57, 34, 62, 82, 15, 10, 73, 62, 2, 11, 65, 72, 37, 44, 10, 43, 68, 62, 9, 34, 18), (36, 66, 5, 48, 62, 13, 75, 29, 24, 61, 42, 70, 66, 62, 32, 14, 81, 8, 15, 78, 2, 29, 13, 49, 1, 69, 76, 52, 9, 48, 66, 80, 22, 64, 57, 40, 49, 78, 3, 16, 56, 19, 47, 40, 80, 6, 13, 64, 29, 49, 64, 63, 6, 49, 31, 13, 16, 10, 45, 24, 26, 77, 10, 60, 81, 61, 34, 54, 70, 21, 15, 4, 66, 77, 42, 37, 30, 22, 0, 11, 41, 72, 57, 20, 23, 57, 65, 41, 23, 18, 72, 42, 5, 3, 26, 78, 8, 5, 54, 45, 77, 25, 64, 61, 16, 44, 54, 51, 20, 63, 25, 11, 26, 45, 53, 60, 38, 34), (76, 66, 5, 49, 75, 54, 69, 46, 32, 1, 42, 60, 26, 48, 50, 80, 32, 24, 55, 61, 47, 12, 21, 12, 49, 54, 34, 25, 36, 15, 56, 55, 20, 9, 8, 62, 13, 82, 9, 44, 29, 60, 53, 82, 42, 80, 5, 43, 71, 3, 80, 77, 47, 78, 34, 25, 62, 18, 10, 49, 62, 64, 52, 81, 11, 66, 62, 13, 47, 17, 52, 70, 26, 23, 32, 31, 64, 23, 35, 32, 50, 6, 1, 25, 8, 37, 47, 43, 26, 76, 65, 68, 80, 17, 7, 45, 63, 14, 53, 63, 60, 16), (63, 66, 5, 49, 75, 54, 2, 60, 29, 40, 78, 47, 60, 75, 67, 71, 60, 2, 65, 7, 47, 14, 45, 74, 59, 41, 80, 13, 60, 13, 81, 22, 35, 50, 40, 39, 2, 59, 48, 31, 76, 2, 80, 75, 1, 56, 67, 11, 21, 8, 40, 65, 45, 75, 55, 39, 60, 42, 13, 3, 22, 57, 2, 6, 58, 9, 70, 1, 58, 56, 63, 68, 25, 79, 7, 20, 19, 64, 2, 66, 73, 30, 71, 16, 12, 30, 65, 37, 20, 13, 22, 63, 18, 46, 64, 59, 41, 81, 82, 22, 78, 36, 47, 17, 4, 6, 17, 5, 36, 79, 63, 1, 64, 69, 15, 43, 4, 58, 56, 31, 14, 64, 58, 18, 44, 78, 69, 1, 0, 46, 20, 71, 73, 25, 35, 8, 24), (34, 66, 5, 49, 75, 54, 23, 74, 11, 13, 28, 26, 19, 48, 67, 57, 37, 60, 34, 28, 74, 10, 17, 32, 11, 18, 19, 43, 19, 81, 42, 4, 62, 9, 46, 49, 32, 51, 76, 58, 4, 43, 47, 17, 67, 79, 21, 32, 44, 16, 30, 37, 26, 28, 41, 68, 57, 34, 51, 10, 69, 70, 8, 6, 46, 43, 18, 39, 47, 43, 15, 13, 33, 30, 35, 62, 37, 0, 37, 5, 38, 55, 37, 13, 40, 25, 9, 21, 11, 64, 5, 79, 42, 68, 11, 71, 11, 48, 3, 67, 61, 40, 22, 14, 35, 50, 61, 39, 11, 2, 66, 49, 51, 53, 17, 73, 36, 75, 74, 54, 24, 30, 54, 70), (27, 66, 5, 49, 75, 54, 2, 60, 29, 40, 2, 55, 9, 15, 59, 18, 68, 3, 36, 5, 47, 77, 44, 38, 1, 18, 28, 76, 4, 34, 60, 63, 58, 80, 17, 54, 79, 75, 48, 54, 55, 19, 62, 64, 14, 47, 51, 70, 75, 5, 11, 47, 45, 58, 68, 69, 79, 25, 38, 45, 73, 47, 68, 50, 34, 45, 78, 26, 79, 57, 4, 56, 22, 60, 18, 75, 43, 60, 59, 67, 63, 42, 49, 33, 40, 65, 79, 77, 7, 3, 26, 62, 31, 78, 26, 57, 69, 40, 4, 23, 26, 13, 67, 42, 38, 72, 11, 39, 65, 60, 25, 6, 80, 66, 68, 77, 59, 78, 19), (77, 66, 5, 49, 75, 54, 2, 60, 29, 40, 2, 55, 9, 15, 59, 18, 68, 3, 36, 5, 47, 60, 21, 80, 1, 72, 55, 16, 82, 35, 57, 19, 1, 66, 18, 27, 39, 17, 74, 81, 39, 14, 78, 0, 25, 65, 43, 66, 64, 38, 81, 23, 24, 50, 57, 30, 71, 75, 26, 68, 54, 57, 56, 50, 71, 73, 14, 21, 8, 32, 26, 63, 5, 37, 19, 43, 66, 47, 53, 34, 66, 23, 73, 31, 54, 38, 77, 67, 11, 63, 79, 6, 22, 21, 51, 69, 74, 21, 5, 17, 67, 37, 29, 21, 60, 14, 82, 44, 30, 4, 20, 42, 35, 1, 31, 54, 46, 20, 40, 30), (33, 66, 5, 49, 75, 54, 2, 60, 29, 40, 2, 55, 9, 15, 59, 18, 68, 3, 36, 5, 47, 33, 21, 59, 44, 18, 28, 76, 59, 34, 60, 63, 79, 27, 12, 54, 5, 49, 48, 54, 55, 52, 62, 72, 69, 10, 57, 22, 58, 48, 67, 53, 7, 34, 32, 30, 31, 19, 26, 8, 34, 46, 7, 30, 71, 55, 34, 75, 54, 9, 6, 60, 5, 23, 25, 45, 42, 80, 25, 12, 22, 76, 20, 51, 62, 21, 40, 9, 41, 10, 44, 73, 8, 33, 70, 73, 6, 31, 21, 72, 5, 40, 61, 51, 42, 66, 64, 74, 61, 25, 63, 42, 24, 41))
##
##
##chains = list(map(lambda c: c.getFlattened(), chains)) #flatten all chains, for easier debugging
##    
##with open("isomorphs.json", "r") as f:
##    isomorphs = json.load(f)
##
##processed = []
##newChains = []
##
##for c1 in chains:
##    sequence = c1.compiledSequence
##    for a1, a2 in itertools.combinations(sequence, 2):
##        for pattern, stuff in atomicChains:
##            for iso in isomorphs[pattern]:
##                isoPatt = iso[2]
##                if a1 in isoPatt and a2 in isoPatt:
##                    for iso2 in isomorphs[pattern]:
##                        iso2Patt = iso2[2]
##                        if iso2Patt != isoPatt:
##                            b1 = iso2Patt[isoPatt.index(a1)]
##                            b2 = iso2Patt[isoPatt.index(a2)]
##                            if b1 != b2:
##                                for c2 in chains:
##                                    if c1 != c2 and not {c1, c2} in processed:
##                                        sequence2 = c2.compiledSequence
##                                        if b1 in sequence2 and b2 in sequence2:
##                                            c1Diff = sequence.index(a2) - sequence.index(a1)
##                                            c2Diff = sequence2.index(b2) - sequence2.index(b1)
##
##                                            gcd = math.gcd(c1Diff, c2Diff)
##                                            c1Diff //= gcd
##                                            c2Diff //= gcd
##
##                                            processed.append({c1, c2})
##
##                                            offset = None
##
##                                            for t in sequence:
##                                                if t in sequence2:
##                                                    offset = sequence.index(t) - sequence2.index(t)
##                                                    break
##
##                                            print(sequence, pattern, sequence2, offset, c2Diff, c1Diff, isoPatt, iso2Patt, a1, a2, b1, b2)
##
##                                            #if offset != None:
##                                                #newChains.append(c1.merge(c2, c2Diff, c1Diff, sequence.index(t), sequence2.index(t)))

                                            
                            


        


                    
    
    
