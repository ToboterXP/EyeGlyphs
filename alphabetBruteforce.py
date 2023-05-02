



chain = (33, 77, 79, 63, 31, 69, 17)


for a1 in range(83):
    print(a1)
    for a2 in range(83):
        for a3 in range(83):
            alphabet = []
            
            for i in range(83):
                alphabet.append( (a1 * (a2**((a3 * i)%83)) )% 83)

            if len(set(alphabet)) < 83:
                continue

            d = []
            for i in range(len(chain)-1):
                d.append( (alphabet.index(chain[i]) - alphabet.index(chain[i+1])) % 83 )

            l = len(set(d))
            if l < len(chain) - 1:
                print(a1, a2, a3, l - len(chain) + 1)
                                 
