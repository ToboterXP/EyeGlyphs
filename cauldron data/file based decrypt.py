
from Crypto.Cipher import AES
from multiprocessing import Pool, freeze_support
import os

#print proper exception tracebacks in the solving processes
import traceback, functools, multiprocessing

def trace_unhandled_exceptions(func):
    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            print ('Exception in '+func.__name__)
            traceback.print_exc()
    return wrapped_func

PROC_COUNT = os.cpu_count()

data = [0x12, 0x3b, 0x92, 0xe2, 0x41, 0xf0, 0xe2, 0x1f, 0xef, 0xf1, 0x03, 0x3e, 0x16, 0xa6, 0x46, 0x3b, 0xdc, 0x00, 0xdd, 0xce, 0xd0, 0xb0, 0x56, 0x1e, 0x98, 0x29, 0xfa, 0x95, 0x13, 0x55, 0x25, 0x9c, 0x45, 0x2e, 0x47, 0xbd, 0x8f, 0x22, 0x98, 0xfc, 0x41, 0x74, 0x68, 0xfc, 0x65, 0x32, 0x36, 0x7b, 0xaf, 0xbc, 0xc7, 0xec, 0x60, 0x14, 0x63, 0xd3, 0xda, 0x20, 0xe3, 0xbf, 0xc4, 0x98, 0xf5, 0x32]

file_path = "C:/Program Files (x86)/Steam/steamapps/common/Noita/noita.exe"


encoded = b""
for i in data:
    encoded += i.to_bytes(1,"big")


file = None
with open(file_path, "rb") as f:
    file = f.read()

print(len(file))

def isText(b):
    return not any(map(lambda a: a < 32 or a > 0xc3, b[:32]))

def decryptData(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    yield "ECB", cipher.decrypt(data)

    cipher = AES.new(key, AES.MODE_CTR, nonce=b"\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a")
    yield "CTR", cipher.decrypt(data)

    iv = data[:16]
    data = data[16:]

    cipher = AES.new(key, AES.MODE_CBC, iv = iv)
    yield "CBC", cipher.decrypt(data)


key_length = 16

def scan(start,stop,step):
    print(start,stop,step)
    stop = min(stop, len(file) - (key_length*step))
    results = []
    for step in (1,19):
        for i in range(start,stop):
            key = file[i:i+(key_length*step):step]
            for cipher_name, plaintext in decryptData(encoded, key):
                if isText(plaintext):
                    results.append((step, i, cipher_name, key, plaintext))

    return results

big_step = 10

steps = [1]

print(f"Creating {PROC_COUNT} workers")
with Pool(PROC_COUNT) as pool:
    print("Starting calculations")
    for i in range(0,len(file)+1,big_step):
        results = pool.starmap(scan, [(i, i+big_step, step) for step in steps])
        print(i, round(i/len(file)*100, 2))
        for r in results:
            print(*r)
        

    

            
    
