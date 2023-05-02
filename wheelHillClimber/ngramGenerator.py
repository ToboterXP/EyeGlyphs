import os

ngramDirectory = "./englishTexts"
ngramLength = 5
ngramFileNames = ("english_monograms_punctuation.txt","english_quintgram_punctuation.txt")

toUpper = True
alphabet = "0123456789abcdefghijklmnopqrstuvwxyz ,.!?-;:'\"".upper()

monogramCounts = {}

for c in alphabet:
    monogramCounts[c] = 0
    
ngramCounts = {}

i = 0
for fileName in os.scandir(ngramDirectory):
    print("File",fileName)
    with open(fileName, "r") as file:
        buffer = ""
        for line in file:
            if toUpper:
                line = line.upper()
            
            for c in filter(lambda c: c in alphabet, line):
                buffer += c

                if "  " in buffer:
                    if len(buffer) == ngramLength:
                        buffer = buffer[1:]
                    continue
                monogramCounts[c] += 1

                if len(buffer) == ngramLength:
                    ngramCounts[buffer] = ngramCounts.setdefault(buffer,0) + 1
                    buffer = buffer[1:]

with open(ngramFileNames[0],"w") as file:
    for c in monogramCounts.keys():
        file.write(f"{c}$${monogramCounts[c]}\n")

with open(ngramFileNames[1],"w") as file:
    for c in ngramCounts.keys():
        file.write(f"{c}$${ngramCounts[c]}\n")
                    

                        
