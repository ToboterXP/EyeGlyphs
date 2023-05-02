
largest_chain = (33, 77, 79, 63, 31, 69, 17)


for i in range(len(largest_chain)-1):
    print((largest_chain[i+1] - largest_chain[i])%83)


##
##alphabet = []
##
##
##
##for k in range(1,83):
##
##
##    alphabet = []
##    a = 0
##    for i in range(83):
##        alphabet.append(2*(a + k) % 83)
##        a+= k
##
##    try:
##
##        ci = []
##        for i in range(len(largest_chain)-1):
##            ci.append((alphabet.index(largest_chain[i]) - alphabet.index(largest_chain[i+1])) % 83)
##
##
##        print(k, ci)
##    except:
##        pass
