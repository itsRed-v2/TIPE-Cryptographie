import base64

# Ce fichier contient les fonctions qui sont utiles à la fois à ElGamal et à RSA

##############################################################
# Isomorphisme entre espace des textes et espace des entiers #
##############################################################

def textToNumber(text: str, bufferLength: int):
    buffer = text.encode('utf-8')
    if len(buffer) > bufferLength:
        raise ValueError("Text is too long to be converted")
    number = int.from_bytes(buffer)
    if number == 0:
        raise ValueError("Cannot convert empty / null message to number")
    return number

def numberToText(number: int, bufferLength: int):
    return number.to_bytes(bufferLength).decode('utf-8')

############################
# Exponentiation modulaire #
############################

import sys
sys.setrecursionlimit(10000)

def exponentiationModulaire(n: int, k: int, module: int) -> int:
    return exponentiationModulaireIterative(n, k, module)

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

############################
# Manipulation de fichiers #
############################

def writeBytesToFile(buffer: bytes, filename: str):
    with open(filename, 'w') as file:
        bytesString = base64.b64encode(buffer).decode('ascii')
        lines = [bytesString[i:i+64] for i in range(0, len(bytesString), 64)]
        file.write("\n".join(lines))

def readBytesFromFile(expectedSize: int, filename: str):
    with open(filename, 'r') as file:
        lines = [l.strip() for l in file.readlines()]
        bytesString = "".join(lines)
        buffer = base64.b64decode(bytesString)
        assert len(buffer) == expectedSize and "Key size in file does not match expected size"
        return buffer

