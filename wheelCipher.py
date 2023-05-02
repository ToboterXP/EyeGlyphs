
import random

messages = [
    "Bread is one of the oldest prepared foods. Evidence from thirty-thousand years ago in Europe and Australia revealed starch residue on rocks used for pounding plants.",
    "It is possible that during this time, starch extract from the roots of plants, such as cattails and ferns, was spread on a flat rock, placed over a fire and cooked into a primitive form of flatbread.",
    "The world's oldest evidence of bread-making has been found in a fourteen-thousand-year-old Natufian site in Jordan's northeastern desert.",
    "Around then, with the dawn of the Neolithic age and the spread of agriculture, grains became the mainstay of making bread.",
    "Yeast spores are ubiquitous, including on the surface of cereal grains, so any dough left to rest leavens naturally.",
    "An early leavened bread was baked as early as six thousand BC by the Sumerians, who may have passed on their knowledge to the Egyptians around three thousand BC. The Egyptians refined the process and started adding yeast to the flour.",
    "There were multiple sources of leavening available for early bread. Airborne yeasts could be harnessed by leaving uncooked dough exposed to air for some time before cooking.",
    "Pliny the Elder reported that the Gauls and Iberians used the foam skimmed from beer, called barm, to produce a lighter kind of bread than other peoples such as barm cake. Parts of the ancient world that drank wine instead of beer used a paste composed of grape juice and flour that was allowed to begin fermenting, or wheat bran steeped in wine, as a source for yeast",
    "Bread is the staple food of the Middle East, Central Asia, North Africa, Europe, and in European-derived cultures such as those in the Americas, Australia, and Southern Africa. This is in contrast to parts of South and East Asia, where rice or noodles are the staple."
    ]

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

outerWheel = list(range(83))
innerWheel = list(alphabet)*3+list("   ,.")
assert len(innerWheel)==83

random.shuffle(outerWheel)
random.shuffle(innerWheel)

cipherMessages = []
for m in messages:
    m = m.upper()
    cm = []
    off = 0
    for c in m:
        if c in innerWheel:
            ai = []
            for i in range(len(innerWheel)):
                if innerWheel[i]==c:
                    ai.append(i)
            cm.append( outerWheel[ (random.choice(ai)+off) % 83])
            #off += random.randint(1,40)
            off += 3
    cipherMessages.append(cm)

print(outerWheel,innerWheel)
print()


##cipherMessages = ((50, 66, 5, 48, 62, 13, 75, 29, 24, 61, 42, 70, 66, 62, 32, 14, 81, 8,  15, 78, 2,  29, 13, 49, 1,  80, 82, 40, 63, 81, 21, 19, 0, 40, 51, 65, 26, 14, 21, 70, 47, 44, 48, 42, 19, 48, 13, 47, 19, 49, 72, 31, 5, 24, 3, 43, 59, 67, 33, 49, 41, 60, 21, 26, 30, 5, 25, 20, 71, 11, 74, 56, 4, 74, 19, 71, 4, 51, 41, 43, 80, 72, 54, 63, 79, 81, 15, 16, 44, 31, 30, 12, 33, 57, 28, 13, 64, 43, 48),
##            (80, 66, 5, 48, 62, 13, 75, 29, 24, 61, 42, 70, 66, 62, 32, 14, 81, 8,  15, 78, 2,  29, 13, 49, 1,  29, 11, 30, 52, 81, 21, 19, 0, 25, 26, 54, 20, 14, 21, 70, 47, 44, 48, 42, 19, 48, 13, 47, 19, 49, 44, 26, 59, 77, 64, 43, 79, 28, 72, 64, 1, 30, 73, 23, 67, 6, 33, 25, 64, 81, 68, 46, 17, 36, 13, 17, 21, 68, 13, 9, 46, 67, 57, 34, 62, 82, 15, 10, 73, 62, 2, 11, 65, 72, 37, 44, 10, 43, 68, 62, 9, 34, 18),
##            (36, 66, 5, 48, 62, 13, 75, 29, 24, 61, 42, 70, 66, 62, 32, 14, 81, 8,  15, 78, 2,  29, 13, 49, 1,  69, 76, 52, 9,  48, 66, 80, 22, 64, 57, 40, 49, 78, 3, 16, 56, 19, 47, 40, 80, 6, 13, 64, 29, 49, 64, 63, 6, 49, 31, 13, 16, 10, 45, 24, 26, 77, 10, 60, 81, 61, 34, 54, 70, 21, 15, 4, 66, 77, 42, 37, 30, 22, 0, 11, 41, 72, 57, 20, 23, 57, 65, 41, 23, 18, 72, 42, 5, 3, 26, 78, 8, 5, 54, 45, 77, 25, 64, 61, 16, 44, 54, 51, 20, 63, 25, 11, 26, 45, 53, 60, 38, 34),
##            (76, 66, 5, 49, 75, 54, 69, 46, 32, 1,  42, 60, 26, 48, 50, 80, 32, 24, 55, 61, 47, 12, 21, 12, 49, 54, 34, 25, 36, 15, 56, 55, 20, 9, 8, 62, 13, 82, 9, 44, 29, 60, 53, 82, 42, 80, 5, 43, 71, 3, 80, 77, 47, 78, 34, 25, 62, 18, 10, 49, 62, 64, 52, 81, 11, 66, 62, 13, 47, 17, 52, 70, 26, 23, 32, 31, 64, 23, 35, 32, 50, 6, 1, 25, 8, 37, 47, 43, 26, 76, 65, 68, 80, 17, 7, 45, 63, 14, 53, 63, 60, 16),
##            (63, 66, 5, 49, 75, 54, 2,  60, 29, 40, 78, 47, 60, 75, 67, 71, 60, 2,  65, 7,  47, 14, 45, 74, 59, 41, 80, 13, 60, 13, 81, 22, 35, 50, 40, 39, 2, 59, 48, 31, 76, 2, 80, 75, 1, 56, 67, 11, 21, 8, 40, 65, 45, 75, 55, 39, 60, 42, 13, 3, 22, 57, 2, 6, 58, 9, 70, 1, 58, 56, 63, 68, 25, 79, 7, 20, 19, 64, 2, 66, 73, 30, 71, 16, 12, 30, 65, 37, 20, 13, 22, 63, 18, 46, 64, 59, 41, 81, 82, 22, 78, 36, 47, 17, 4, 6, 17, 5, 36, 79, 63, 1, 64, 69, 15, 43, 4, 58, 56, 31, 14, 64, 58, 18, 44, 78, 69, 1, 0, 46, 20, 71, 73, 25, 35, 8, 24),
##            (34, 66, 5, 49, 75, 54, 23, 74, 11, 13, 28, 26, 19, 48, 67, 57, 37, 60, 34, 28, 74, 10, 17, 32, 11, 18, 19, 43, 19, 81, 42, 4, 62, 9, 46, 49, 32, 51, 76, 58, 4, 43, 47, 17, 67, 79, 21, 32, 44, 16, 30, 37, 26, 28, 41, 68, 57, 34, 51, 10, 69, 70, 8, 6, 46, 43, 18, 39, 47, 43, 15, 13, 33, 30, 35, 62, 37, 0, 37, 5, 38, 55, 37, 13, 40, 25, 9, 21, 11, 64, 5, 79, 42, 68, 11, 71, 11, 48, 3, 67, 61, 40, 22, 14, 35, 50, 61, 39, 11, 2, 66, 49, 51, 53, 17, 73, 36, 75, 74, 54, 24, 30, 54, 70),
##            (27, 66, 5, 49, 75, 54, 2,  60, 29, 40, 2,  55, 9,  15, 59, 18, 68, 3,  36, 5,  47, 77, 44, 38, 1,  18, 28, 76, 4,  34, 60, 63, 58, 80, 17, 54, 79, 75, 48, 54, 55, 19, 62, 64, 14, 47, 51, 70, 75, 5, 11, 47, 45, 58, 68, 69, 79, 25, 38, 45, 73, 47, 68, 50, 34, 45, 78, 26, 79, 57, 4, 56, 22, 60, 18, 75, 43, 60, 59, 67, 63, 42, 49, 33, 40, 65, 79, 77, 7, 3, 26, 62, 31, 78, 26, 57, 69, 40, 4, 23, 26, 13, 67, 42, 38, 72, 11, 39, 65, 60, 25, 6, 80, 66, 68, 77, 59, 78, 19),
##            (77, 66, 5, 49, 75, 54, 2,  60, 29, 40, 2,  55, 9,  15, 59, 18, 68, 3,  36, 5,  47, 60, 21, 80, 1,  72, 55, 16, 82, 35, 57, 19, 1, 66, 18, 27, 39, 17, 74, 81, 39, 14, 78, 0, 25, 65, 43, 66, 64, 38, 81, 23, 24, 50, 57, 30, 71, 75, 26, 68, 54, 57, 56, 50, 71, 73, 14, 21, 8, 32, 26, 63, 5, 37, 19, 43, 66, 47, 53, 34, 66, 23, 73, 31, 54, 38, 77, 67, 11, 63, 79, 6, 22, 21, 51, 69, 74, 21, 5, 17, 67, 37, 29, 21, 60, 14, 82, 44, 30, 4, 20, 42, 35, 1, 31, 54, 46, 20, 40, 30),
##            (33, 66, 5, 49, 75, 54, 2,  60, 29, 40, 2,  55, 9,  15, 59, 18, 68, 3,  36, 5,  47, 33, 21, 59, 44, 18, 28, 76, 59, 34, 60, 63, 79, 27, 12, 54, 5, 49, 48, 54, 55, 52, 62, 72, 69, 10, 57, 22, 58, 48, 67, 53, 7, 34, 32, 30, 31, 19, 26, 8, 34, 46, 7, 30, 71, 55, 34, 75, 54, 9, 6, 60, 5, 23, 25, 45, 42, 80, 25, 12, 22, 76, 20, 51, 62, 21, 40, 9, 41, 10, 44, 73, 8, 33, 70, 73, 6, 31, 21, 72, 5, 40, 61, 51, 42, 66, 64, 74, 61, 25, 63, 42, 24, 41))

print(cipherMessages)


s = ""

    

for message in cipherMessages:
    offset = 0
    for tri in message:
        i = outerWheel.index(tri)
        char = innerWheel[(i-offset)%83]
        offset += 3
        s += char
    s+="\n"

print(s)
           
    
