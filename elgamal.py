import random
import base64

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
    # VERSION WIKIPEDIA à RÉÉCRIRE
    if k == 0:
        return 1
    y = 1
    while k > 1:
        # print("k:", k)
        if k & 1 == 1:
            y = (n * y) % module
            k -= 1
        n = (n * n) % module
        k //= 2
    return (n * y) % module

def exponentiationModulaire(n: int, k: int, module: int) -> int:
    return exponentiationModulaireIteratif(n, k, module)

def exponentiationModulaireRecursive(n: int, k: int, module: int, depth = 0):
    print("depth", depth)
    if k == 0:
        return 1
    if k == 1:
        return n
    if (k & 1 == 1):
        return (n * exponentiationModulaire((n * n), (k-1) // 2, module, depth + 1)) % module
    else:
        return exponentiationModulaire((n * n) % module, k // 2, module, depth + 1) % module

def generateKeyPair(keySize: int):
    module = 2**(8 * keySize)
    x = random.randint(1, module - 1)
    h = exponentiationModulaire(3, x, module)
    publicKey = h
    privateKey = x
    return publicKey, privateKey

# message: entier dans [0, MODULE[
def encrypt(message: int, publicKey: int, keySize: int):
    module = 2**(8 * keySize)

    y = random.randint(1, module - 1)
    s = exponentiationModulaire(publicKey,y,module)
    c1 = exponentiationModulaire(GENERATOR, y, module)
    c2 = (message * s) % module
    ciphertext = (c1, c2)
    return ciphertext

def decrypt(ciphertext: int, privateKey: int, keySize: int):
    module = 2**(8 * keySize)

    c1, c2 = ciphertext
    sInv = exponentiationModulaire(c1, module - privateKey, module)
    message = (c2 * sInv) % module
    return message

def writeKeyToFile(key: int, filename: str, keySize: int):
    with open(filename, 'wb') as file:
        file.write(base64.b64encode(key.to_bytes(keySize)))

def readKeyFromFile(filename: str, keySize: int):
    with open(filename, 'rb') as file:
        key = int.from_bytes(base64.b64decode(file.read()))
        assert len(key) == keySize
        return key
        