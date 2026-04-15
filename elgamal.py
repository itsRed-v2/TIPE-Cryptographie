import random
import base64
import sys
sys.setrecursionlimit(10000)

# KEY_SIZE = 1024

GENERATOR = 3

def textToNumber(text: str, keySize: int):
    buffer = text.encode('utf-8')
    if len(buffer) > keySize:
        print("Text is too long to be converted")
        exit(1)
    return int.from_bytes(buffer)

def numberToText(number: int, keySize):
    return number.to_bytes(keySize).decode('utf-8')

def exponentiationModulaireIteratif(n: int, k: int, module: int) -> int:
    if k == 0:
        return 1
    
    acc = 1    
    while k > 1:
        if k & 1 == 1:
            acc = (acc * n) % module
            k = k-1
        n = (n*n) % module
        k //= 2

    return (n * acc) % module

def exponentiationModulaire(n: int, k: int, module: int) -> int:
    return exponentiationModulaireRecursive(n, k, module)

def exponentiationModulaireRecursive(n: int, k: int, module: int, depth = 0):
    # print("depth", depth)
    if k == 0:
        return 1
    if k == 1:
        return n
    if (k & 1 == 1):
        return (n * exponentiationModulaireRecursive((n * n) % module, (k-1) // 2, module, depth + 1)) % module
    else:
        return exponentiationModulaireRecursive((n * n) % module, k // 2, module, depth + 1)

def generateKeyPair(keySize: int):
    module = 2**(8 * keySize)
    x = random.randint(1, module - 1)
    h = exponentiationModulaire(3, x, module)
    publicKey = h
    privateKey = x
    return publicKey, privateKey

# message: entier dans [0, MODULE[
def encrypt(message: int, publicKey: int, keySize: int) -> tuple[int, int]:
    module = 2**(8 * keySize)

    y = random.randint(1, module - 1)
    s = exponentiationModulaire(publicKey,y,module)
    c1 = exponentiationModulaire(GENERATOR, y, module)
    c2 = (message * s) % module
    ciphertext = (c1, c2)
    return ciphertext

def decrypt(ciphertext: tuple[int, int], privateKey: int, keySize: int):
    module = 2**(8 * keySize)

    c1, c2 = ciphertext
    sInv = exponentiationModulaire(c1, module - privateKey, module)
    message = (c2 * sInv) % module
    return message

def writeKeyToFile(key: int, filename: str, keySize: int):
    with open(filename, 'w') as file:
        keyString = base64.b64encode(key.to_bytes(keySize)).decode('ascii')
        lines = [keyString[i:i+64] for i in range(0, len(keyString), 64)]
        file.write("\n".join(lines))

def readKeyFromFile(filename: str, keySize: int):
    with open(filename, 'r') as file:
        lines = [l.strip() for l in file.readlines()]
        keyString = "".join(lines)
        keyBytes = base64.b64decode(keyString)
        assert len(keyBytes) == keySize and "Key size in file does not match expected size"
        return int.from_bytes(keyBytes)
        