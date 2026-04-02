from elgamal import generateKeyPair, textToNumber, encrypt, decrypt, numberToText
import base64
from matplotlib import pyplot as plt
import time

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
    times = []
    square = []
    cube = []
    for keySize in range(32, 256, 4):
        sizes.append(keySize)
        times.append(measure("genration de clé", lambda: generateKeyPair(keySize)))
        square.append(0.000001 * keySize * keySize)
        cube.append(0.0000000045 * keySize ** 3)
    plt.plot(sizes, times, "+", label = "mesure")
    plt.plot(sizes, square, "-r", label = "x²")
    plt.plot(sizes, cube, "-g", label = "x³")
    plt.xlabel("keySize (bytes)")
    plt.ylabel("temps (s)")
    plt.legend(); plt.grid(); plt.show()

plotGenerate()