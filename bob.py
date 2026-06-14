from elgamal import generateKeyPair, textToNumber, encrypt, decrypt, numberToText
import base64

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