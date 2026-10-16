from elgamal import generateKeyPair, textToNumber, encrypt, decrypt, numberToText
from RSA import dechiffrementTRC, readRsaPrivateKey, readRsaPublicKey, chiffrementRSA, dechiffrementRSA
from primes import MillerRabin, testPrimalitéFermat, genere_nb_premierRabin
import base64

def printb64(msg: str, key: bytes):
    print(msg, base64.b64encode(key).decode('utf-8'))

def bobEG(keySize: int):
    # Key generation (Alice)
    publicKey, privateKey = generateKeyPair(keySize)
    printb64("publicKey:", publicKey)
    printb64("privateKey:", privateKey)

    # Encryption (Bob)
    m = textToNumber("Hello, world !", keySize)
    ciphertext = encrypt(m, int.from_bytes(publicKey), keySize)
    # print("ciphertext:", ciphertext)

    # Decryption (Alice)
    message = decrypt(ciphertext, int.from_bytes(privateKey), keySize)
    print(numberToText(message, keySize))

def bobRSA():
    Ksize = 256
    PrivateKey = readRsaPrivateKey(Ksize, "RSAprivate.key")
    PublicKey = readRsaPublicKey(Ksize, "RSApublic.key")

    chiffré=chiffrementRSA("Hello tout le monde",PublicKey,Ksize)
    printb64("chiffré:", chiffré)
    print("dechiffrement classique:", dechiffrementRSA(chiffré,PrivateKey,Ksize))
    print("dechiffrement TRC:", dechiffrementTRC(chiffré,PrivateKey,Ksize))

def bobMiller():
    print(MillerRabin(2821,5))
    print(testPrimalitéFermat(2821))

    print(genere_nb_premierRabin(2**(8*256)-1,5))

# bobEG(256)
# bobRSA()
bobMiller()
