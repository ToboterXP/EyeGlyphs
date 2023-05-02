
eyeMap = {}

for a in range(125):
    eyes = [a//25, (a%25)//5, a%5]
    diffs = (eyes[1] - eyes[0], eyes[2] - eyes[1])
    eyeMap.setdefault(diffs, [])
    eyeMap[diffs].append(a)

print(eyeMap)
