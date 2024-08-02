

messages_raw = [
    #barren temple
    "112612242114111212212611115224122121"+
    "112612151111412221236122422412212111261134111141111121211161",
    #henkeva temple
    "224111113212111111263114112411113111361211411111121112112226324215121121113632411114111112111126",
    #ominous temple
    "11412221236122422412212111261134111141111121211161215"+
    "1124111212236121513411122121261211112224121",
    #lohkare temple
    "1112111211222632421512112111363241111411111211112612242"+
    "11411121221261111522412212111261215111141",
    #watchtower
    "1161215112411121223612151341112212126121111222412111221"+
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



merged_message = messages_raw[1][:46] + messages_raw[3][:46] + messages_raw[0][:46] + messages_raw[2][:46] + messages_raw[4] + messages_raw[5]

messages_raw = merged_message.split("0")

shared_sections = [] #format [section, [[message, start, end],..]

def add_section(section, occurences):
    for s in shared_sections[:]:
        matched = 0
        for o in occurences:
            for o2 in s[1]:
                if o[0] == o2[0] and o[1]>=o2[1] and o[2]<=o2[2]:
                    matched += 1
                    break
        if matched == len(occurences):
            return #is subsection of a known section
            
    shared_sections.append([section, occurences])
                
    
for l in range(50, 5, -1):
    print(l)
    for mi,m in enumerate(messages_raw):
        if len(m)>=l:
            for i in range(len(m)-l+1):
                s = m[i:i+l]
                occs = [[mi, i, i+l]]
                
                for j in range(i+1,len(m)-l+1):
                    if m[j:j+l] == s:
                        occs.append([mi, j, j+l])
                        
                for m2i, m2 in enumerate(messages_raw[mi+1:]):
                    for j in range(len(m2)-l+1):
                        if m2[j:j+l] == s:
                            occs.append([m2i+mi+1, j, j+l])

                if len(occs)>=2:
                    add_section(s, occs)


for i in range(len(messages_raw)):
    print(i, len(messages_raw[i]), messages_raw[i])


for s in shared_sections:
    print(*s)
    





                        
                    
