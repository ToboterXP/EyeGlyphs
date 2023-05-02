
from collections import namedtuple
from itertools import permutations
import copy
import random

DisplayMode_WheelSection = 0
DisplayMode_EyeDecode = 1

DISPLAY_MODE = DisplayMode_WheelSection


class WheelException(Exception):
    pass


eyeMessages = ((50, 66, 5, 48, 62, 13, 75, 29, 24, 61, 42, 70, 66, 62, 32, 14, 81, 8,  15, 78, 2,  29, 13, 49, 1,  80, 82, 40, 63, 81, 21, 19, 0, 40, 51, 65, 26, 14, 21, 70, 47, 44, 48, 42, 19, 48, 13, 47, 19, 49, 72, 31, 5, 24, 3, 43, 59, 67, 33, 49, 41, 60, 21, 26, 30, 5, 25, 20, 71, 11, 74, 56, 4, 74, 19, 71, 4, 51, 41, 43, 80, 72, 54, 63, 79, 81, 15, 16, 44, 31, 30, 12, 33, 57, 28, 13, 64, 43, 48),
            (80, 66, 5, 48, 62, 13, 75, 29, 24, 61, 42, 70, 66, 62, 32, 14, 81, 8,  15, 78, 2,  29, 13, 49, 1,  29, 11, 30, 52, 81, 21, 19, 0, 25, 26, 54, 20, 14, 21, 70, 47, 44, 48, 42, 19, 48, 13, 47, 19, 49, 44, 26, 59, 77, 64, 43, 79, 28, 72, 64, 1, 30, 73, 23, 67, 6, 33, 25, 64, 81, 68, 46, 17, 36, 13, 17, 21, 68, 13, 9, 46, 67, 57, 34, 62, 82, 15, 10, 73, 62, 2, 11, 65, 72, 37, 44, 10, 43, 68, 62, 9, 34, 18),
            (36, 66, 5, 48, 62, 13, 75, 29, 24, 61, 42, 70, 66, 62, 32, 14, 81, 8,  15, 78, 2,  29, 13, 49, 1,  69, 76, 52, 9,  48, 66, 80, 22, 64, 57, 40, 49, 78, 3, 16, 56, 19, 47, 40, 80, 6, 13, 64, 29, 49, 64, 63, 6, 49, 31, 13, 16, 10, 45, 24, 26, 77, 10, 60, 81, 61, 34, 54, 70, 21, 15, 4, 66, 77, 42, 37, 30, 22, 0, 11, 41, 72, 57, 20, 23, 57, 65, 41, 23, 18, 72, 42, 5, 3, 26, 78, 8, 5, 54, 45, 77, 25, 64, 61, 16, 44, 54, 51, 20, 63, 25, 11, 26, 45, 53, 60, 38, 34),
            (76, 66, 5, 49, 75, 54, 69, 46, 32, 1,  42, 60, 26, 48, 50, 80, 32, 24, 55, 61, 47, 12, 21, 12, 49, 54, 34, 25, 36, 15, 56, 55, 20, 9, 8, 62, 13, 82, 9, 44, 29, 60, 53, 82, 42, 80, 5, 43, 71, 3, 80, 77, 47, 78, 34, 25, 62, 18, 10, 49, 62, 64, 52, 81, 11, 66, 62, 13, 47, 17, 52, 70, 26, 23, 32, 31, 64, 23, 35, 32, 50, 6, 1, 25, 8, 37, 47, 43, 26, 76, 65, 68, 80, 17, 7, 45, 63, 14, 53, 63, 60, 16),
            (63, 66, 5, 49, 75, 54, 2,  60, 29, 40, 78, 47, 60, 75, 67, 71, 60, 2,  65, 7,  47, 14, 45, 74, 59, 41, 80, 13, 60, 13, 81, 22, 35, 50, 40, 39, 2, 59, 48, 31, 76, 2, 80, 75, 1, 56, 67, 11, 21, 8, 40, 65, 45, 75, 55, 39, 60, 42, 13, 3, 22, 57, 2, 6, 58, 9, 70, 1, 58, 56, 63, 68, 25, 79, 7, 20, 19, 64, 2, 66, 73, 30, 71, 16, 12, 30, 65, 37, 20, 13, 22, 63, 18, 46, 64, 59, 41, 81, 82, 22, 78, 36, 47, 17, 4, 6, 17, 5, 36, 79, 63, 1, 64, 69, 15, 43, 4, 58, 56, 31, 14, 64, 58, 18, 44, 78, 69, 1, 0, 46, 20, 71, 73, 25, 35, 8, 24),
            (34, 66, 5, 49, 75, 54, 23, 74, 11, 13, 28, 26, 19, 48, 67, 57, 37, 60, 34, 28, 74, 10, 17, 32, 11, 18, 19, 43, 19, 81, 42, 4, 62, 9, 46, 49, 32, 51, 76, 58, 4, 43, 47, 17, 67, 79, 21, 32, 44, 16, 30, 37, 26, 28, 41, 68, 57, 34, 51, 10, 69, 70, 8, 6, 46, 43, 18, 39, 47, 43, 15, 13, 33, 30, 35, 62, 37, 0, 37, 5, 38, 55, 37, 13, 40, 25, 9, 21, 11, 64, 5, 79, 42, 68, 11, 71, 11, 48, 3, 67, 61, 40, 22, 14, 35, 50, 61, 39, 11, 2, 66, 49, 51, 53, 17, 73, 36, 75, 74, 54, 24, 30, 54, 70),
            (27, 66, 5, 49, 75, 54, 2,  60, 29, 40, 2,  55, 9,  15, 59, 18, 68, 3,  36, 5,  47, 77, 44, 38, 1,  18, 28, 76, 4,  34, 60, 63, 58, 80, 17, 54, 79, 75, 48, 54, 55, 19, 62, 64, 14, 47, 51, 70, 75, 5, 11, 47, 45, 58, 68, 69, 79, 25, 38, 45, 73, 47, 68, 50, 34, 45, 78, 26, 79, 57, 4, 56, 22, 60, 18, 75, 43, 60, 59, 67, 63, 42, 49, 33, 40, 65, 79, 77, 7, 3, 26, 62, 31, 78, 26, 57, 69, 40, 4, 23, 26, 13, 67, 42, 38, 72, 11, 39, 65, 60, 25, 6, 80, 66, 68, 77, 59, 78, 19),
            (77, 66, 5, 49, 75, 54, 2,  60, 29, 40, 2,  55, 9,  15, 59, 18, 68, 3,  36, 5,  47, 60, 21, 80, 1,  72, 55, 16, 82, 35, 57, 19, 1, 66, 18, 27, 39, 17, 74, 81, 39, 14, 78, 0, 25, 65, 43, 66, 64, 38, 81, 23, 24, 50, 57, 30, 71, 75, 26, 68, 54, 57, 56, 50, 71, 73, 14, 21, 8, 32, 26, 63, 5, 37, 19, 43, 66, 47, 53, 34, 66, 23, 73, 31, 54, 38, 77, 67, 11, 63, 79, 6, 22, 21, 51, 69, 74, 21, 5, 17, 67, 37, 29, 21, 60, 14, 82, 44, 30, 4, 20, 42, 35, 1, 31, 54, 46, 20, 40, 30),
            (33, 66, 5, 49, 75, 54, 2,  60, 29, 40, 2,  55, 9,  15, 59, 18, 68, 3,  36, 5,  47, 33, 21, 59, 44, 18, 28, 76, 59, 34, 60, 63, 79, 27, 12, 54, 5, 49, 48, 54, 55, 52, 62, 72, 69, 10, 57, 22, 58, 48, 67, 53, 7, 34, 32, 30, 31, 19, 26, 8, 34, 46, 7, 30, 71, 55, 34, 75, 54, 9, 6, 60, 5, 23, 25, 45, 42, 80, 25, 12, 22, 76, 20, 51, 62, 21, 40, 9, 41, 10, 44, 73, 8, 33, 70, 73, 6, 31, 21, 72, 5, 40, 61, 51, 42, 66, 64, 74, 61, 25, 63, 42, 24, 41))


Message = namedtuple("Message",["plaintext","trigrams","offset"])

#assumed shared message sections
messages = (
    Message("&ABCDEFGHI","fOLPJ3P-O3",39), #m1
    Message("JKLMNOPQR","53sHSa:.5",30),
    Message("&ABCDEFGHI","4g+jX$j3g$",67),
    
    Message("&ABCDEFGHI","qdN1D-15d-",69), #m2
    Message("JKLMNOPQR","53s9:V4.5",30),
    Message("STUVWX","`Ko<h`",54),
    Message("STUVWX","^r/*i^",84),
    
    Message("&ABCDEFGHI","p&-`=Q`_&Q",44), #m3
    Message("&ABCDEFGHI","+IhY47YaI7",79),
    Message("JKLMNOPQR","HQn#0X3OH",35),
    Message("STUVWX","*M8:m*",57),
    Message("STUVWX","%#:n(%",92),
    
    
    Message("abcdefghijkl","OMZdeo9FMiOd",51), #m7
    Message("mnopqrstuvwxyz0123456789","\\2kK\\[c_JQAHaom'#:^?n:YeH",83),
    Message("+%*/#!$.","VokPVW3^",35),
    
    Message("abcdefghijkl","RY>gk:dVYXRg",53), #m8
    Message("mnopqrstuvwxyz0123456789","bOUBb7i?VFmc+_o&65Sej5%1c",86),
    Message("+%*/#!$.","G1jqG.n ",36),
    
    Message("abcdefghijkl","'B@>?3:(BN'>",52), #m9
    Message("mnopqrstuvwxyz0123456789","9MJp9,6l4S^5H)I*Li(Afi&?5",84),
    Message("+%*/#!$.","V%QPVWT^",35),
    )


class WheelSection:
    def __init__(self,trigram,charOffsets=[],trigramOffsets=[],charsByOffset={},trigramsByOffset={}):
        
        self.trigram = trigram
        self.charOffsets = list(charOffsets)
        self.charsByOffset = charsByOffset.copy()
        
        self.trigramOffsets = list(trigramOffsets)
        self.trigramsByOffset = trigramsByOffset.copy()

    def addCharOffset(self,charOffset):
        global addEquivalence
        o = self.charsByOffset.get(charOffset.offset)
        if o:
            if o.character != charOffset.character:
                addEquivalence(o.character, charOffset.character)
            return
        else:
            self.charOffsets.append( charOffset)
            self.charsByOffset[charOffset.offset] = charOffset

    def addTrigramOffset(self,trigramOffset):
        
        if trigramOffset.offset == 0:
            if trigramOffset.trigram == self.trigram:
                return
            else:
                raise WheelException(f"Trigram Collision between {self.trigram} and {trigramOffset.trigram}")

        tri = self.trigramsByOffset.get(trigramOffset.offset)
        if tri:
            if tri.trigram == trigramOffset.trigram:
                return
            else:
                raise WheelException(f"Trigram Collision between {tri.trigram} and {trigramOffset.trigram}")

        self.trigramOffsets.append(trigramOffset)
        self.trigramsByOffset[trigramOffset.offset] = trigramOffset

    def addWheelSection(self, other):
        "Try to merge the offsets of a different wheel section. return true on success, otherwise false"
        #find a matching offset between characters, and match accordingly
        sharedCharacterOffsets = []
        for co in self.charOffsets:
            for co2 in other.charOffsets:
                if co.character == co2.character:
                    sharedCharacterOffsets.append((co,co2))

        if len(sharedCharacterOffsets) == 0:
            return False

        
        offset = None #try to find offset

        if len(sharedCharacterOffsets) >= 2:
            #try to find offset based on distance between shared characters
            proposedOffsets = list()
            for a,b in permutations(sharedCharacterOffsets, 2):
                diffSelf = a[0].offset-b[0].offset
                diffOther = a[1].offset-b[1].offset
                if diffSelf == diffOther:
                    proposedOffsets.append(a[0].offset - a[1].offset)

            proposedOffsetSet = tuple(set(proposedOffsets))

            if len(proposedOffsetSet) > 0:  
                
                counts = {}
                for o in proposedOffsetSet:
                    counts[o] = proposedOffsets.count(o)

                if tuple(counts.values()).count(max(counts.values())) == 1: #if two propsed offsets are equally likely, don't merge

                    allCounts = list(counts.values())
                    allCounts.sort(reverse=True)

                    offset = None
                    for o in counts.keys():
                        if counts[o] == max(counts.values()):
                            offset = o

        if offset == None:
            #if shared character matching wasn't successful, try shared character offset matching
            offsetScores = {}
            for a, b in sharedCharacterOffsets:
                offsetsSelf = set()
                
                for o in self.charOffsets:
                    if o!=a:
                        offsetsSelf.add(o.offset - a.offset)

                offsetsOther = set()
                for o in other.charOffsets:
                    if o!=b:
                        offsetsOther.add(o.offset - b.offset)

                score = offsetScores.setdefault(a.offset - b.offset,0)

                for o in offsetsSelf:
                    if o in offsetsOther:
                        score += 1

                offsetScores[a.offset - b.offset] = score

            offsSorted = list(offsetScores.values())
            offsSorted.sort(reverse = True)

            if offsSorted.count(offsSorted[0]) == 1 and offsSorted[0]>=4: #no two offsets equally likely and there is enough evidence
                for o in offsetScores.keys():
                    if offsetScores[o] == offsSorted[0]:
                        offset = o
                        break

        if offset == None: #if still no offset found, return
            return False
                       
        self.mergeWheelSection(other, offset)
        
        return True

    def mergeWheelSection(self, other, offset):
        self.addTrigramOffset(TrigramOffset(other.trigram, offset))

        for tri in other.trigramOffsets:
            self.addTrigramOffset(TrigramOffset(tri.trigram, tri.offset+offset))

        
        for char in other.charOffsets:
            self.addCharOffset(CharOffset(char.character, char.offset + offset))

    def checkForTrigramCollisions(self, other, offset): #return True if there is a trigram collision
        for trigramOffset in other.trigramOffsets+[TrigramOffset(other.trigram, 0)]:
            otherTri = trigramOffset.trigram
            otherOff = (trigramOffset.offset + offset)%83
            if otherOff == 0:
                if otherTri != self.trigram:
                    return True
            
            tri = self.trigramsByOffset.get(otherOff)
            if tri:
                if tri.offset == otherOff:
                    if tri.trigram != otherTri:
                        return True

        return False

    def getCharOffsets(self,char):
        return list(filter(lambda c: c.character == char, self.charOffsets))

    def copy(self):
        return WheelSection(self.trigram, list(map(lambda a: a.copy(), self.charOffsets)), list(map(lambda a: a.copy(), self.trigramOffsets)), self.charsByOffset, self.trigramsByOffset)
                
class CharOffset:
    def __init__(self, character, offset):#offset = how far before that trigram
        global getEquivalent
        self.character = getEquivalent(character)
        self.offset = offset % 83

    def __str__(self):
        return f"chr {self.character} {self.offset}"

    def copy(self):
        return CharOffset(self.character, self.offset)

class TrigramOffset:
    def __init__(self, trigram, offset):#offset = how far before that trigram
        self.trigram = trigram
        self.offset = offset % 83

    def __str__(self):
        return f"tri {self.trigram} {self.offset}"

    def copy(self):
        return TrigramOffset(self.trigram, self.offset)



sections = []   #the found wheel sections

equivalences = {}   #the found character equivalences


UPDATE_SECTIONS_ON_EQUIVALENCE = True

#a is the old character, b the new one
def addEquivalence(a,b):
    
    equivalences[b] = a

    #update all the character offsets inside sections
    if UPDATE_SECTIONS_ON_EQUIVALENCE:
        for s in sections:
            for o in s.charOffsets:
                if o.character == b:
                    o.character = a

def getEquivalent(a):
    return equivalences.get(a,a)
    
            

#step one: extract character to trigram offsets
for m in messages:
    for i in range(len(m.plaintext)):
        offset = (i + m.offset)%83
        trigram = m.trigrams[i]
        character = getEquivalent(m.plaintext[i])

        for e in equivalences:
            if character in e:
                character = e[0]
                break
        
        section = None  #grab the section of that trigram
        
        for s in sections:
            if s.trigram == trigram:
                section = s
                break
        else:
            section = WheelSection(trigram,[])
            sections.append(section)

        #detect repeats/equivalences
        section.addCharOffset(CharOffset(character,offset))



print("Starting two character based matching")
#try to merge as many sections as possible

notCurrent = sections[:]    #have never been current

rerty = False

current = notCurrent.pop()
currentChanged = False

while notCurrent:
    print(f"Remaining sections: {len(notCurrent)}, available sections {len(sections)}")
    
    for sect in sections[:]:
        if sect == current:
            continue
        #print(sect.trigram,end="")
        if current.addWheelSection(sect):
            currentChanged = True
            retry = True
            sections.remove(sect)
            if sect in notCurrent:
                notCurrent.remove(sect)
    #print()

    if not currentChanged:
        current = notCurrent.pop()
    currentChanged = False

##    if not notCurrent and retry:
##        retry = False
##        notCurrent = sections[:]


#do an aggressive match on collision free characters

print("Starting single character based matching")
alphabet = set()

for m in messages:
    for c in m.plaintext:
        alphabet.add(getEquivalent(c))

alphabet = list(alphabet)
alphabet.sort()

sections.sort(reverse = True, key=lambda a: len(a.charOffsets)+len(a.trigramOffsets))

def mergeCollisionless(merges,allSections):
    global equivalences, UPDATE_SECTIONS_ON_EQUIVALENCE

    UPDATE_SECTIONS_ON_EQUIVALENCE = False
    mergeStack = [(merges,set(allSections),0,copy.deepcopy(equivalences))]

    maxColl = 0
    while mergeStack:
        merges, allSections, hasSkipped, iEquivalences = mergeStack[-1]
        sect1, sect2, offset = merges[0]

        equivalences = iEquivalences #janky programming to get around the problem with equivalences being global
        
        if hasSkipped == 0:
            if not merges:
                UPDATE_SECTIONS_ON_EQUIVALENCE = True
                return allSections
            
            if not sect1 in allSections or not sect2 in allSections:
                mergeStack.append((merges[1:], allSections,0,copy.deepcopy(equivalences)))
                continue

            mergedSection = sect1.copy()
            try:
                mergedSection.mergeWheelSection(sect2, offset)
            except WheelException:
                if maxColl<len(mergeStack):
                    maxColl = len(mergeStack)
                    print("Collision at depth",len(mergeStack),"of",len(mergeStack)+len(merges),f"({len(allSections)} remaining)")
                mergeStack.pop()
                continue

            newMerges = []
            for m in merges[1:]:
                if m[0] in allSections and m[1] in allSections:
                    if m[0] == sect1:
                        newMerges.append((mergedSection, m[1], m[2]))
                    elif m[1] == sect1:
                        newMerges.append((m[0], mergedSection, m[2]))
                    else:
                        newMerges.append(m[:])

            newAllSections = allSections.copy()
            newAllSections.remove(sect2)
            newAllSections.remove(sect1)
            newAllSections.add(mergedSection)


            mergeStack[-1] = (merges, allSections, 1, equivalences)
            mergeStack.append((newMerges, newAllSections, 0,copy.deepcopy(equivalences)))
            
        elif hasSkipped == 1:
            mergeStack[-1] = (merges, allSections, 2, equivalences)
            mergeStack.append((merges[1:], allSections, 0,copy.deepcopy(equivalences)))

        elif hasSkipped == 2:
            mergeStack.pop()
            #if mergeStack[-1][2]!=2:
                #print("Turnaround at depth",len(mergeStack))
    
    print("Matching impossible")
    UPDATE_SECTIONS_ON_EQUIVALENCE = True
    return []


changes = True
while changes:
    changes = False
    all_possible_merges = []

    for sect1, sect2 in permutations(sections,2):
        possibleMerges = []
        for char in alphabet:
            sect1chars = sect1.getCharOffsets(char)
            sect2chars = sect2.getCharOffsets(char)

            if not sect1chars or not sect2chars:
                continue
            
            for sect1char in sect1chars:
                for sect2char in sect2chars:
            
                    if sect1.checkForTrigramCollisions(sect2, sect1char.offset - sect2char.offset):
                        continue

                    noSuccess = False

                    if not sect1char.offset-sect2char.offset in possibleMerges:
                        possibleMerges.append(sect1char.offset-sect2char.offset)

        if len(possibleMerges)==1:
            merge = possibleMerges[0]
            all_possible_merges.append((sect1,sect2,merge))

    print(f"Merge count: {len(all_possible_merges)}")

    all_possible_merges.sort(reverse=False, key=lambda a: len(a[0].trigramOffsets)+len(a[1].trigramOffsets))
    start_len = len(sections)
    sections = mergeCollisionless(all_possible_merges, sections)
    print(f"Sections remaining: {len(sections)}")
    if start_len > len(sections):
        changed = True


##            if not (sect1,sect1char) in charInSections[char]:
##                charInSections[sect1char.character].append((sect1,sect1char))
##
##            if not (sect2,sect2char) in charInSections[char]:
##                charInSections[sect1char.character].append((sect2,sect2char))         
##
##
##    #merge based on the actual 
##    used = []
##    for char in alphabet:
##        char = getEquivalent(char)
##        if char in used:
##            continue
##        used.append(char)
##        sects = list(filter(lambda a: a[0] in sections, charInSections[char]))
##        if sects:
##            mainSect = sects[0][0]
##            mainSectCharOff = sects[0][1]
##            for sect, sectOff in sects[1:]:
##                if sect in sections and not sect is mainSect:
##                    offset = mainSectCharOff.offset - sectOff.offset
##                    if not mainSect.checkForTrigramCollisions(sect, offset):
##                        mainSect.mergeWheelSection(sect, offset)
##                        changes = True
##                        sections.remove(sect)
##            print(f"Sections remaining: {len(sections)}")
    

print("Starting trigram pattern based matching")

possibleMerges = []
for sect1, sect2 in permutations(sections,2):
    possibleOffsets = []
    for offset in range(83):
        if not sect1.checkForTrigramCollisions(sect2, offset):
            possibleOffsets.append(offset)

    if len(possibleOffsets) == 1:
        possibleMerges.append((sect1, sect2, possibleOffsets[0]))

    if len(possibleOffsets) == 0:
        print("Error - irreconcilable sections")

for sect1, sect2, offset in possibleMerges:
    if sect1 in sections and sect2 and sections:
        sect1.mergeWheelSection(sect2, offset)
        sections.remove(sect2)
        print(f"Sections remaining: {len(sections)}")
        


#display the results
#if DISPLAY_MODE == DisplayMode_WheelSection:
        
print("Equivalent values:",equivalences)

alphabet = set()

for m in messages:
    for c in m.plaintext:
        alphabet.add(getEquivalent(c))

print("Alphabet:",len(alphabet))

sections.sort(key = lambda a: len(a.charOffsets)+len(a.trigramOffsets), reverse =True)

print("Wheel Sections (character or trigram, value, offset):")
print()
for sect in sections:
    offs = sect.charOffsets+sect.trigramOffsets
    offs.sort(key=lambda a:a.offset,reverse = True)
    for off in offs:
        print(str(off))
    print("tri",sect.trigram,0)
    print()

#elif DISPLAY_MODE == DisplayMode_EyeDecode:
print()
print()
for m in eyeMessages:
    for i in range(len(m)):
        tri = chr(m[i]+32)
        char = None
        for sect in sections:
            off = None
            if sect.trigram == tri:
                off = 0
            else:
                for triOff in sect.trigramOffsets:
                    if triOff.trigram == tri:
                        off = triOff.offset

            if off != None:
                off = (off+i)%83
                for charOff in sect.charOffsets:
                    if charOff.offset == off:
                        char = charOff.character
                        break
            if char:
                break
        if char:
            print(char,end="")
        else:
            print("-",end="")
    print()
                        
            

    


##print(equivalences)
##for s in sections:
##    print(s.trigram,":")
##    for co in s.charOffsets:
##        print(co.character, co.offset)
            

##alphabet = list(alphabet)
##alphabet.sort()
##
##for a,b in permutations(alphabet,2):
##    distancesD = set()
##    distances = []
##    for s in sections:
##        aOffsets = []
##        for co in s.charOffsets:
##            if co.character == a:
##                aOffsets.append(co.offset)
##        for co in s.charOffsets:
##            if co.character == b:
##                for i in aOffsets:
##                    distancesD.add(i-co.offset)
##                    distances.append(i-co.offset)
##    distancesD = list(distancesD)
##    distancesD.sort()
##    if distancesD:
##        print(len(distances),len(distancesD),distances,distancesD,a,b)




            
    

                    
        
