

messages_raw = [
    #barren temple
    "112612242114111212212611115224122121",
    "112612151111412221236122422412212111261134111141111121211161",
    #henkeva temple
    "224111113212111111263114112411113111361211411111121112112226324215121121113632411114111112111126",
    #ominous temple
    "11412221236122422412212111261134111141111121211161215",
    "1124111212236121513411122121261211112224121",
    #lohkare temple
    "1112111211222632421512112111363241111411111211112612242",
    "11411121221261111522412212111261215111141",
    #watchtower
    "1161215112411121223612151341112212126121111222412111221",
    "2631521141112211136113422421222112612242114",
    #pillar
    "121121113631511241\
211122126315211411\
122111126121511241\
121111236315112412\
2111113612114221111\
21211213612111111112\
421112121161211421\
14122212363151115\
121121236324224212\
221126311411241123\
121263151342121111\
".replace("\n","")
]

m2 = []
for m in messages_raw:
    m2.append(m.replace("6","0"))


messages_raw = m2


merged_message = ["2241111132121111112631141124111131113612114111\
11121112112226324215121121113632411114111112111126\
1224211411121221261111522412212111261215111141\
2221236122422412212111261134111141111121211161\
2151124111212236121513411122121261211112224121\
112212631521141112211136113422421222112612242114\
".replace("\n","") + messages_raw[-1]]


#check glyph-interval-sums
for i in range(6):
    s= set()
    for m in messages_raw:
        for j in range(len(m)-2):
            if int(m[j])==i:
                for k in range(j+2, len(m)):
                    if m[j]==m[k]:
                        l = list(m[j+1:k])
                        s.add(sum(map(lambda a:int(a),l)))
                        break

    print(i,s)

print()

#bruteforce glyph value assignment
i=0
s= set()
for m in messages_raw:
    for j in range(len(m)-2):
        if int(m[j])==i:
            for k in range(j+2, len(m)):
                if m[j]==m[k]:
                    l = list(m[j+1:k])
                    l.sort()
                    s.add(tuple(l))
                    break

    



cs = []

for ss in s:
    c = []
    for i in range(1,6):
        c.append(ss.count(str(i)))
    cs.append(c)


best = 120000
bestV = []

for a in range(1,15):
    print(a)
    for b in range(1,15):
        for c in range(1,15):
            for d in range(1,15):
                for e in range(1,15):
                    dd = set()
                    for s in cs:
                        dd.add(s[0]*a + s[1]*b + s[2]*c + s[3]*d + s[4]*e)
                    l = len(dd)
                    if l<best:
                        best = l
                        bestV = [(a,b,c,d,e, dd)]
                    elif l==best:
                        bestV.append((a,b,c,d,e, dd))


print(best, bestV)
                        
                    
