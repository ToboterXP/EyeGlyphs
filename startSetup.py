


expMess = ((66,5,48,62,13,75,29,24,61,42,70,66,62,32,14,81,8,15,78,2,29,13,49,1), (66,5,49,75,54,2,60,29,40,2,55,9,15,59,18,68,3,36,5,47))

def IoC(messages, precalc=True):

    mmin = 0
    mmax =82
    
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

def DoubleCount(messages):
    dc = 0
    for m in messages:
        for i in range(len(m)-1):
            if m[i] == m[i+1]:
                dc += 1
    return dc

expMess = [list(m) for m in expMess]

for m in expMess:
    for i in range(len(m)-1):
        m[i] = (m[i] + m[i+1]) % 83




print(expMess)

print(IoC(expMess))
