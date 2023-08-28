import json

with open("isomorphs.json") as f:
    isomorphs = json.load(f)



for iso in isomorphs.keys():
    l = len(isomorphs[iso][0][2])
    for i in range(l):
        a = set()
        for ic in isomorphs[iso]:
            a.add(ic[2][i])
        if len(a) < len(isomorphs[iso]):
            print(iso, i, len(a), len(isomorphs[iso]))
        
