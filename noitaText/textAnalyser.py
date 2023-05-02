##from noitaText import all_text
##
##
##critical_lengths = (83,)
##
##
##for text in all_text:
##    words = text.replace("\n"," ").split(" ")
##    for sep in ("", " "):
##        for length in range(1,len(words)+1):
##            for start in range(0, len(words)-length+1):
##                sequence = ""
##                for i in range(start, start+length-1):
##                    sequence += words[i]+sep
##                sequence += words[start+length-1]
##
##                if len(sequence) in critical_lengths:
##                    print(sequence, len(sequence))

from noitaText import emerals_tablets


alphabet = "abcdefghijklmnopqrstuvwxyz"

def IoC(messages, precalc=True):

    mmin = 0
    mmax = len(alphabet)-1
    
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



mess = []

for text in emerals_tablets:
    n = []
    for c in text:
        c = c.lower()
        if c in alphabet:
            n.append(alphabet.index(c))
    mess.append(n)

print(IoC(mess))
