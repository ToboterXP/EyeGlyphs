from dataclasses import dataclass
import itertools
import json

with open("isomorphs.json", "r") as f:
    isomorphs = json.load(f)


def genVariables():
    for i in range(100):
        for c in "abcdefghijklmnopqrstuvwxyz":
            if i==0:
                yield c
            else:
                yield c+str(i)


@dataclass
class ChainPair:
    c1: str
    c2: str
    distance: str
    iso1: str
    iso2: str

badIsomorphs = ["AB......A.C.D.BD.CB", "A...A......B.....C...C..B", "AB...C...C......D.A...E...EB.D", "A.B....A..B", "ABC..D...D......E.A...F...FB.EC.F", "A..BAC........B..DE.F....E.DF.C"]#, "A.BA..B"] #literally never work in chaining, last one sometimes works

chainPairs = []
varName = genVariables()

created = set()

variables = []


for iso in isomorphs.keys():
    #if not iso in badIsomorphs: or iso=="A.B....A..B"  
    if iso == "A.BA..B"  or iso=="AB..C...A.DEF.BF.DB.EC"or iso=="A.....BCD.ED.BE.CAF....F" or iso=="A.....BCD.ED.BE.CA..F....F":# or iso=="A..BAC........B..DE.F....E.DF.C":
        for i1, i2 in itertools.combinations(isomorphs[iso], 2):
            if i1[2] == i2[2]:
                continue
            var = next(varName)
            print("Assoc:",var,iso,isomorphs[iso].index(i1),isomorphs[iso].index(i2))
            variables.append(var)

            isoLen = len(i1[2])
            #if "F....F" in iso:
                #isoLen -= 6
            
            for i in range(isoLen):
                if not (i1[2][i], i2[2][i], var) in created:
                    created.add((i1[2][i], i2[2][i], var))
                    print((i1[2][i], i2[2][i], var))
                    chainPairs.append( ChainPair(i1[2][i], i2[2][i], var, iso+f"_{i1[0]}_{i1[1]}", iso+f"_{i2[0]}_{i2[1]}"))


print(len(chainPairs))

print(variables)

##multipliers = (-3, 3, -1, 1, 3, 6, 2, 4, 3, -1, 1, -4, -2, 2, 1, -1, 2, 3, 1)
##
##for d in range(1,83):
##            alphabet = [None] * 83
##            alphabet[0] = 19
##            cp = chainPairs[:]
##            while cp:
##                change = False
##                for p in cp[:]:
##                    md = multipliers[variables.index(p.distance)]
##                    c1 = None
##                    c2 = None
##                    dist = None
##                    
##                    if p.c1 in alphabet:
##                        c1 = p.c1
##                        c2 = p.c2
##                        
##                        dist =  d*md
##                    elif p.c2 in alphabet:
##                        c1 = p.c2
##                        c2 = p.c1
##                        dist = -(d*md)
##
##                    else:
##                        continue
##
##                    dist %= 83
##
##                    pos = (alphabet.index(c1) + dist) % 83
##                    if alphabet[pos] != None and alphabet[pos] != c2:
##                        print("Fail",dist, pos, c1, c2, alphabet[pos], alphabet)
##                        break
##
##                    print(dist, pos, c1, c2, alphabet[pos], p)
##                    alphabet[pos] = c2
##
##                    cp.remove(p)
##                    change = True    
##
##                else:
##                    if change:
##                        continue
##                    else:
##                        print(d, len(cp))
##                break
##            else:
##                print(d, alphabet)




#b,c,d,p (-2,0,0,0), (0,0,0,1), (2,0,0,1),
multipliers = ((-1,0,0,0), (1,0,0,0), (0,1,0,0), (0,0,1,0), (1,0,0,0), (2,0,0,0), (1,1,0,0), (1,0,1,0), (1,0,0,0), (0,1,0,0), (0,0,1,0), (-1,1,0,0), (-1, 0,1,0), (0,-1,1,0),  (0,1,0,0), (0,-1,1,0), (1,0,0,0), (2,0,0,1))


for i in range(len(variables)):
    print(variables[i],multipliers[i])

forbiddenEqualities = []
forbiddenNegEqualities = []

for p1, p2 in itertools.combinations(chainPairs, 2):
    if p1.c1 == p2.c1 and p2.c2 != p1.c2:
        forbiddenEqualities.append((multipliers[variables.index(p1.distance)], multipliers[variables.index(p2.distance)]))

    if p1.c2 == p2.c2 and p2.c1 != p1.c1:
        forbiddenEqualities.append((multipliers[variables.index(p1.distance)], multipliers[variables.index(p2.distance)]))
        
    if p1.c1 == p2.c2 and p2.c1 != p1.c2:
        forbiddenNegEqualities.append((multipliers[variables.index(p1.distance)], multipliers[variables.index(p2.distance)]))

    if p1.c2 == p2.c1 and p2.c2 != p1.c1:
        forbiddenNegEqualities.append((multipliers[variables.index(p1.distance)], multipliers[variables.index(p2.distance)]))


statement = ""

for m1, m2 in forbiddenEqualities:
    statement += f"(b * {m1[0]} + c*{m1[1]}+d*{m1[2]}+pv*{m1[3]})%83 == (b * {m2[0]} + c*{m2[1]}+d*{m2[2]}+pv*{m2[3]})%83 or "

for m1, m2 in forbiddenNegEqualities:
    statement += f"(b * {m1[0]} + c*{m1[1]}+d*{m1[2]}+pv*{m1[3]})%83 == (-(b * {m2[0]} + c*{m2[1]}+d*{m2[2]}+pv*{m2[3]}))%83 or "

statement = statement[:-4]

statement = compile(statement, "<string>", "eval")

primes = (1,2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79)

for b in primes:
    for c in primes:
        print(b,c)
        for d in primes:
            for pv in [0]:
                if eval(statement):
                    continue
                alphabet = [None] * 83
                alphabet[0] = 21
                cp = chainPairs[:]
                while cp:
                    change = False
                    for p in cp[:]:
                        mb, mc, md, mp = multipliers[variables.index(p.distance)]
                        c1 = None
                        c2 = None
                        dist = None
                        
                        if p.c1 in alphabet:
                            c1 = p.c1
                            c2 = p.c2
                            
                            dist =  b*mb + c*mc + d*md + pv*mp
                        elif p.c2 in alphabet:
                            c1 = p.c2
                            c2 = p.c1
                            dist = -(b*mb + c*mc + d*md + pv*mp)

                        else:
                            continue

                        dist %= 83

                        pos = (alphabet.index(c1) + dist) % 83
                        if alphabet[pos] != None and alphabet[pos] != c2:
                            #print("Fail",dist, pos, c1, c2, alphabet[pos], p)
                            break

                        #print(dist, pos, c1, c2, alphabet[pos], p)
                        alphabet[pos] = c2

                        cp.remove(p)
                        change = True    

                    else:
                        if change:
                            continue
                        else:
                            print(b,c,d,pv, alphabet)
                            alphabet = [None] * 83
                            alphabet[0] = cp[0].c1
                            continue
                    break
                else:
                    print(b,c,d,pv, alphabet)
    

##
##
##equalityGroups = []
##
##negativeRelations = []
##
##for p1, p2 in itertools.combinations(chainPairs, 2):
##    if p1.c1 == p2.c1 and p1.c2 == p2.c2:
##        for e in equalityGroups:
##            if p1.distance in e:
##                e.add(p2.distance)
##                break
##            elif p2.distance in e:
##                e.add(p1.distance)
##                break
##        else:
##            equalityGroups.append({p1.distance, p2.distance})
##                
##        print(f"{p1.distance} = {p2.distance}")
##    if p1.c1 == p2.c2 and p1.c2 == p2.c1:
##        if not {p1.distance, p2.distance} in negativeRelations:
##            negativeRelations.append({p1.distance, p2.distance})
##        print(f"{p1.distance} = -{p2.distance}")
##
##mergedEqualityGroups = []
##
##for e in equalityGroups:
##    for e2 in mergedEqualityGroups:
##        if e.intersection(e2):
##            mergedEqualityGroups.remove(e2)
##            mergedEqualityGroups.append(e2.union(e))
##            break
##    else:
##        mergedEqualityGroups.append(e)
##
##
##print(mergedEqualityGroups)
##print(negativeRelations)
##
##def isEqual(v1, v2):
##    for eg in mergedEqualityGroups:
##        if v1 in eg and v2 in eg:
##            return True
##
##def getRepr(v1):
##    for eg in mergedEqualityGroups:
##        if v1 in eg:
##            return min(eg)
##    return v1
##
##checkedChains = set()        
##
##for p1, p2 in itertools.permutations(chainPairs,2):
##    if p1.c2 == p2.c1 and isEqual(p1.distance, p2.distance):
##        for p3 in chainPairs:
##            if p1.c1 == p3.c1 and p2.c2 == p3.c2:
##                print(f"{p3.distance} = 2*{p1.distance}")
##            if p1.c1 == p3.c2 and p2.c2 == p3.c1:
##                print(f"{p3.distance} = -2*{p1.distance}")
##
##printed = set()
##
##for p1, p2 in itertools.permutations(chainPairs,2):
##    if p1.c2 == p2.c1 :
##        for p3 in chainPairs:
##            toPrint = ""
##            if p1.c1 == p3.c1 and p2.c2 == p3.c2:
##                toPrint = (f"{p3.distance} = {p1.distance}+{p2.distance}")
##            if p1.c1 == p3.c2 and p2.c2 == p3.c1:
##                toPrint = (f"{p3.distance} = -({p1.distance}+{p2.distance})")
##
##            if toPrint and not toPrint in printed:
##                printed.add(toPrint)
##                print(toPrint)
