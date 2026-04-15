from elgamal import generateKeyPair, textToNumber, encrypt, decrypt, numberToText, exponentiationModulaireIteratif, exponentiationModulaireRecursive
import base64
from matplotlib import pyplot as plt
import time
import random
import numpy as np

def measure(nom: str, func):
    start = time.time()
    func()
    end = time.time()
    elapsed = end - start
    print(f"'{nom}': {elapsed:.3f}")
    return elapsed

def printb64(msg: str, key: int, keySize: int):
    print(msg, base64.b64encode(key.to_bytes(keySize)).decode('utf-8'))

def bob(keySize: int):
    # Key generation (Alice)
    publicKey, privateKey = generateKeyPair(keySize)
    printb64("publicKey:", publicKey, keySize)
    printb64("privateKey:", privateKey, keySize)

    # Encryption (Bob)
    m = textToNumber("Hello, world !", keySize)
    ciphertext = encrypt(m, publicKey, keySize)
    # print("ciphertext:", ciphertext)

    # Decryption (Alice)
    message = decrypt(ciphertext, privateKey, keySize)
    print(numberToText(message, keySize))

def plotGenerate():
    sizes = []
    timesIteratif = []
    timesRecursif = []
    for keySize in range(32, 513, 16):
        module = 2**(8 * keySize)
        x = random.randint(1, module - 1)

        sizes.append(keySize)
        timesIteratif.append(measure(f"Iteratif {keySize}", lambda: exponentiationModulaireIteratif(3, x, module)))
        timesRecursif.append(measure(f"Recursif {keySize}", lambda: exponentiationModulaireRecursive(3, x, module)))
    
    # a, b = np.polynomial.polynomial.polyfit(sizes.copy(), timesIteratif.copy(), 1)
    # x = np.linspace(32, 512, 100)
    # reg = a*x + b

    plt.plot(sizes, timesIteratif, "+", label = "Itératif")
    plt.plot(sizes, timesRecursif, "+", label = "Recursif")
    # plt.plot(x, reg, "-", label = "Régression")
    plt.xlabel("keySize (bytes)")
    plt.ylabel("temps (s)")
    plt.legend(); plt.grid(); plt.show()

plotGenerate()