
with open("Englishv4.txt","r") as f:
    for m in f.read().split("\n"):
        m = m.replace(" ","")
        for j in range(len(m)-10):
            if m[j]==m[j+1] and m[j+3] == m[j+4] and m[j+8]==m[j+9] and m[j+9]==m[j+10]:
                print(m[j:j+11].replace(" ", "-"))
