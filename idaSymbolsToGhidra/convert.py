files = ("message(1).txt","message(2).txt")


ret = ""

for fn in files:
    with open(fn) as f:
        for l in f.readlines():
            s = l.split("\t")
            ret += f"{s[0]}\t{s[2]}\n"

with open("symbols.txt","w") as f:
    f.write(ret)
