from itertools import permutations

eyeTris = ((2,0,0,2,3,1,0,1,0,1,4,3,2,2,2,0,2,3,3,0,0,1,0,4,0,4,4,2,2,1,1,3,2,2,4,0,2,3,1,2,2,2,1,1,2,0,2,4,3,1,1,0,1,3,0,3,0,3,0,3,0,0,2,1,0,4,0,2,3,1,4,4,0,0,1,3,1,0,3,1,2,1,3,0,2,2,3,3,1,1,0,4,1,0,3,4,0,0,0,1,3,0,2,0,1,2,3,0,1,0,1,0,2,4,0,4,1,2,4,0,1,4,2,1,3,4,1,4,3,1,3,2,0,3,4,1,4,3,0,2,3,1,4,2,0,3,4,1,4,4,2,4,2,1,1,1,0,1,0,0,4,4,0,0,3,1,3,3,2,1,4,2,3,2,1,1,3,1,4,4,1,3,1,2,2,0,0,4,1,1,0,1,1,1,0,0,1,0,1,0,0,0,4,0,2,4,1,0,2,1,2,4,4,2,1,1,0,0,4,2,4,4,0,3,4,2,4,1,0,0,4,2,0,1,1,3,1,1,3,3,3,1,0,2,4,2,2,0,4,2,2,3,3,0,4,3,1,1,0,3,0,0,3,1,1,3,4,1,1,1,1,1,0,0,2,2,1,1,3,2,1,2,1,0,3,0,2,3,2,2,4,1,3,3,1,4,3),(3,1,0,2,3,1,0,1,0,1,4,3,2,2,2,0,2,3,3,0,0,1,0,4,0,4,4,2,2,1,1,3,2,2,4,0,2,3,1,2,2,2,1,1,2,0,2,4,3,1,1,0,1,3,0,3,0,3,0,3,0,0,2,1,0,4,0,2,3,1,4,4,0,0,1,1,0,4,0,2,1,1,1,0,2,0,2,3,1,1,0,4,1,0,3,4,0,0,0,1,0,0,1,0,1,2,0,4,0,4,0,0,2,4,0,4,1,2,4,0,1,4,2,1,3,4,1,4,3,1,3,2,0,3,4,1,4,3,0,2,3,1,4,2,0,3,4,1,4,4,1,3,4,1,0,1,2,1,4,3,0,2,2,2,4,1,3,3,3,0,4,1,0,3,2,4,2,2,2,4,0,0,1,1,1,0,2,4,3,0,4,3,2,3,2,0,1,1,1,1,3,1,0,0,2,2,4,3,1,1,2,3,3,1,4,1,0,3,2,1,2,1,0,2,3,0,3,2,0,4,1,2,3,3,0,2,3,0,1,4,1,4,1,2,3,2,2,1,2,1,1,4,2,2,2,3,1,2,0,3,0,0,2,0,2,4,3,2,2,2,0,0,2,0,2,1,2,3,0,2,4,2,1,2,2,1,3,4,0,2,0,1,3,3,2,3,3,2,2,2,0,1,4,1,1,4,0,3,3),(1,2,1,2,3,1,0,1,0,1,4,3,2,2,2,0,2,3,3,0,0,1,0,4,0,4,4,2,2,1,1,3,2,2,4,0,2,3,1,2,2,2,1,1,2,0,2,4,3,1,1,0,1,3,0,3,0,3,0,3,0,0,2,1,0,4,0,2,3,1,4,4,0,0,1,2,3,4,3,0,1,2,0,2,0,1,4,1,4,3,2,3,1,3,1,0,0,4,2,2,2,4,2,1,2,1,3,0,1,4,4,3,0,3,0,0,3,0,3,1,2,1,1,0,3,4,1,4,2,1,3,0,3,1,0,0,1,1,0,2,3,2,2,4,1,0,4,1,4,4,2,2,4,2,2,3,0,1,1,1,4,4,1,1,1,0,2,3,0,3,1,0,2,0,1,4,0,0,4,4,1,0,1,3,0,2,0,2,0,2,2,0,3,1,1,2,2,1,1,1,4,2,0,4,2,4,0,0,4,1,0,3,0,0,0,4,2,3,1,3,0,2,1,3,2,1,2,2,1,1,0,0,4,2,0,0,0,0,2,1,1,3,1,2,4,2,2,1,2,0,4,0,0,4,3,2,1,2,2,3,0,1,3,1,0,4,3,0,3,3,2,4,2,1,3,2,0,1,0,0,0,3,1,0,1,3,0,3,0,1,3,0,1,0,2,0,4,1,4,0,3,0,2,1,0,0,2,2,4,2,2,1,0,3,1,1,3,4,2,0,4,2,0,1,0,4,0,2,2,3,1,0,0,0,2,1,1,0,1,1,4,0,2,0,3,2,2,0,1,2,3,1,1,4,),(3,0,1,2,3,1,0,1,0,1,4,4,3,0,0,2,0,4,2,3,4,1,4,1,1,1,2,0,0,1,1,3,2,2,2,0,1,0,1,1,4,3,2,0,0,3,1,0,1,1,2,0,4,4,2,1,0,2,2,1,1,4,2,0,2,2,0,4,1,0,2,2,1,4,4,2,0,4,1,1,4,1,0,0,1,2,1,0,3,0,2,1,1,2,1,0,0,4,0,0,1,4,0,1,3,2,2,2,0,2,3,3,1,2,0,1,4,1,3,4,1,0,4,2,2,0,2,0,3,3,1,2,1,3,2,3,1,0,0,1,0,1,3,3,2,4,1,0,0,3,3,1,0,3,0,2,1,4,2,3,0,3,1,1,4,1,0,0,2,2,2,0,3,3,0,2,0,1,4,4,2,2,2,2,2,4,2,0,2,3,1,1,0,2,1,2,3,1,2,2,2,0,2,3,1,4,2,0,3,2,2,0,2,2,4,0,1,0,1,0,4,3,1,1,2,1,1,1,2,2,4,0,4,3,1,2,0,1,1,2,2,0,0,0,1,1,0,0,1,1,0,0,0,1,3,1,2,2,1,4,2,1,3,3,1,0,1,3,0,1,2,3,0,2,3,3,3,1,0,0,3,2,0,1,2,1,4,0,2,2,3,0,2,4,2,0,3,2,2,3,2,2,0,0,3,1,),(2,2,3,2,3,1,0,1,0,1,4,4,3,0,0,2,0,4,0,0,2,2,2,0,1,0,4,1,3,0,3,0,3,1,4,2,2,2,0,3,0,0,2,3,2,2,4,1,2,2,0,0,0,2,2,3,0,0,1,2,1,4,2,0,2,4,1,4,0,2,4,4,2,1,4,1,3,1,3,1,0,0,2,3,2,2,0,0,2,3,3,1,1,0,4,2,1,2,0,2,0,0,1,3,0,1,2,4,0,0,2,2,1,4,1,4,3,1,1,1,3,0,1,0,0,2,3,1,0,3,0,0,0,0,1,2,1,1,2,3,2,0,2,1,0,4,1,0,1,3,1,3,0,2,3,0,1,4,0,3,0,0,2,1,0,1,2,4,2,2,0,1,3,2,0,2,3,0,0,3,0,4,2,2,1,2,0,0,2,0,1,1,2,1,3,0,1,4,2,4,0,0,0,1,2,1,3,2,1,1,2,2,3,2,3,3,1,0,0,3,0,4,0,1,2,0,4,0,0,3,4,2,2,4,0,0,2,2,3,1,2,4,3,1,1,0,2,4,1,0,3,1,0,2,2,1,1,0,2,3,0,1,2,2,0,4,0,0,2,3,0,4,2,2,2,3,0,3,3,1,4,1,2,2,4,2,1,4,1,3,1,3,1,1,3,1,2,0,4,2,3,0,3,1,2,1,1,4,2,0,3,2,0,0,4,0,1,1,0,3,2,0,1,0,1,2,1,3,0,4,2,2,3,0,0,1,2,2,4,2,3,4,0,3,0,1,3,3,0,0,4,2,1,3,2,1,1,1,1,1,0,2,4,2,2,4,2,1,3,0,3,3,1,3,4,3,0,3,2,3,4,0,0,1,0,0,0,1,4,1,0,4,0,2,4,1,2,4,3,1,0,0,1,2,0,0,1,3,0,4,4),(1,1,4,2,3,1,0,1,0,1,4,4,3,0,0,2,0,4,0,4,3,2,4,4,0,2,1,0,2,3,1,0,3,1,0,1,0,3,4,1,4,3,2,3,2,2,1,2,1,2,2,2,2,0,1,1,4,1,0,3,2,4,4,0,2,0,0,3,2,1,1,2,0,2,1,0,3,3,0,3,4,1,3,3,0,3,4,3,1,1,1,3,2,0,0,4,2,2,2,0,1,4,1,4,1,1,4,4,1,1,2,2,0,1,3,0,1,2,1,3,0,0,4,1,3,3,1,4,2,0,3,2,2,3,2,3,0,4,0,4,1,1,1,2,1,3,4,0,3,1,1,1,0,1,2,2,1,0,1,1,0,3,1,3,1,2,3,3,2,1,2,1,1,4,2,0,1,0,2,0,2,3,4,2,4,0,0,1,3,0,1,1,1,4,1,1,3,3,0,3,3,1,2,4,1,4,2,1,3,3,0,3,0,0,2,3,1,1,3,1,1,0,1,2,0,2,2,2,1,2,2,0,0,0,1,2,2,0,1,0,1,2,3,2,1,0,1,2,2,0,2,3,1,3,0,1,0,0,0,1,4,0,4,1,0,2,1,2,2,4,0,1,0,3,0,4,1,3,2,2,3,3,0,2,1,2,4,1,0,2,1,1,4,3,0,0,3,2,3,2,2,2,1,1,3,0,0,4,2,0,2,4,1,2,0,2,0,0,2,2,1,1,2,4,0,2,1,0,0,2,2,3,1,1,4,4,2,0,1,2,0,3,0,3,2,2,4,3,1,2,1,3,0,0,2,4,4,2,0,4,0,4,4,1,1,0,2,0,4,2,4,0,),(1,0,2,2,3,1,0,1,0,1,4,4,3,0,0,2,0,4,0,0,2,2,2,0,1,0,4,1,3,0,0,0,2,2,1,0,0,1,4,0,3,0,2,1,4,0,3,3,2,3,3,0,0,3,1,2,1,0,1,0,1,4,2,3,0,2,1,3,4,1,2,3,0,0,1,0,3,3,1,0,3,3,0,1,0,0,4,1,1,4,2,2,0,2,2,3,2,1,3,3,1,0,0,3,2,2,0,4,3,0,4,3,0,0,1,4,3,2,0,4,2,1,0,0,3,4,2,2,2,2,2,4,0,2,4,1,4,2,2,0,1,2,4,0,3,0,0,0,1,0,0,2,1,1,4,2,1,4,0,2,1,3,2,3,3,2,3,4,3,0,4,1,0,0,1,2,3,1,4,0,2,4,3,1,4,2,2,3,3,2,0,0,1,1,4,1,4,0,3,0,3,1,0,1,3,0,4,2,1,2,0,0,4,2,1,1,0,4,2,2,2,0,0,3,3,3,0,0,1,3,3,2,2,0,2,1,4,2,3,2,2,2,3,1,3,2,1,4,4,1,1,3,1,3,0,2,3,0,3,0,4,3,0,2,0,1,2,0,0,3,1,0,1,2,2,2,1,1,1,3,0,3,1,0,1,2,1,2,2,3,4,1,3,0,0,0,4,0,4,3,1,0,1,0,2,3,2,3,2,1,3,2,1,2,3,2,4,2,0,2,1,1,2,4,2,3,0,2,2,0,1,0,0,0,1,1,3,1,0,2,3,1,2,3,3,3,0,2,2,1,4,3,0,3,0,3,4),(3,0,2,2,3,1,0,1,0,1,4,4,3,0,0,2,0,4,0,0,2,2,2,0,1,0,4,1,3,0,0,0,2,2,1,0,0,1,4,0,3,0,2,1,4,0,3,3,2,3,3,0,0,3,1,2,1,0,1,0,1,4,2,2,2,0,0,4,1,3,1,0,0,0,1,2,4,2,2,1,0,0,3,1,3,1,2,1,2,0,2,1,2,0,3,4,0,0,1,2,3,1,0,3,3,1,0,2,1,2,4,0,3,2,2,4,4,3,1,1,1,2,4,0,2,4,3,0,3,0,0,0,1,0,0,2,3,0,1,3,3,2,3,1,2,2,4,1,2,3,3,1,1,0,4,3,0,4,4,2,0,0,2,1,2,1,1,0,2,4,1,3,0,0,1,0,1,2,3,3,2,0,4,2,1,2,2,1,1,2,0,0,2,4,1,2,4,3,0,2,4,0,4,1,0,1,3,1,1,2,1,0,1,2,2,3,0,1,0,1,2,2,0,3,4,1,3,3,2,3,1,1,4,2,2,0,3,1,1,4,2,3,1,0,4,3,2,4,3,1,1,1,2,0,4,1,2,3,3,0,2,2,3,2,0,2,1,2,2,3,3,0,4,0,1,1,0,4,2,0,4,1,2,0,1,2,3,4,2,4,4,0,4,1,0,1,0,0,3,2,2,3,2,1,2,2,1,0,4,0,4,1,2,2,0,0,2,4,3,1,2,1,3,4,1,1,0,0,0,4,0,4,0,1,3,2,1,2,0,0,0,1,1,1,1,2,0,4,1,4,1,0,4,0,1,3,0,1,1,0,),(1,1,3,2,3,1,0,1,0,1,4,4,3,0,0,2,0,4,0,0,2,2,2,0,1,0,4,1,3,0,0,0,2,2,1,0,0,1,4,0,3,0,2,1,4,0,3,3,2,3,3,0,0,3,1,2,1,0,1,0,1,4,2,1,1,3,0,4,1,2,1,4,1,3,4,0,3,3,1,0,3,3,0,1,2,1,4,1,1,4,2,2,0,2,2,3,3,0,4,1,0,2,0,2,2,2,0,4,0,1,0,1,4,4,1,4,3,2,0,4,2,1,0,2,0,2,2,2,2,2,4,2,2,3,4,0,2,0,2,1,2,0,4,2,2,1,3,1,4,3,2,3,2,2,0,3,0,1,2,1,1,4,1,1,2,1,1,0,1,1,1,0,3,4,1,0,1,0,1,3,1,1,4,1,4,1,0,1,2,1,1,0,2,4,1,2,1,0,1,1,4,3,0,0,2,0,4,0,1,4,0,1,1,2,2,0,0,1,0,0,4,3,1,0,0,1,4,0,1,3,2,3,1,0,1,0,0,0,2,2,0,4,2,3,0,1,0,4,0,2,0,1,2,2,2,0,4,1,1,3,0,0,1,4,1,3,1,0,2,0,1,3,4,2,4,3,0,1,3,1,1,3,2,4,0,2,4,3,0,1,1,1,1,1,0,4,1,2,4,2,0,1,0,1,3,0,2,2,1,2,0,1,1,3,2,2,3,1,2,2,4,2,4,4,2,2,1,1,0,0,2,2,3,1,3,2,0,4,4,1,3,1,))

eyeNorm = ((2,0,1,0,1,3,2,2,3,3,0,4,0,4,1,1,3,0,2,3,2,1,1,4,3,1,3,0,3,3,0,0,4,0,2,4,0,0,0,0,3,2,0,4,1,2,2,0,0,0,1,4,2,2,2,4,2,1,2,2,2,2,0,1,1,0,0,0,3,2,0,1,3,4,1,1,1,3,3,1,0,2,2,1,0,4,4,0,0,0,2,0,0,1,0,4,0,4,0,1,4,4,1,4,2,0,3,3,0,2,2,0,3,4,2,4,1,2,3,1,3,1,3,1,3,0,0,3,1,1,3,2,1,2,0,1,4,2,2,3,1,3,3,1,4,4,1,3,4,1,4,4,1,2,1,1,0,1,4,0,0,3,2,1,2,1,1,4,1,3,0,0,4,1,1,1,0,1,0,0,2,4,1,2,4,1,0,0,4,0,3,1,0,0,1,0,4,0,3,3,1,4,3,2,3,4,1,1,2,2,1,0,1,0,1,0,0,4,0,1,2,0,4,1,2,4,4,2,4,4,2,4,0,2,1,3,3,3,1,2,2,0,3,3,0,1,0,3,1,1,3,1,1,1,2,1,1,2,1,0,3,2,2,3,1,4,1,3,1,0,4,2,4,2,2,4,1,3,0,3,0,4,1,1,0,2,0,3,1,2,3,2,0,4,3,1,3,),(3,1,1,0,1,3,2,2,3,3,0,4,0,4,1,1,3,0,2,3,2,1,1,4,3,1,3,0,3,3,0,0,4,0,2,4,0,0,4,0,3,2,0,4,1,2,2,0,0,0,1,4,2,2,2,4,2,1,2,2,2,2,0,1,1,0,0,0,3,2,0,1,3,4,1,1,0,1,0,2,0,2,0,1,0,4,4,0,0,0,1,0,4,0,4,4,0,4,0,1,4,4,1,4,2,0,3,3,0,2,2,0,3,4,1,3,1,1,1,1,2,1,3,1,3,0,0,0,1,1,0,2,0,2,0,1,4,2,2,3,1,3,3,1,4,4,1,3,4,1,4,4,1,4,0,1,2,1,2,2,2,3,3,0,3,2,4,4,0,0,0,2,4,3,2,3,1,1,1,0,2,2,1,2,3,1,0,3,1,0,2,2,0,4,3,4,0,3,4,3,1,4,0,1,2,2,2,1,1,1,3,4,0,2,1,0,3,0,1,4,1,3,3,4,1,2,2,1,3,3,0,1,3,2,0,2,4,1,4,2,2,1,4,2,2,2,0,3,0,2,4,2,0,0,1,2,3,2,1,2,4,0,2,3,2,3,2,0,1,4,0,3,3,1,0,1,3,2,2,1,1,2,1,3,0,2,0,3,2,2,2,2,0,0,4,2,2,3,1,0,3,1,3,2,2,4,1,1,3,),(1,2,1,0,1,3,2,2,3,3,0,4,0,4,1,1,3,0,2,3,2,1,1,4,3,1,3,0,3,3,0,0,4,0,2,4,0,0,4,1,3,2,0,4,1,2,2,0,0,0,1,4,2,2,2,4,2,1,2,2,2,2,0,1,1,0,0,0,3,2,0,1,3,4,1,1,3,2,3,0,2,0,1,3,2,3,0,0,4,4,2,1,0,1,4,3,0,0,1,2,1,4,1,4,0,3,1,1,0,2,4,1,0,4,2,2,3,1,0,2,4,4,1,1,1,3,2,2,2,2,3,1,4,0,3,3,3,0,1,3,0,2,3,1,0,1,0,3,2,2,4,4,1,4,2,2,0,1,4,1,1,3,0,3,0,1,4,4,1,0,2,0,2,0,3,1,1,1,1,4,2,4,1,0,3,4,2,3,2,1,3,2,1,1,2,1,4,1,1,2,0,1,2,0,0,4,0,1,0,3,0,2,2,1,2,2,4,0,2,0,4,0,0,0,0,1,0,3,2,2,1,0,4,0,0,0,1,1,3,2,2,1,0,0,4,2,2,3,1,0,4,3,2,4,2,0,1,3,1,0,3,0,1,0,2,0,0,3,0,0,2,2,1,0,2,0,1,4,2,2,4,0,3,1,2,0,3,1,3,3,0,2,3,1,0,0,0,1,0,3,3,1,0,4,4,1,2,0,1,4,2,2,0,3,4,2,0,1,0,4,3,1,0,1,1,0,0,2,0,0,1,2,4,1,3,1,4,0,2,0,2,2,0,2,0,1,4,1,3,2,2,3,1,1),(3,0,1,0,1,4,3,0,4,2,3,1,1,1,1,1,3,0,1,0,3,2,0,0,1,1,4,2,1,1,1,4,2,0,4,2,1,4,4,1,3,2,0,4,1,0,0,2,4,4,1,2,0,0,2,2,2,1,4,1,0,1,3,2,4,0,0,2,2,2,2,0,1,2,0,4,0,2,1,1,0,1,2,0,2,1,0,0,4,4,0,1,2,0,2,2,0,1,4,1,0,0,2,0,2,1,3,0,0,1,3,2,4,3,3,1,2,4,0,1,1,3,0,1,1,2,0,1,0,3,2,2,3,1,3,4,3,1,4,2,2,3,1,3,2,1,3,0,3,1,1,0,0,0,0,3,1,4,3,1,1,0,2,2,3,0,2,4,2,2,4,2,0,1,0,2,1,2,2,3,1,4,2,2,0,0,1,0,3,1,1,1,2,2,3,2,0,3,4,0,1,2,3,0,0,4,1,2,2,2,2,1,3,1,3,2,2,2,0,2,3,0,2,4,2,1,4,0,2,1,1,4,4,0,1,2,2,2,0,1,0,0,0,0,1,2,1,4,3,1,0,1,2,3,3,3,1,2,0,1,0,2,2,4,2,0,3,2,2,1,0,1,1,0,1,0,1,0,1,3,2,1,2,3,1,1,0,3,0,3,2,0,3,0,2,4,1,3,2,0,3,2,2,0,3,0),(2,2,1,0,1,4,3,0,4,0,0,0,1,0,0,3,0,2,2,2,0,2,3,1,2,2,2,2,3,2,1,4,4,1,4,4,2,1,1,3,3,2,0,4,1,0,0,2,2,2,2,4,3,1,3,4,1,0,0,3,2,4,2,0,0,0,0,1,0,2,2,0,0,4,2,4,3,1,3,1,3,2,2,3,3,1,2,1,2,0,1,3,4,0,0,4,1,4,1,3,0,2,3,1,0,0,0,1,2,3,1,0,4,3,1,3,0,0,2,0,0,2,0,1,4,0,0,0,2,0,2,1,2,1,2,3,1,1,1,0,0,0,0,3,1,1,2,2,2,0,1,1,0,0,3,2,1,4,0,2,1,4,2,2,2,0,2,3,0,4,2,0,0,1,2,1,4,2,4,1,2,1,1,2,2,3,1,0,4,0,1,0,0,3,4,0,0,3,0,2,1,0,3,1,3,0,0,2,1,2,2,1,0,3,1,0,0,0,0,3,1,2,3,3,2,0,0,3,2,4,0,4,2,2,0,0,1,2,4,0,2,4,1,0,2,0,2,3,2,0,4,3,0,4,3,0,3,1,2,2,4,1,3,1,3,1,2,3,0,1,1,4,2,2,3,2,3,1,1,1,3,0,2,1,1,0,2,1,0,2,0,2,2,2,3,4,1,4,1,2,1,1,3,2,4,0,3,2,1,2,3,0,0,0,1,0,3,0,1,2,4,2,2,1,2,2,4,0,3,3,0,0,3,2,1,1,0,2,4,2,1,3,1,3,3,2,3,1,0,0,1,4,1,0,2,1,0,1,0,3,3,0,0,4,3,2,0,3,1,4,1,2,1,1,1,4,2,2,3,3,0,4,0,3,4,0,0,0,4,1,0,4,1,2,4,0,1,2,3,0,4,5,0,4,2,3,0,1,0,1,0,4),(1,1,1,0,1,4,3,0,4,0,4,4,0,2,3,1,0,1,0,3,3,2,3,2,1,2,0,1,1,3,2,4,0,0,3,2,0,2,3,4,3,2,0,4,1,0,0,2,3,4,2,1,2,0,3,0,1,4,4,1,2,1,2,2,2,2,4,0,1,4,2,0,2,1,1,1,3,0,0,3,3,0,3,1,1,3,4,2,2,4,1,4,4,1,1,1,3,0,3,0,0,3,1,4,2,2,3,4,0,4,2,1,3,1,1,1,2,4,3,1,4,1,3,2,0,0,2,1,0,1,4,1,2,0,2,1,1,2,4,3,1,2,3,0,2,0,3,1,1,1,4,3,0,0,2,1,1,0,3,1,3,3,2,1,4,2,0,0,2,3,0,0,1,1,1,4,3,0,3,4,1,4,3,0,3,3,1,1,0,1,2,2,1,2,0,1,0,1,1,3,2,2,1,1,1,2,0,4,4,2,3,1,0,1,3,1,3,2,1,2,3,1,0,2,0,3,1,1,0,2,2,2,0,0,1,2,0,1,2,0,1,2,3,1,3,0,0,1,1,0,2,4,0,1,4,1,3,3,0,2,1,0,2,3,0,0,2,2,2,0,0,4,4,2,1,0,3,1,2,2,2,0,0,0,1,4,4,0,1,2,2,0,0,3,2,3,2,1,4,2,1,4,1,3,3,2,1,3,1,2,2,0,1,2,0,2,2,4,0,2,2,2,3,4,2,0,3,0,3,3,1,2,0,2,4,4,0,4,0,2,0,0,0,0,2,1,2,1,1,0,0,1,4,1,1,0,2,2,4,2,1,0,3,4,0,2,4,1,1,4,4,2),(1,0,1,0,1,4,3,0,4,0,0,0,1,0,0,0,0,0,0,1,0,2,1,3,2,3,3,1,2,0,1,4,2,1,3,3,0,0,3,2,3,2,0,4,1,0,0,2,2,2,2,4,3,1,2,1,2,4,3,0,4,3,0,3,0,0,1,1,0,2,0,3,4,2,1,1,3,0,1,0,1,0,0,4,2,2,3,2,1,0,0,3,4,3,0,0,1,4,4,2,1,4,2,2,4,0,2,2,2,0,0,3,0,0,0,2,2,3,0,3,4,1,1,0,2,2,3,1,3,2,0,2,4,0,3,3,0,2,0,3,0,2,2,2,4,4,1,1,4,2,0,1,0,1,4,1,1,4,3,2,3,4,3,0,0,1,2,0,2,4,2,2,3,0,1,1,0,3,0,1,3,0,2,0,0,1,0,4,0,0,3,0,1,3,0,0,1,2,3,3,2,4,0,1,3,4,1,3,4,1,3,0,2,4,4,1,3,0,1,4,1,2,4,1,2,2,2,2,3,0,3,3,2,2,2,1,2,2,2,2,1,4,3,1,3,0,3,0,2,0,1,3,1,0,2,1,1,3,1,0,2,2,3,0,0,0,3,1,0,3,2,3,2,4,3,2,3,3,1,4,1,1,0,3,2,4,0,3,2,0,0,1,2,2,1,0,3,1,1,2,4,3,1,4,4,0,1,2,0,2,3,1,1,2,2,0,2,4,2,3,0,1,0,1,3,1,1,2,3,2,2,1,3,0,3,3,4,2,1,2,1,0,2,2,0,1,0,0,3,2,3,0,3,4,0,3,4,),(3,0,1,0,1,4,3,0,4,0,0,0,1,0,0,0,0,0,0,1,0,2,1,3,2,3,3,1,2,0,1,4,0,0,4,0,0,0,2,2,3,2,0,4,1,0,0,2,2,2,2,4,3,1,2,1,2,4,3,0,4,3,0,3,0,0,1,1,0,2,2,2,1,1,3,1,4,2,2,1,1,3,1,0,2,1,4,0,0,1,0,3,2,1,2,2,2,4,1,1,2,4,3,0,0,1,0,0,1,3,1,2,2,3,3,1,3,0,3,0,2,2,1,2,3,0,1,3,2,3,0,1,4,3,0,4,1,3,4,2,0,3,0,0,0,3,2,3,3,2,4,2,1,1,4,0,0,4,0,2,1,0,2,4,0,1,0,3,2,0,2,2,1,0,2,4,3,0,2,1,0,1,2,1,0,3,0,1,2,0,3,3,2,3,2,4,0,2,2,1,1,1,0,3,1,3,2,4,1,2,1,0,2,1,4,2,4,4,0,3,1,1,1,2,2,0,2,1,4,3,1,1,4,1,2,0,4,2,3,3,2,4,1,2,0,3,3,0,2,0,2,3,3,0,1,0,4,1,2,0,4,2,4,1,0,1,2,2,3,2,1,0,1,3,1,1,1,4,0,3,1,1,4,2,1,2,3,2,1,2,2,4,1,0,2,4,0,1,3,2,4,4,0,0,3,0,2,2,1,4,4,0,2,2,4,3,1,4,1,1,4,0,4,2,1,2,1,1,1,4,1,4,0,1,3,0,0,2,0,2,3,1,0,0,0,0,3,1,0,0,0,1,0,2,1,4,0,0,1,1),(1,1,1,0,1,4,3,0,4,0,0,0,1,0,0,0,0,0,0,1,0,2,1,3,2,3,3,1,2,0,1,4,3,0,4,4,1,3,3,3,3,2,0,4,1,0,0,2,2,2,2,4,3,1,2,1,2,4,3,0,4,3,0,3,0,0,1,1,0,2,1,1,1,1,2,4,3,0,1,0,1,2,1,4,2,2,3,3,0,2,0,2,4,0,1,4,1,4,4,2,1,2,2,2,2,2,3,0,2,1,2,2,1,3,2,3,3,3,0,3,4,1,1,0,2,2,4,0,1,2,0,2,0,4,1,3,0,2,0,0,2,2,4,2,4,2,0,2,4,0,3,4,1,2,0,2,0,1,4,1,1,0,1,1,4,1,0,3,1,1,1,0,1,0,2,4,0,1,1,0,2,0,4,0,1,0,0,1,3,1,0,0,1,3,0,2,1,1,2,1,1,1,3,0,1,1,0,4,4,1,2,1,1,1,1,2,4,0,3,4,1,0,1,2,2,0,4,0,0,4,1,2,1,3,1,0,2,0,4,1,0,4,1,2,2,1,1,3,4,1,3,0,1,3,3,0,1,3,2,4,3,0,1,1,0,4,2,0,1,0,2,2,1,0,2,0,2,0,3,0,0,2,2,4,0,0,1,0,1,2,0,4,4,2,3,1,1,0,4,2,1,1,1,1,4,2,0,3,1,1,0,2,1,3,1,2,2,4,2,2,0,2,2,2,0,4,1,5,2,3,2,4,4,2,1,0,1,3,3,1,4,3,1,))

RANDOM_TRIS = False

if RANDOM_TRIS:
    import random
    eyeTris = []
    for i in range(9):
        eyeTris.append([])
        for j in range(103):
            a = random.randint(0,83)
            eyeTris[-1] += [a//25, (a%25)//5, a%5] 


def permute(a,b):
    ret = []
    for i in b:
        ret.append(a[i])
    return ret


for t1o in permutations(range(3)):
    for t2o in permutations(range(3)):
        for eyeMap in permutations(range(5)):
            s = set()

            for m in eyeTris:
                for i in range(0, len(m)-2, 3):
                    tri = None
                    if (i//3)%2 == 0:
                        tri = permute(m[i:i+3], t1o)
                    else:
                        tri = permute(m[i:i+3], t2o)
                    
                    tri = tuple(map(lambda a: eyeMap[a], tri))
                    s.add(tri)
                    
            s = list(map(lambda a: a[0]*25+a[1]*5+a[2], s))
            if len(s)<=83:
                print(t1o, t2o, eyeMap, len(s))
                    

