import random
import base64
import sys
sys.setrecursionlimit(10000)

# KEY_SIZE = 1024

GENERATOR = 3

def textToNumber(text: str, keySize: int):
    buffer = text.encode('utf-8')
    if len(buffer) > keySize:
        raise ValueError("Text is too long to be converted")
    number = int.from_bytes(buffer)
    if number == 0:
        raise ValueError("Cannot convert empty / null message to number")
    return number

def numberToText(number: int, keySize):
    return number.to_bytes(keySize).decode('utf-8')

def exponentiationModulaireIterative(n: int, k: int, module: int) -> int:
    if k == 0:
        return 1

    acc = 1
    while k > 1:
        if k & 1 == 1:
            acc = (acc * n) % module
            k = k-1
        n = (n*n) % module
        k >>= 1 # Dixvise par 2

    return (n * acc) % module

def exponentiationModulaire(n: int, k: int, module: int) -> int:
    return exponentiationModulaireIterative(n, k, module)

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

def exponentiationModulaireRecursiveBuggée(n: int, k: int, module: int, depth = 0):
    if k == 0:
        return 1
    if k == 1:
        return n
    if (k & 1 == 1):
        return (n * exponentiationModulaireRecursiveBuggée((n * n), (k-1) // 2, module, depth + 1)) % module
    else:
        return exponentiationModulaireRecursiveBuggée((n * n) % module, k // 2, module, depth + 1) % module

def generateKeyPair(keySize: int):
    module = 2**(8 * keySize)
    x = random.randint(1, module - 1)
    h = exponentiationModulaire(GENERATOR, x, module)
    publicKey = h
    privateKey = x
    return publicKey, privateKey

# message: entier dans [1, MODULE[
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

def chiffrementElGamal(msg: str, publicKey: int, keySize: int):
    msgNumber = textToNumber(msg, keySize)
    c1, c2 = encrypt(msgNumber, publicKey, keySize)
    cyphertext = c1.to_bytes(keySize) + c2.to_bytes(keySize)
    return cyphertext

def déchiffrementElGamal(cyphertext: bytes, privateKey: int, keySize: int):
    c1 = int.from_bytes(cyphertext[0:keySize])
    c2 = int.from_bytes(cyphertext[keySize:2*keySize])
    msgNumber = decrypt((c1, c2), privateKey, keySize)
    return numberToText(msgNumber, keySize)

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

