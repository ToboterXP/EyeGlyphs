import json

with open("isomorphs.json", "r") as f:
    isomorphs = json.load(f)


chains = []

foundChains = set()

for pattern in isomorphs.keys():
    print(pattern)
    newChains = []
    
    for o1 in isomorphs[pattern]:
        m1 = o1[2]
        for o2 in isomorphs[pattern]:
            m2 = o2[2]
            if m1 == m2:
                continue
            if tuple(map(lambda a: a[0] == a[1], zip(m1, m2))).count(True) > len(m1)//2: #ignore occurences with overly large overlap (clearly something is amiss)
                continue

            shared = set()
            for c in m1:
                if c in m2:
                    shared.add(c)

            for c in shared:
                p1 = m1[m2.index(c)]
                p3 = m2[m1.index(c)]

                identifier = (isomorphs[pattern].index(o1), isomorphs[pattern].index(o2))

                if (p1, c, p3) in foundChains:
                    continue

                if (p3, c, p1) in foundChains:
                    continue

                foundChains.add((p1, c, p3))
                newChains.append((p1, c, p3, identifier))

    if newChains:
        chains.append((pattern, newChains))


print(chains)

with open("atomicChains.json", "w") as f:
    json.dump(chains,f)

            

