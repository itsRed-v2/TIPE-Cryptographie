from elgamal import generateKeyPair, textToNumber, encrypt, decrypt, numberToText

# Key generation (Alice)
publicKey, privateKey = generateKeyPair()
print("publicKey:", publicKey)
print("privateKey:", privateKey)

# Encryption (Bob)
m = textToNumber("Hello, world !")
ciphertext = encrypt(m, publicKey)
print("ciphertext:", ciphertext)

# Decryption (Alice)
message = decrypt(ciphertext, privateKey)
print(numberToText(message))