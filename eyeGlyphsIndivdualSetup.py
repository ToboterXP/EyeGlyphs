import random
import math
import itertools
from sympy.ntheory import discrete_log
from sympy.ntheory.residue_ntheory import nthroot_mod, is_primitive_root

RANDOM_MESSAGE = True
PRESERVE_REPEATED = True

ONLY_X_PLUS = False
X = 26


messages = ((50, 66, 5, 48, 62, 13, 75, 29, 24, 61, 42, 70, 66, 62, 32, 14, 81, 8,  15, 78, 2,  29, 13, 49, 1,  80, 82, 40, 63, 81, 21, 19, 0, 40, 51, 65, 26, 14, 21, 70, 47, 44, 48, 42, 19, 48, 13, 47, 19, 49, 72, 31, 5, 24, 3, 43, 59, 67, 33, 49, 41, 60, 21, 26, 30, 5, 25, 20, 71, 11, 74, 56, 4, 74, 19, 71, 4, 51, 41, 43, 80, 72, 54, 63, 79, 81, 15, 16, 44, 31, 30, 12, 33, 57, 28, 13, 64, 43, 48),
            (80, 66, 5, 48, 62, 13, 75, 29, 24, 61, 42, 70, 66, 62, 32, 14, 81, 8,  15, 78, 2,  29, 13, 49, 1,  29, 11, 30, 52, 81, 21, 19, 0, 25, 26, 54, 20, 14, 21, 70, 47, 44, 48, 42, 19, 48, 13, 47, 19, 49, 44, 26, 59, 77, 64, 43, 79, 28, 72, 64, 1, 30, 73, 23, 67, 6, 33, 25, 64, 81, 68, 46, 17, 36, 13, 17, 21, 68, 13, 9, 46, 67, 57, 34, 62, 82, 15, 10, 73, 62, 2, 11, 65, 72, 37, 44, 10, 43, 68, 62, 9, 34, 18),
            (36, 66, 5, 48, 62, 13, 75, 29, 24, 61, 42, 70, 66, 62, 32, 14, 81, 8,  15, 78, 2,  29, 13, 49, 1,  69, 76, 52, 9,  48, 66, 80, 22, 64, 57, 40, 49, 78, 3, 16, 56, 19, 47, 40, 80, 6, 13, 64, 29, 49, 64, 63, 6, 49, 31, 13, 16, 10, 45, 24, 26, 77, 10, 60, 81, 61, 34, 54, 70, 21, 15, 4, 66, 77, 42, 37, 30, 22, 0, 11, 41, 72, 57, 20, 23, 57, 65, 41, 23, 18, 72, 42, 5, 3, 26, 78, 8, 5, 54, 45, 77, 25, 64, 61, 16, 44, 54, 51, 20, 63, 25, 11, 26, 45, 53, 60, 38, 34),
            (76, 66, 5, 49, 75, 54, 69, 46, 32, 1,  42, 60, 26, 48, 50, 80, 32, 24, 55, 61, 47, 12, 21, 12, 49, 54, 34, 25, 36, 15, 56, 55, 20, 9, 8, 62, 13, 82, 9, 44, 29, 60, 53, 82, 42, 80, 5, 43, 71, 3, 80, 77, 47, 78, 34, 25, 62, 18, 10, 49, 62, 64, 52, 81, 11, 66, 62, 13, 47, 17, 52, 70, 26, 23, 32, 31, 64, 23, 35, 32, 50, 6, 1, 25, 8, 37, 47, 43, 26, 76, 65, 68, 80, 17, 7, 45, 63, 14, 53, 63, 60, 16),
            (63, 66, 5, 49, 75, 54, 2,  60, 29, 40, 78, 47, 60, 75, 67, 71, 60, 2,  65, 7,  47, 14, 45, 74, 59, 41, 80, 13, 60, 13, 81, 22, 35, 50, 40, 39, 2, 59, 48, 31, 76, 2, 80, 75, 1, 56, 67, 11, 21, 8, 40, 65, 45, 75, 55, 39, 60, 42, 13, 3, 22, 57, 2, 6, 58, 9, 70, 1, 58, 56, 63, 68, 25, 79, 7, 20, 19, 64, 2, 66, 73, 30, 71, 16, 12, 30, 65, 37, 20, 13, 22, 63, 18, 46, 64, 59, 41, 81, 82, 22, 78, 36, 47, 17, 4, 6, 17, 5, 36, 79, 63, 1, 64, 69, 15, 43, 4, 58, 56, 31, 14, 64, 58, 18, 44, 78, 69, 1, 0, 46, 20, 71, 73, 25, 35, 8, 24),
            (34, 66, 5, 49, 75, 54, 23, 74, 11, 13, 28, 26, 19, 48, 67, 57, 37, 60, 34, 28, 74, 10, 17, 32, 11, 18, 19, 43, 19, 81, 42, 4, 62, 9, 46, 49, 32, 51, 76, 58, 4, 43, 47, 17, 67, 79, 21, 32, 44, 16, 30, 37, 26, 28, 41, 68, 57, 34, 51, 10, 69, 70, 8, 6, 46, 43, 18, 39, 47, 43, 15, 13, 33, 30, 35, 62, 37, 0, 37, 5, 38, 55, 37, 13, 40, 25, 9, 21, 11, 64, 5, 79, 42, 68, 11, 71, 11, 48, 3, 67, 61, 40, 22, 14, 35, 50, 61, 39, 11, 2, 66, 49, 51, 53, 17, 73, 36, 75, 74, 54, 24, 30, 54, 70),
            (27, 66, 5, 49, 75, 54, 2,  60, 29, 40, 2,  55, 9,  15, 59, 18, 68, 3,  36, 5,  47, 77, 44, 38, 1,  18, 28, 76, 4,  34, 60, 63, 58, 80, 17, 54, 79, 75, 48, 54, 55, 19, 62, 64, 14, 47, 51, 70, 75, 5, 11, 47, 45, 58, 68, 69, 79, 25, 38, 45, 73, 47, 68, 50, 34, 45, 78, 26, 79, 57, 4, 56, 22, 60, 18, 75, 43, 60, 59, 67, 63, 42, 49, 33, 40, 65, 79, 77, 7, 3, 26, 62, 31, 78, 26, 57, 69, 40, 4, 23, 26, 13, 67, 42, 38, 72, 11, 39, 65, 60, 25, 6, 80, 66, 68, 77, 59, 78, 19),
            (77, 66, 5, 49, 75, 54, 2,  60, 29, 40, 2,  55, 9,  15, 59, 18, 68, 3,  36, 5,  47, 60, 21, 80, 1,  72, 55, 16, 82, 35, 57, 19, 1, 66, 18, 27, 39, 17, 74, 81, 39, 14, 78, 0, 25, 65, 43, 66, 64, 38, 81, 23, 24, 50, 57, 30, 71, 75, 26, 68, 54, 57, 56, 50, 71, 73, 14, 21, 8, 32, 26, 63, 5, 37, 19, 43, 66, 47, 53, 34, 66, 23, 73, 31, 54, 38, 77, 67, 11, 63, 79, 6, 22, 21, 51, 69, 74, 21, 5, 17, 67, 37, 29, 21, 60, 14, 82, 44, 30, 4, 20, 42, 35, 1, 31, 54, 46, 20, 40, 30),
            (33, 66, 5, 49, 75, 54, 2,  60, 29, 40, 2,  55, 9,  15, 59, 18, 68, 3,  36, 5,  47, 33, 21, 59, 44, 18, 28, 76, 59, 34, 60, 63, 79, 27, 12, 54, 5, 49, 48, 54, 55, 52, 62, 72, 69, 10, 57, 22, 58, 48, 67, 53, 7, 34, 32, 30, 31, 19, 26, 8, 34, 46, 7, 30, 71, 55, 34, 75, 54, 9, 6, 60, 5, 23, 25, 45, 42, 80, 25, 12, 22, 76, 20, 51, 62, 21, 40, 9, 41, 10, 44, 73, 8, 33, 70, 73, 6, 31, 21, 72, 5, 40, 61, 51, 42, 66, 64, 74, 61, 25, 63, 42, 24, 41))


if ONLY_X_PLUS:
    nm = []
    for m in messages:
        nm.append(m[X:])

    messages = nm



if RANDOM_MESSAGE:
    oldm = messages
    messages = []
    for i in range(len(oldm)):
        messages.append([])
        
        for j in range(len(oldm[i])):

            if not PRESERVE_REPEATED:
                messages[-1].append(random.randint(0,82))

            else:
            
                #preserve repeated sections
                for k in range(i):
                    
                    try :
                        if oldm[i][j] == oldm[k][j]:
                            messages[-1].append(messages[k][j])
                            break
                    except IndexError:
                        pass
                else:
                    messages[-1].append(random.randint(0,82))




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


def Trigraph_IoC(messages,mmin = 0, mmax=82):
    n = {}
    amount = 0
    for m in messages:
        amount += len(m)-2
        for c1, c2, c3 in zip(m[:-2], m[1:-1], m[2:]):
            v = (c1,c2,c3)
            n.setdefault(v,0)
            n[v]+=1
            

    if amount <= 1:
        return 0,0

    ic = 0
    for i in n.values():
        ic += i*(i-1)

    return ic  / (amount * (amount - 1) / math.comb(83, 2))



##def trigraph_ioc(msg):
##    nmsg = tuple()
##    for m in msg:
##        nmsg += tuple(m)
##    msg = nmsg
##    counts = {}
##    for i in range(len(msg)-2):
##        counts.setdefault(tuple(msg[i:i+3]), 0)
##        counts[tuple(msg[i:i+3])] += 1
##            
##    n = sum([a*(a-1) for a in counts.values()])
##    sz = len(msg)
##    d = (sz-2) * (sz-3)
##    return n / d

messageNames = ("e1","w1","e2","w2","e3","w3","e4","w4","e5")

def compare(l1, l2):
    if len(l1) != len(l2):
        return False

    for a1, a2 in zip(l1, l2):
        if a1 != a2:
            return False

    return True

exponents = [2, 5, 6, 8, 13, 14, 15, 18, 19, 20, 22, 24, 32, 34, 35, 39, 42, 43, 45, 46, 47, 50, 52, 53, 54, 55, 56, 57, 58, 60, 62, 66, 67, 71, 72, 73, 74, 76, 79, 80]

def get_bit_count(value):
   n = 0
   while value:
      n += 1
      value &= value-1
   return n

def sortedPrint(dictionary):
    l = list(dictionary.keys())
    l.sort(reverse=True, key=lambda a: dictionary[a])
    for i in l:
        print(i, dictionary[i])



for d in range(30):
    a = 0
    n = 0
    for m1, m2 in itertools.combinations(messages[:3], 2):
        for c1,c2 in zip(m1,m2[d:]):
            a += 1
            if c1==c2:
                n += 1
    print(d, n/a, a, n)
            
            
                 


        
        
        
    
    
    

















