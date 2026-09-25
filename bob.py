from elgamal import generateKeyPair, textToNumber, encrypt, decrypt, numberToText
from RSA import readPrivateKey, readPublicKey, chiffrementRSA, déchiffrementRSA
import base64

def printb64(msg: str, key: int, keySize: int):
    print(msg, base64.b64encode(key.to_bytes(keySize)).decode('utf-8'))

def bobEG(keySize: int):
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

def bobRSA():
    Ksize = 256
    PrivateKey = readPrivateKey(Ksize, "RSAprivate.key")
    PublicKey = readPublicKey(Ksize, "RSApublic.key")

    chiffré=chiffrementRSA("Hello tout le monde",PublicKey,Ksize)
    print(chiffré)
    print(déchiffrementRSA(chiffré,PrivateKey,Ksize))

bobRSA()
