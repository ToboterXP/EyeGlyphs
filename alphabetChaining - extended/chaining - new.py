from dataclasses import dataclass
import itertools
import json
import math
import copy
import random as r

messages = ((50, 66, 5, 48, 62, 13, 75, 29, 24, 61, 42, 70, 66, 62, 32, 14, 81, 8,  15, 78, 2,  29, 13, 49, 1,  80, 82, 40, 63, 81, 21, 19, 0, 40, 51, 65, 26, 14, 21, 70, 47, 44, 48, 42, 19, 48, 13, 47, 19, 49, 72, 31, 5, 24, 3, 43, 59, 67, 33, 49, 41, 60, 21, 26, 30, 5, 25, 20, 71, 11, 74, 56, 4, 74, 19, 71, 4, 51, 41, 43, 80, 72, 54, 63, 79, 81, 15, 16, 44, 31, 30, 12, 33, 57, 28, 13, 64, 43, 48),
            (80, 66, 5, 48, 62, 13, 75, 29, 24, 61, 42, 70, 66, 62, 32, 14, 81, 8,  15, 78, 2,  29, 13, 49, 1,  29, 11, 30, 52, 81, 21, 19, 0, 25, 26, 54, 20, 14, 21, 70, 47, 44, 48, 42, 19, 48, 13, 47, 19, 49, 44, 26, 59, 77, 64, 43, 79, 28, 72, 64, 1, 30, 73, 23, 67, 6, 33, 25, 64, 81, 68, 46, 17, 36, 13, 17, 21, 68, 13, 9, 46, 67, 57, 34, 62, 82, 15, 10, 73, 62, 2, 11, 65, 72, 37, 44, 10, 43, 68, 62, 9, 34, 18),
            (36, 66, 5, 48, 62, 13, 75, 29, 24, 61, 42, 70, 66, 62, 32, 14, 81, 8,  15, 78, 2,  29, 13, 49, 1,  69, 76, 52, 9,  48, 66, 80, 22, 64, 57, 40, 49, 78, 3, 16, 56, 19, 47, 40, 80, 6, 13, 64, 29, 49, 64, 63, 6, 49, 31, 13, 16, 10, 45, 24, 26, 77, 10, 60, 81, 61, 34, 54, 70, 21, 15, 4, 66, 77, 42, 37, 30, 22, 0, 11, 41, 72, 57, 20, 23, 57, 65, 41, 23, 18, 72, 42, 5, 3, 26, 78, 8, 5, 54, 45, 77, 25, 64, 61, 16, 44, 54, 51, 20, 63, 25, 11, 26, 45, 53, 60, 38, 34),
            (76, 66, 5, 49, 75, 54, 69, 46, 32, 1,  42, 60, 26, 48, 50, 80, 32, 24, 55, 61, 47, 12, 21, 12, 49, 54, 34, 25, 36, 15, 56, 55, 20, 9, 8, 62, 13, 82, 9, 44, 29, 60, 53, 82, 42, 80, 5, 43, 71, 3, 80, 77, 47, 78, 34, 25, 62, 18, 10, 49, 62, 64, 52, 81, 11, 66, 62, 13, 47, 17, 52, 70, 26, 23, 32, 31, 64, 23, 35, 32, 50, 6, 1, 25, 8, 37, 47, 43, 26, 76, 65, 68, 80, 17, 7, 45, 63, 14, 53, 63, 60, 16),
            (63, 66, 5, 49, 75, 54, 2,  60, 29, 40, 78, 47, 60, 75, 67, 71, 60, 2,  65, 7,  47, 14, 45, 74, 59, 41, 80, 13, 60, 13, 81, 22, 35, 50, 40, 39, 2, 59, 48, 31, 76, 2, 80, 75, 1, 56, 67, 11, 21, 8, 40, 65, 45, 75, 55, 39, 60, 42, 13, 3, 22, 57, 2, 6, 58, 9, 70, 1, 58, 56, 63, 68, 25, 79, 7, 20, 19, 64, 2, 66, 73, 30, 71, 16, 12, 30, 65, 37, 20, 13, 22, 63, 18, 46, 64, 59, 41, 81, 82, 22, 78, 36, 47, 17, 4, 6, 17, 5, 36, 79, 63, 1, 64, 69, 15, 43, 4, 58, 56, 31, 14, 64, 58, 18, 44, 78, 69, 1, 0, 46, 20, 71, 73, 25, 35, 8, 24),
            (34, 66, 5, 49, 75, 54, 23, 74, 11, 13, 28, 26, 19, 48, 67, 57, 37, 60, 34, 28, 74, 10, 17, 32, 11, 18, 19, 43, 19, 81, 42, 4, 62, 9, 46, 49, 32, 51, 76, 58, 4, 43, 47, 17, 67, 79, 21, 32, 44, 16, 30, 37, 26, 28, 41, 68, 57, 34, 51, 10, 69, 70, 8, 6, 46, 43, 18, 39, 47, 43, 15, 13, 33, 30, 35, 62, 37, 0, 37, 5, 38, 55, 37, 13, 40, 25, 9, 21, 11, 64, 5, 79, 42, 68, 11, 71, 11, 48, 3, 67, 61, 40, 22, 14, 35, 50, 61, 39, 11, 2, 66, 49, 51, 53, 17, 73, 36, 75, 74, 54, 24, 30, 54, 70),
            (27, 66, 5, 49, 75, 54, 2,  60, 29, 40, 2,  55, 9,  15, 59, 18, 68, 3,  36, 5,  47, 77, 44, 38, 1,  18, 28, 76, 4,  34, 60, 63, 58, 80, 17, 54, 79, 75, 48, 54, 55, 19, 62, 64, 14, 47, 51, 70, 75, 5, 11, 47, 45, 58, 68, 69, 79, 25, 38, 45, 73, 47, 68, 50, 34, 45, 78, 26, 79, 57, 4, 56, 22, 60, 18, 75, 43, 60, 59, 67, 63, 42, 49, 33, 40, 65, 79, 77, 7, 3, 26, 62, 31, 78, 26, 57, 69, 40, 4, 23, 26, 13, 67, 42, 38, 72, 11, 39, 65, 60, 25, 6, 80, 66, 68, 77, 59, 78, 19),
            (77, 66, 5, 49, 75, 54, 2,  60, 29, 40, 2,  55, 9,  15, 59, 18, 68, 3,  36, 5,  47, 60, 21, 80, 1,  72, 55, 16, 82, 35, 57, 19, 1, 66, 18, 27, 39, 17, 74, 81, 39, 14, 78, 0, 25, 65, 43, 66, 64, 38, 81, 23, 24, 50, 57, 30, 71, 75, 26, 68, 54, 57, 56, 50, 71, 73, 14, 21, 8, 32, 26, 63, 5, 37, 19, 43, 66, 47, 53, 34, 66, 23, 73, 31, 54, 38, 77, 67, 11, 63, 79, 6, 22, 21, 51, 69, 74, 21, 5, 17, 67, 37, 29, 21, 60, 14, 82, 44, 30, 4, 20, 42, 35, 1, 31, 54, 46, 20, 40, 30),
            (33, 66, 5, 49, 75, 54, 2,  60, 29, 40, 2,  55, 9,  15, 59, 18, 68, 3,  36, 5,  47, 33, 21, 59, 44, 18, 28, 76, 59, 34, 60, 63, 79, 27, 12, 54, 5, 49, 48, 54, 55, 52, 62, 72, 69, 10, 57, 22, 58, 48, 67, 53, 7, 34, 32, 30, 31, 19, 26, 8, 34, 46, 7, 30, 71, 55, 34, 75, 54, 9, 6, 60, 5, 23, 25, 45, 42, 80, 25, 12, 22, 76, 20, 51, 62, 21, 40, 9, 41, 10, 44, 73, 8, 33, 70, 73, 6, 31, 21, 72, 5, 40, 61, 51, 42, 66, 64, 74, 61, 25, 63, 42, 24, 41))


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

#messages = (6,7)

for iso in isomorphs.keys():
    #if not iso in badIsomorphs: or iso=="A.B....A..B"  
    #if iso == "A.BA..B"  or iso=="AB..C...A.DEF.BF.DB.EC"or iso=="A.....BCD.ED.BE.CAF....F" or iso=="A.....BCD.ED.BE.CA..F....F":# or iso=="A..BAC........B..DE.F....E.DF.C":
        for i1, i2 in itertools.combinations(isomorphs[iso], 2):

            if not i1[0] in (0,1,2) or not i2[0] in (0,1,2):
                continue
            
            if i1[2] == i2[2] or i1[1]==i2[1]:
                continue

            if iso=="AB......A.C.D.BD.CB":
                continue

            #if not (i1[1]//26 == (i1[1]+len(i1[2]))//26 and i2[1]//26 == (i2[1]+len(i2[2]))//26):
            #    continue
            var = next(varName)
            print("Assoc:",var,iso,isomorphs[iso].index(i1),isomorphs[iso].index(i2), i1[0], i2[0])
            variables.append(var)

            isoStart = 0
            isoLen = len(i1[2])
            if "F....F" in iso:
                isoLen -= 6
                if var=='q':
                    isoStart = 7
                    isoLen -= 6
            
            for i in range(isoStart,isoLen):
                if not (i1[2][i], i2[2][i], var) in created:
                    created.add((i1[2][i], i2[2][i], var))
                    print((i1[2][i], i2[2][i], var))
                    chainPairs.append( ChainPair(i1[2][i], i2[2][i], var, iso+f"_{i1[0]}_{i1[1]}", iso+f"_{i2[0]}_{i2[1]}"))


print(len(chainPairs))

print(variables)


varValues = { #b,c,d, v6(v6 = diff 0,6)
    'a' : (-1,0,0,0,0,0,0,0),
    'b' : (1,0,0,0,0,0,0,0),
    'c' : (0,1,0,0,0,0,0,0),
    'd' : (0,0,1,0,0,0,0,0),
    'e' : (1,0,0,0,0,0,0,0),
    'f' : (2,0,0,0,0,0,0,0),
    'g' : (1,1,0,0,0,0,0,0),
    'h' : (1,0,1,0,0,0,0,0),
    'i' : (1,0,0,0,0,0,0,0),
    'j' : (0,1,0,0,0,0,0,0),
    'k' : (0,0,1,0,0,0,0,0),
    'l' : (-1,1,0,0,0,0,0,0),
    'm' : (-1,0,1,0,0,0,0,0),
    'n' : (0,-1,1,0,0,0,0,0),
    'o' : (0,1,0,0,0,0,0,0),
    'p' : (0,-1,1,0,0,0,0,0),
    'q' : (1,0,0,0,0,0,0,0),
    #'v6': (0,0,0,1,0,0,0,0),
    #'v17': (0,0,0,0,1,0,0,0),
    #'v3' : (0,0,0,0,0,1,0,0),
    #'v11' : (0,0,0,0,0,0,1,0),
    #'v5' : (0,0,0,0,0,0,1,0),
    #'v11' : (0,0,0,0,0,0,0,1),
    }



#chainPairs.append(ChainPair(0,6, 'v6', "",""))
#chainPairs.append(ChainPair(0,17, 'v17', "",""))
#chainPairs.append(ChainPair(0,3, 'v3', "",""))
#chainPairs.append(ChainPair(0,5, 'v5', "",""))
#chainPairs.append(ChainPair(0,11, 'v11', "",""))


null = (0,0,0,0,0,0,0)

def vecAdd(a,b):
    ret = []
    for a1,b1 in zip(a,b):
        ret.append((a1+b1)%83)
    return tuple(ret)

def vecSub(a,b):
    ret = []
    for a1,b1 in zip(a,b):
        ret.append((a1-b1)%83)
    return tuple(ret)

def vecMul(c,a):
    ret = []
    for a1 in a:
        ret.append((c*a1)%83)
    return tuple(ret)

def vecDiv(c,a):
    ret = []
    for a1 in a:
        ret.append((a1//c)%83)
    return tuple(ret)

def simplify(a):
    d = a[0]
    for a1 in a:
        d = math.gcd(d,a1)

    d = abs(d)
    if not d:
        return tuple(a)
    return tuple(vecDiv(d, a))



changed = list()

M = [] #i,j = relationship from i to j
for i in range(83):
    M.append([None]*83)
    M[i][i] = null
    changed.append((i,i))


#M[11][65] = (3, 2, 3, 0, 0, 1)
#M[54][51] = (0, 80, 1, 0, 0, 0)



prevM = None


print("Computing distance matrix")

a=0

guessesApplied = False
while prevM != M:
    a+=1
    print(a)
    prevM = copy.deepcopy(M)
    pchanged = set(changed)
    changed = list()
    for i,j in pchanged:
        if prevM[i][j]:
            v = prevM[i][j]
            for c in chainPairs:
                if c.distance in "":
                    continue
                if c.c1 == j:
                    nv = tuple(vecAdd(v, varValues[c.distance]))
                    if prevM[i][c.c2] and prevM[i][c.c2] != nv:
                        print("Error ",i,j,c.c1,c.c2,(i,c.c2),prevM[i][c.c2], nv)
                    if not prevM[i][c.c2]:
                        changed.append((i,c.c2))
                    
                    M[i][c.c2] = nv
                    M[c.c2][i] = vecMul(-1,nv)
                    
                    #print(i,c.c2,nv,(i,j),c, "a")
                elif c.c2 == j:
                    nv = tuple(vecAdd(v, vecMul(-1,varValues[c.distance])))
                    if prevM[i][c.c1] and prevM[i][c.c1] != nv:
                        print("Error ",i,j,c.c1,c.c2,(i,c.c1),prevM[i][c.c1], nv)

                    if not prevM[i][c.c1]:
                        changed.append((i,c.c1))
                        
                    M[i][c.c1] = nv
                    M[c.c1][i] = vecMul(-1,nv)
                    
                    #print(i,c.c1,nv,(i,j),c, "a")

                elif c.c1 == i:
                    nv = tuple(vecAdd(vecMul(-1,v), varValues[c.distance]))
                    if prevM[j][c.c2] and prevM[j][c.c2] != nv:
                        print("Error ",i,j,c.c1,c.c2,(j,c.c2),prevM[j][c.c2], nv)
                    if not prevM[j][c.c2]:
                        changed.append((j,c.c2))
                    
                    M[j][c.c2] = nv
                    M[c.c2][j] = vecMul(-1,nv)
                    
                    #print(i,c.c2,nv,(i,j),c, "a")
                elif c.c2 == i:
                    nv = tuple(vecAdd(vecMul(-1,v), vecMul(-1,varValues[c.distance])))
                    if prevM[j][c.c1] and prevM[j][c.c1] != nv:
                        print("Error ",i,j,c.c1,c.c2,(j,c.c1),prevM[j][c.c1], nv)

                    if not prevM[j][c.c1]:
                        changed.append((j,c.c1))
                        
                    M[j][c.c1] = nv
                    M[c.c1][j] = vecMul(-1,nv)

    if prevM == M and not guessesApplied:
        guessesApplied = True
        

def sortedPrint(dictionary):
    l = list(dictionary.keys())
    l.sort(reverse=True, key=lambda a: dictionary[a])
    for i in l:
        print(i, dictionary[i])

a = 0
n = 0
mentries = {}
for i in range(83):
    for j in range(83):
        if M[i][j]:
            n+=1
            mentries.setdefault(M[i][j], 0)
            mentries[M[i][j]] +=1

            if M[i][j] == null and i!=j:
                print("Null error", i,j)

            #if M[i][j] == (1, 2, 1):
                #print("A",i,j)
        a+=1
print("Entries found:",n,"Entries total:",a,"Ratio:",n/a, "Distinct Distances:",len(mentries.keys()))

series = set()
for i in range(83):
    eq = {i}
    change=True
    while change:
        change = False
        for j in tuple(eq):
            for k in range(83):
                if not k in eq and M[j][k]:
                    eq.add(k)
                    change=True

    eq = list(eq)
    eq.sort()
    if not tuple(eq) in series and len(eq)>1:
        series.add(tuple(eq))
        print(eq)


##mcols = []
##for j in range(83):
##    c = []
##    for i in range(83):
##        c.append(M[i][j])
##    mcols.append(c)
##
###for a in mentries:
##for i in range(3):
##    for n in (80,81,82,1,2,3):
##        a = [0]*6
##        a[i] = n
##        a = tuple(a)
##        if mentries[a] >= 8:
##            for b in mentries:
##                if mentries[b]>=8:
##                    for m in M+mcols:
##                        if a in m and b in m:
##                            break
##                    else:
##                        print(a,b)


diffs = {}
a = 0
n=0
for m in messages[:3]:
    for i1,i2 in zip(m[:],m[1:]):
        d = M[i1][i2]
        a += 1
        if d:
            n+=1
            diffs.setdefault(d,0)
            diffs[d] += 1



print(n,a,n/a, len(diffs.keys()))


##inequalities = set()
##
##
##for i in range(83):
##    for j in range(83):
##        for k in range(j+1,83):
##            if M[i][j] and M[i][k] and M[i][j] != null and M[i][k] != null:
##                v = vecSub(M[i][j],M[i][k])
##                #if not vecSub(M[i][k],M[i][j]) in inequalities:
##                inequalities.add(v)
##        if M[i][j] and M[i][j] != null:
##            inequalities.add(M[i][j])
##
##print(len(inequalities))
##
##term = ""
##
##for a,b,c,d,e,f in inequalities:
##    term += f" and ({a}*a+{b}*b+{c}*c+{d}*d+{e}*e+{f}*f)%83 != 0"
##
##term = term[5:]
##
##term = compile(term, "<string>","eval")


##for a in range(1,83):
##    b=a
##    c=a
##            print(a,b,c)
##            for d in range(1,83):
##                for e in range(1,83):
##                    for f in range(1,83):
##                        if eval(term):
##                            print(a,b,c,d,e,f)




##while True:
##    a = r.randint(1,82)
##    b = r.randint(1,82)
##    c = r.randint(1,82)
##    d = r.randint(1,82)
##    e = r.randint(1,82)
##    f = r.randint(1,82)
##    if eval(term):
##        print(a,b,c,d,e,f)
    
                    


diffls = list(diffs.keys())

diffls.sort(key=lambda a: a[0]*10000+a[1]*100+a[2])


for i in range(len(diffls)):
    print(chr(48+i), diffls[i])


foundForms = []
for f in mentries.keys():
    foundForms.append(simplify(f))


impossiblePairs = set()
possiblePairs = set()

for i,d1 in enumerate(diffls):
    for i2,d2 in enumerate(diffls):
        if i>=i2:
            continue
        if d1!=d2:
            d = simplify(vecSub(d1,d2))
            dd = simplify(vecSub(d2,d1))
            imp = False
            for f in foundForms:
                if f == d or f==dd:
                    imp = True
                    impossiblePairs.add((chr(48+i),chr(48+i2)))
            if not imp:
                possiblePairs.add((chr(48+i),chr(48+i2)))                

print(len(impossiblePairs),len(possiblePairs))




#print(diffls)
##ss = []
##for i in range(len(M[0][0])):
##    ss.append(set())
##for n in diffls:
##    for i in range(len(n)):
##        ss[i].add(n[i])
##
##for a in ss:
##    print(a)

seqs = []

st = []

for m in messages[:3]:
    s = []
    si=0
    i=0
    for i1,i2 in zip(m[:],m[1:]):
        d = M[i1][i2]
        if d:
            print(chr(48+diffls.index(d)),end="")
            st.append(diffls.index(d))
        else:
            print(" ", end="")
    print("\n")
           


def IoC(messages, precalc=True, mmin = 0, mmax=82):
    n = [0]*(mmax - mmin + 1)
    amount = 0
    for m in messages:
        amount += len(m)
        for c in m:
            
            n[c - mmin] += 1

    if amount <= 1:
        return 0,0

    ic = 0
    for i in n:
        ic += i*(i-1)

    if precalc:
        return ic / (amount * (amount - 1) / (mmax - mmin + 1))

    return ic , (amount * (amount - 1) / (mmax - mmin + 1))

print(IoC([st], mmax=len(diffs.keys())-1))

while True:
    a,b = input("").split(" ")
    if (a,b) in impossiblePairs or (b,a) in impossiblePairs:
        print("Impossible")
    if (a,b) in possiblePairs or (b,a) in possiblePairs:
        print("Possible")
    
#sortedPrint(diffs)





##print(M)
##


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




#a,b,e
##multipliers = ((1,0,0,0), (0,1,0,0), (-1,0,0,0), (-1,1,0,0), (0,1,0,0), (0,0,1,0), (1,0,-1,0), (1,0,-2,0), (1,0,-1,0))
##
##
##for i in range(len(variables)):
##    print(variables[i],multipliers[i])
##
##forbiddenEqualities = []
##forbiddenNegEqualities = []
##
##for p1, p2 in itertools.combinations(chainPairs, 2):
##    if p1.c1 == p2.c1 and p2.c2 != p1.c2:
##        forbiddenEqualities.append((multipliers[variables.index(p1.distance)], multipliers[variables.index(p2.distance)]))
##
##    if p1.c2 == p2.c2 and p2.c1 != p1.c1:
##        forbiddenEqualities.append((multipliers[variables.index(p1.distance)], multipliers[variables.index(p2.distance)]))
##        
##    if p1.c1 == p2.c2 and p2.c1 != p1.c2:
##        forbiddenNegEqualities.append((multipliers[variables.index(p1.distance)], multipliers[variables.index(p2.distance)]))
##
##    if p1.c2 == p2.c1 and p2.c2 != p1.c1:
##        forbiddenNegEqualities.append((multipliers[variables.index(p1.distance)], multipliers[variables.index(p2.distance)]))
##
##
##statement = ""
##
##for m1, m2 in forbiddenEqualities:
##    statement += f"(b * {m1[0]} + c*{m1[1]}+d*{m1[2]}+pv*{m1[3]})%83 == (b * {m2[0]} + c*{m2[1]}+d*{m2[2]}+pv*{m2[3]})%83 or "
##
##for m1, m2 in forbiddenNegEqualities:
##    statement += f"(b * {m1[0]} + c*{m1[1]}+d*{m1[2]}+pv*{m1[3]})%83 == (-(b * {m2[0]} + c*{m2[1]}+d*{m2[2]}+pv*{m2[3]}))%83 or "
##
##statement = statement[:-4]
##
##statement = compile(statement, "<string>", "eval")
##
##primes = (1,2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79)
##
##for b in primes:
##    for c in primes:
##        print(b,c)
##        for d in primes:
##            for pv in [0]:
##                if eval(statement):
##                    continue
##                alphabet = [None] * 83
##                alphabet[0] = 21
##                cp = chainPairs[:]
##                while cp:
##                    change = False
##                    for p in cp[:]:
##                        mb, mc, md, mp = multipliers[variables.index(p.distance)]
##                        c1 = None
##                        c2 = None
##                        dist = None
##                        
##                        if p.c1 in alphabet:
##                            c1 = p.c1
##                            c2 = p.c2
##                            
##                            dist =  b*mb + c*mc + d*md + pv*mp
##                        elif p.c2 in alphabet:
##                            c1 = p.c2
##                            c2 = p.c1
##                            dist = -(b*mb + c*mc + d*md + pv*mp)
##
##                        else:
##                            continue
##
##                        dist %= 83
##
##                        pos = (alphabet.index(c1) + dist) % 83
##                        if alphabet[pos] != None and alphabet[pos] != c2:
##                            #print("Fail",dist, pos, c1, c2, alphabet[pos], p)
##                            break
##
##                        #print(dist, pos, c1, c2, alphabet[pos], p)
##                        alphabet[pos] = c2
##
##                        cp.remove(p)
##                        change = True    
##
##                    else:
##                        if change:
##                            continue
##                        else:
##                            print(b,c,d,pv, alphabet)
##                            alphabet = [None] * 83
##                            alphabet[0] = cp[0].c1
##                            continue
##                    break
##                else:
##                    print(b,c,d,pv, alphabet)
    

##equalityGroups = []
##
##negativeRelations = []
##
##printed = set()
##
##for p1, p2 in itertools.combinations(chainPairs, 2):
##    p = ""
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
##            
##        p = (f"{p1.distance} = {p2.distance}")
##    if p1.c1 == p2.c2 and p1.c2 == p2.c1:
##        if not {p1.distance, p2.distance} in negativeRelations:
##            negativeRelations.append({p1.distance, p2.distance})
##        p = (f"{p1.distance} = -{p2.distance}")
##
##    if not p in printed:
##        print(p)
##        printed.add(p)
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
##                print(f"{p3.distance} = 2*{p1.distance} ({getRepr(p3.distance)} = 2*{getRepr(p1.distance)})", p1, p2, p3)
##            if p1.c1 == p3.c2 and p2.c2 == p3.c1:
##                print(f"{p3.distance} = -2*{p1.distance} ({getRepr(p3.distance)} = -2*{getRepr(p1.distance)})", p1, p2, p3)
##
##
##
##for p1, p2 in itertools.permutations(chainPairs,2):
##    if p1.c2 == p2.c1 :
##        for p3 in chainPairs:
##            toPrint = ""
##            if p1.c1 == p3.c1 and p2.c2 == p3.c2:
##                toPrint = (f"{p3.distance} = {p1.distance}+{p2.distance} ({getRepr(p3.distance)} = {getRepr(p1.distance)}+{getRepr(p2.distance)})")
##            if p1.c1 == p3.c2 and p2.c2 == p3.c1:
##                toPrint = (f"{p3.distance} = -({p1.distance}+{p2.distance}) ({getRepr(p3.distance)} = -({getRepr(p1.distance)}+{getRepr(p2.distance)}))")
##
##            if toPrint and not toPrint in printed:
##                printed.add(toPrint)
##                print(toPrint)
