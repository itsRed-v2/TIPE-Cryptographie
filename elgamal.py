import random
import base64

MODULE = 2**256
GENERATOR = 3

def textToNumber(text: str):
    buffer = text.encode('utf-8')
    if len(buffer) > 32:
        print("Text is too long to be converted")
        exit(1)
    return int.from_bytes(buffer)

def numberToText(number: int):
    return number.to_bytes(32).decode('utf-8')

def exponentiationModulaire(n: int, k: int, module: int) -> int:
    if (k == 0):
        return 1
    if (k & 1 == 1):
        return (n * exponentiationModulaire(n, k-1, module)) % module
    else:
        return exponentiationModulaire((n * n) % module, k // 2, module) % module

def generateKeyPair():
    x = random.randint(1, MODULE - 1)
    h = exponentiationModulaire(3, x, MODULE)
    publicKey = h
    privateKey = x
    return publicKey, privateKey

# message: entier dans [0, MODULE[
def encrypt(message, publicKey):
    y = random.randint(1, MODULE - 1)
    s = exponentiationModulaire(publicKey,y,MODULE)
    c1 = exponentiationModulaire(GENERATOR, y, MODULE)
    c2 = (message * s) % MODULE
    ciphertext = (c1, c2)
    return ciphertext

def decrypt(ciphertext, privateKey):
    c1, c2 = ciphertext
    sInv = exponentiationModulaire(c1, MODULE - privateKey, MODULE)
    message = (c2 * sInv) % MODULE
    return message

def writeKeyToFile(key: int, filename: str):
    with open(filename, 'wb') as file:
        file.write(base64.b64encode(key.to_bytes(32)))

def readKeyFromFile(filename: str):
    with open(filename, 'rb') as file:
        return int.from_bytes(base64.b64decode(file.read()))
        