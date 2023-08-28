import json
import itertools

with open("isomorphs.json") as f:
    isomorphs = json.load(f)

for iso in isomorphs.keys():
    for i1,i2 in itertools.permutations(isomorphs[iso], 2):
        for a,b in zip(i1[2],i2[2]):
            if a==b:
                print(iso, i1[0], i1[1],i2[0],i2[1])
                break


##for iso in isomorphs.keys():
##    l = len(isomorphs[iso][0][2])
##    for i in range(l):
##        a = set()
##        for ic in isomorphs[iso]:
##            a.add(ic[2][i])
##        if len(a) < len(isomorphs[iso]):
##            print(iso, i, len(a), len(isomorphs[iso]))
        
