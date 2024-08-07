import math

text = 5*"You've gotta be carefulvirsihin Vipunen kuoli, Lemminkäinen leikkilöihin. data there isn't raukaisen sanaisen arkun, virsilippahan viritän,s oJop' on astuiksen alemma, laskeusi lainehille,n occasion."
text += text[:40]
alphabet = "abcdefghijklmnopqrstuvwxyz"

N = 0

def _patternFromSequence(sequence):
    if len(sequence)>30:
        return _patternFromSequence(sequence[:len(sequence)//2]) + _patternFromSequence(sequence[len(sequence)//2:])
    letterMapping = {}
    for c in sequence:
        if not c in letterMapping.keys() and sequence.count(c) > 1:
            letterMapping[c] = chr(65 + len(letterMapping))

    pattern = ""
    for c in sequence:
        pattern += letterMapping.get(c, ".")

    return pattern

def asciify(m):
    ret = ""
    for c in m:
        ret += chr(32+c)
    return ret

#c = previous ciphertext char
#p = current plaintext char
#pp = previous plaintext char
def func(c, p, pp):
    r = c + 2**(p+pp)
    return r%83




def encode(m, init):
    ret = [init]
    prevC = 0
    a=0
    for c in m:
        c = c.lower()
        if c in alphabet:
            i = alphabet.index(c)
            #ret.append(func(ret[-1], i, prevC))
            ret.append((i+ ret[-1]+1)%83)
            
            if prevC == i:
                ret[-1] = 3**(ret[-1])
                ret[-1] %= 83

            prevC = i
    return ret

#bucketSizes = [8,1,3,3,12,2,2,4,7,1,1,4,1,7,7,2,1,6,6,8,2,1,1,1,1,1]
bucketSizes = [6,2,2,3,9,2,2,4,5,2,2,4,2,5,5,2,2,5,5,2,2,2,2,2,2,2]

print(sum(bucketSizes))

def encode2(text, offset):

    buckets = []
    i = 0
    for s in bucketSizes:
        n = []
        for j in range(s):
            n.append(i)
            i+=1
        buckets.append(n)
    
    ret = [2]
    cText = []
    for c in offset+text:
        c = c.lower()
        if c in alphabet:
            cText.append(alphabet.index(c))

    i = 0
    prevV = 0
    for c,cprev in zip(cText[1:], cText[:-1]):
        b = buckets[(c)%26]
        v = b[0]
        b.remove(v)
        b.append(v)
        if i>=len(offset):
            ret.append((v)%83)

        if v%10==0:
            buckets[c],buckets[cprev] = buckets[cprev],buckets[c]
            
        prevV = v
        i+=1
    return ret

def encode3(text, offset):
    g1_pattern = [1]
    g2_pattern = [1, 0]
    g3_pattern = [1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0]

    cn = offset
    gn = offset

    ret = []
    prevP = 0
    for p in text:
        p=p.lower()
        if p==" ":
            cn=0
        if p in alphabet:
            pindex = alphabet.index(p)
            off = 0

            d = (pindex - prevP)%26
            if d == 0:
                d = 26
            for i in range(d):
                off += 3*g1_pattern[gn%1] + 4*g2_pattern[gn%2] + 3*g3_pattern[gn%17]
                gn+=1

            cn += off;
            ret.append((cn)%83)
            prevP = pindex
    return ret

#alphabet = alphabet[::-1]

    


print(len(text))
A = encode3(text, 3)
B = encode3(text, 14)

#A = encode2(text[:50]+"erwervdfbbbtbt"+text[:50])
#B = encode2(text[:50]+"ergetrgergetggr"+text[:50])

hasCrossDoubles = False
for i in range(len(A)-1):
    if A[i]==B[i+1] or B[i]==A[i+1]:
        hasCrossDoubles = True


print(asciify(A[:200]))
print(asciify(B[:200]))
print(_patternFromSequence(A[:200]))
print(_patternFromSequence(B[:200]))

#print(len(set(A+B)), list(filter(lambda a: not a in A+B, range(83))))

print("Has Cross-Double:",hasCrossDoubles)

print("Gap Freqs:")
for i in range(20):
    a=0
    for j in range(len(B)-i):
        if B[j] == B[j+i]:
            a += 1
    print(i, a)



