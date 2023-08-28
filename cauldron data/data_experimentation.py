from Crypto.Cipher import AES
from Crypto.Util import Counter
from itertools import permutations

import base64

data = [0x12, 0x3b, 0x92, 0xe2, 0x41, 0xf0, 0xe2, 0x1f, 0xef, 0xf1, 0x03, 0x3e, 0x16, 0xa6, 0x46, 0x3b, 0xdc, 0x00, 0xdd, 0xce, 0xd0, 0xb0, 0x56, 0x1e, 0x98, 0x29, 0xfa, 0x95, 0x13, 0x55, 0x25, 0x9c, 0x45, 0x2e, 0x47, 0xbd, 0x8f, 0x22, 0x98, 0xfc, 0x41, 0x74, 0x68, 0xfc, 0x65, 0x32, 0x36, 0x7b, 0xaf, 0xbc, 0xc7, 0xec, 0x60, 0x14, 0x63, 0xd3, 0xda, 0x20, 0xe3, 0xbf, 0xc4, 0x98, 0xf5, 0x32]

encoded = b""
for i in data:
    encoded += i.to_bytes(1,"big")

usedKeyIVPairs = (
    ("WhenYouHaveNothingLeftToSeek", "PeopleWillRejoiceAndDance"),
    ("WeSeeATrueSeekerOfKnowledge", "YouAreSoCloseToBeingEnlightened"),
    ("TheTruthIsThatThereIsNothing", "MoreValuableThanKnowledge"),
    ("KnowledgeIsTheHighestOfTheHighest", "WhoWouldntGiveEverythingForTrueKnowledge"),
    ("SecretsOfTheAllSeeing", "ThreeEyesAreWatchingYou"),
    ("AGICKMAGICKMAGICKMAGICKM", "KMGICKMGICKMGICKMGICKMGICKMGICKM")
    )


##for usedKeyIVPerm in permutations(usedKeyIVPairs):
##    encoded = b""
##    for i in data:
##        encoded += i.to_bytes(1,"big")
##        
##    for key,iv in usedKeyIVPerm:
##        key = bytes(key[:16],"UTF-8")
##        iv = bytes(iv[:16],"UTF-8")
##        counter = Counter.new(128, little_endian=False, initial_value=int.from_bytes(iv,"big"))
##        encoded = AES.new(key, AES.MODE_CTR, counter=counter).decrypt(encoded)
##        
##    print(encoded)

    
##
##testKey = "for_the_seekers_of_truest_of_knowledge"
##
##testKey = testKey.split("_")
##
##
##
##keyA= ""
##keyB= ""
##for k in testKey:
##    keyA += k
##    keyB += k.capitalize()
##
##


#keys = [keyA, keyB]

#print(keys)

keys = []
##keys = ["bdmagick"*4, "Bdmagick"*4, "BDMAGICK"*4]
for key, iv in usedKeyIVPairs:
    keys.append(key[:16]+iv[:16])
    keys.append(iv[:16]+key[:16])



for key in keys:
    key = bytes(key, "UTF-8")

    counter = Counter.new(128, little_endian=True, initial_value=int.from_bytes(key[:16],"little"))

    cipher = AES.new(key[:16], AES.MODE_CTR, counter=counter)
    print(cipher.decrypt(encoded))
    
