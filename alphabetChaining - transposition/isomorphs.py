from dataclasses import dataclass


def _containsPattern(a,b):
    assert len(a) >= len(b)

    for offset in range(len(a) - len(b) + 1):
        orig = a[offset : offset + len(b)]
        ignore = set()
        for c in orig:
            if orig.count(c) == 1:
                ignore.add(c)
        
        mapping = {}
        for i in range(0, len(b)):
            c1 = a[i+offset]
            c2 = b[i]

            if c1 == "." and c2 == ".":
                continue
            elif c1 == ".":
                break
            elif c2 == "." and not c1 in ignore:
                break
            elif c1 in mapping.keys():
                if mapping[c1] == c2:
                    continue
                else:
                    break
            elif c2 in mapping.values():
                break
            else:
                mapping[c1] = c2
                continue
        else:
            return True
    return False




def _patternFromSequence(sequence):
    letterMapping = {}
    for c in sequence:
        if not c in letterMapping.keys() and sequence.count(c) > 1:
            letterMapping[c] = chr(65 + len(letterMapping))

    pattern = ""
    for c in sequence:
        pattern += letterMapping.get(c, ".")

    return pattern, letterMapping



def detectIsomorphs(messages, minIsomorphLength=5, maxIsomorphLength=50, maxDotRatio = 0.6):
    isomorphs = {} #keys: patterns, values: (message, position)

    for isomorphLength in range(minIsomorphLength, maxIsomorphLength+1):
        for h in range(len(messages)):
            print(isomorphLength, h)
            i = 0
            while i <= len(messages[h])-isomorphLength:
                
                sequence = messages[h][i : i + isomorphLength]
                
                pattern, mapping = _patternFromSequence(sequence)

                if pattern.find("A") > 0:
                    i += pattern.find("A")
                    continue

                i+=1

                if pattern.count(".") / len(pattern) > maxDotRatio:
                    continue

                if pattern[-1] == ".":
                    continue

                if len(mapping) <= 1:
                    continue

                if pattern in isomorphs.keys():
                    continue

                #get all occurences of pattern
                occurences = []
                for j in range(h, len(messages)):
                    for k in range(i-1 if j==h else 0, len(messages[h])-isomorphLength):
                        if _patternFromSequence(messages[j][k : k + isomorphLength])[0] == pattern:
                            occurences.append((j, k))

                if len(occurences) <= 1:
                    continue

                #remove isomorphs that are just a subset of the newly found one
                for iso in tuple(isomorphs.keys()):
                    if _containsPattern(pattern, iso) and len(isomorphs[iso]) == len(occurences):
                        isomorphs.pop(iso)

                isomorphs[pattern] = occurences
    return isomorphs


if __name__ == "__main__":

    messages = [[68, 62, 32, 20, 54, 23, 64, 59, 81, 32, 78, 73, 15, 76, 19, 68, 41, 38, 77, 60, 21, 44, 23, 26, 30, 79, 60, 27, 69, 2, 33, 77, 70, 46, 49, 49, 63, 7, 70, 3, 81, 5, 52, 17, 46, 1, 74, 82, 54, 81, 13, 15, 56, 65, 82, 21, 39, 49, 5, 67, 20, 4, 55, 62, 82, 69, 7, 50, 1, 71, 9, 18, 0, 49, 73, 51, 47, 14, 8, 61, 12, 76, 73, 82, 70, 59, 13, 38, 65, 16, 3, 40, 30, 78, 57, 20, 34, 32], [68, 59, 32, 20, 54, 23, 64, 59, 81, 32, 78, 73, 15, 76, 19, 68, 41, 38, 77, 60, 21, 44, 23, 26, 30, 76, 60, 24, 69, 20, 22, 41, 70, 73, 49, 49, 28, 7, 78, 3, 81, 5, 52, 17, 46, 1, 74, 82, 54, 81, 16, 79, 56, 79, 3, 58, 0, 47, 20, 52, 33, 28, 24, 24, 69, 59, 36, 27, 8, 50, 6, 24, 20, 55, 74, 76, 45, 71, 10, 72, 66, 0, 73, 26, 42, 30, 54, 46, 37, 47, 71, 3, 9, 28, 22, 56, 53, 32, 25, 54, 61, 30], [68, 79, 32, 20, 54, 23, 64, 59, 81, 32, 78, 73, 15, 76, 19, 68, 41, 38, 77, 60, 21, 44, 23, 26, 30, 75, 82, 32, 1, 77, 77, 47, 54, 68, 34, 49, 7, 49, 47, 40, 2, 56, 45, 20, 56, 35, 74, 64, 22, 81, 42, 38, 62, 7, 62, 69, 68, 24, 60, 34, 79, 3, 57, 69, 5, 2, 32, 64, 54, 72, 70, 75, 3, 22, 17, 61, 26, 35, 8, 14, 8, 28, 26, 77, 42, 46, 4, 72, 19, 29, 36, 52, 63, 49, 31, 55, 36, 61, 77, 58, 46, 75, 8, 39, 11, 36, 36, 59, 51, 78, 76, 35, 10, 17, 74, 81, 5], [69, 25, 82, 20, 50, 79, 41, 59, 12, 46, 59, 14, 15, 40, 18, 40, 7, 73, 59, 59, 31, 42, 57, 49, 33, 75, 80, 73, 57, 11, 63, 12, 72, 10, 76, 12, 22, 80, 72, 29, 73, 10, 12, 54, 35, 3, 3, 14, 32, 41, 58, 46, 18, 36, 24, 29, 35, 40, 3, 4, 72, 20, 55, 27, 8, 67, 10, 0, 31, 29, 54, 22, 36, 50, 33, 27, 10, 67, 73, 14, 6, 7, 14, 2, 2, 4, 47, 51, 75, 79, 75, 70, 41, 68, 75, 60, 57, 24, 42, 10, 57], [69, 30, 70, 20, 72, 70, 41, 41, 12, 70, 30, 0, 15, 47, 38, 9, 59, 48, 63, 58, 31, 31, 68, 67, 8, 44, 17, 70, 59, 58, 75, 79, 37, 38, 57, 20, 49, 60, 1, 71, 64, 75, 36, 9, 8, 64, 16, 24, 31, 29, 59, 62, 51, 56, 15, 81, 16, 55, 68, 81, 22, 38, 1, 29, 71, 45, 16, 4, 57, 59, 39, 39, 43, 70, 5, 34, 57, 18, 13, 46, 34, 13, 26, 25, 32, 39, 2, 49, 31, 6, 25, 46, 21, 37, 22, 61, 67, 34, 5, 26, 41, 45, 82, 24, 44, 61, 7, 48, 18, 7, 31, 81, 80, 19, 15, 7, 68, 69, 54, 75, 31, 54, 49, 20, 6, 59, 60, 6, 43, 2, 33, 7, 37, 44, 20, 73], [69, 7, 80, 20, 18, 43, 41, 15, 12, 67, 76, 25, 15, 40, 38, 50, 25, 37, 34, 17, 29, 74, 30, 55, 6, 73, 60, 28, 42, 53, 39, 39, 11, 4, 61, 34, 22, 3, 66, 47, 29, 42, 45, 44, 34, 15, 58, 5, 39, 12, 30, 36, 5, 51, 66, 30, 32, 68, 79, 57, 71, 38, 27, 46, 13, 78, 56, 73, 31, 5, 70, 73, 44, 35, 77, 21, 75, 12, 71, 52, 73, 11, 42, 23, 47, 61, 0, 73, 33, 0, 68, 68, 32, 24, 25, 35, 15, 2, 15, 13, 54, 23, 1, 59, 69, 43, 61, 34, 2, 82, 69, 48, 14, 73, 9, 9, 80, 41, 57, 34, 47, 43, 73], [69, 29, 70, 20, 72, 70, 41, 54, 12, 37, 30, 71, 15, 10, 29, 37, 56, 47, 6, 36, 31, 79, 65, 38, 30, 73, 6, 2, 14, 16, 56, 41, 27, 2, 48, 32, 50, 60, 26, 36, 42, 56, 82, 31, 63, 44, 78, 35, 78, 8, 47, 68, 60, 56, 12, 72, 75, 53, 20, 42, 9, 65, 72, 59, 48, 60, 4, 80, 70, 46, 26, 18, 37, 10, 0, 82, 38, 20, 80, 71, 73, 10, 37, 78, 76, 26, 4, 70, 61, 18, 72, 7, 44, 22, 31, 12, 26, 42, 38, 51, 70, 31, 19, 51, 69, 22, 36, 49, 46, 54, 2, 77, 65, 26, 28, 77, 67, 45], [69, 51, 70, 20, 72, 70, 41, 54, 12, 37, 30, 71, 15, 10, 29, 37, 56, 47, 6, 36, 31, 1, 57, 44, 30, 30, 5, 44, 16, 62, 20, 74, 48, 68, 49, 79, 7, 43, 7, 41, 5, 82, 82, 41, 66, 20, 52, 34, 76, 66, 33, 15, 20, 26, 47, 30, 14, 55, 14, 35, 36, 65, 72, 17, 28, 22, 77, 16, 47, 3, 56, 41, 25, 36, 73, 30, 73, 59, 30, 69, 4, 3, 75, 19, 31, 61, 11, 79, 32, 72, 53, 37, 27, 57, 69, 80, 54, 46, 80, 76, 58, 21, 26, 82, 57, 81, 4, 53, 67, 1, 15, 10, 49, 13, 0, 36, 1, 51, 7], [69, 33, 70, 20, 72, 70, 41, 54, 12, 37, 30, 71, 15, 10, 29, 37, 56, 47, 6, 36, 31, 27, 57, 5, 9, 73, 6, 2, 3, 16, 30, 41, 27, 82, 48, 24, 65, 60, 75, 36, 42, 53, 82, 53, 15, 38, 46, 49, 42, 46, 8, 53, 20, 23, 47, 23, 44, 65, 18, 47, 62, 55, 30, 17, 29, 30, 32, 32, 68, 38, 62, 53, 25, 50, 1, 44, 56, 34, 16, 72, 66, 36, 56, 27, 70, 3, 42, 0, 29, 24, 24, 41, 27, 48, 39, 63, 77, 11, 77, 30, 22, 23, 29, 25, 10, 23, 7, 37, 21, 53, 58, 0, 38]]



    isos = detectIsomorphs(messages, maxIsomorphLength = 50, maxDotRatio = 0.8)

    isoSeqs = {}

    for iso in isos:
        print(len(iso))
        s = []
        for m, pos in isos[iso]:
            n = messages[m][pos : pos+len(iso)]
            if not n in s:
                s.append((m,pos,n))
        isoSeqs[iso] = s

    print(isoSeqs)

    import json
    with open("isomorphs.json","w") as f:
        json.dump(isoSeqs, f)

    
    

##patts = list(isoSeqs.keys())
##patts.sort(reverse = True, key = lambda p: len(isoSeqs[p]) + (1-p.count(".")/len(p)))
##
##for iso in isoSeqs:
##    print(iso)
##    for s in isoSeqs[iso]:
##        print(s)
##    dubs = set()
##    for s in isoSeqs[iso]:
##        for c in s:
##            n = 0
##            for s in isoSeqs[iso]:
##                if c in s:
##                    n += 1
##            if n>1:
##                dubs.add(c)
##    print(dubs)
##    print()
                
                        







                    
                
