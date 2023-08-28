
ngrams = {}

with open("finnish_trigrams.txt", "r") as f:
    for line in f.readlines():
        ngram, count = line.split(" ")
        ngrams[ngram] = int(count)



repeatCount = 0
for ngram in ngrams.keys():
    if ngram[0] == ngram[-1]:
        repeatCount += ngrams[ngram]


print(repeatCount, repeatCount/sum(ngrams.values()), repeatCount/sum(ngrams.values())*1036)



