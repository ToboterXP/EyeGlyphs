

messages_raw = [
    #barren temple
    "112012242114111212212011115224122121"+
    "112012151111412221230122422412212111201134111141111121211101",
    #henkeva temple
    "224111113212111111203114112411113111301211411111121112112220324215121121113032411114111112111120",
    #ominous temple
    "11412221230122422412212111201134111141111121211101215"+
    "1124111212230121513411122121201211112224121",
    #lohkare temple
    "1112111211222032421512112111303241111411111211112012242"+
    "11411121221201111522412212111201215111141",
    #watchtower
    "1101215112411121223012151341112212120121111222412111221"+
    "2031521141112211130113422421222112012242114",
    #pillar
    "121121113031511241\
211122120315211411\
122111120121511241\
121111230315112412\
2111113012114221111\
21211213012111111112\
421112121101211421\
14122212303151115\
121121230324224212\
221120311411241123\
121203151342121111\
".replace("\n","")
]


def sortedPrint(dictionary):
    l = list(dictionary.keys())
    l.sort(reverse=True, key=lambda a: dictionary[a])
    for i in l:
        print(i, dictionary[i])


def IoC(messages, precalc=True, mmin = 1, mmax=5):



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


merged_message = "1"+messages_raw[1][:46] + messages_raw[3][:46] + messages_raw[0][:46] + messages_raw[2][:46] + messages_raw[4] + messages_raw[5]

merged_message = merged_message.rstrip("12345")[:-1]




p = 2


for l in merged_message.split("0"):
    print(l, len(l)+1)
    n = [0]*p
    t = [0]*p
    for i in range(len(l)):
        if l[i]=="1":
            n[i%p]+=1
        t[i%p]+=1
    for i in range(p):
        print(round(n[i]/t[i],3), end=" ")
    print()
    
    
        





                    
