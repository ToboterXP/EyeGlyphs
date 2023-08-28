import json

with open("isomorphs_extended.json", "r") as f:
    isomorphs = json.load(f)


chains = []

for pattern in isomorphs.keys():
    #print(pattern)
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

                if (p1, c, p3) in newChains:
                    continue

                if (p3, c, p1) in newChains:
                    continue

                newChains.append((p1, c, p3))

    if newChains:
        chains.append((pattern, newChains))


#print(chains)
print("Atomic Chain Amount:", sum(map(lambda a: len(a[1]), chains)))

with open("atomicChains.json", "w") as f:
    json.dump(chains,f)

            

