from elgamal import generateKeyPair, writeEgKeyToFile
import base64

KEY_SIZE = 256

print("Key size (bytes):", KEY_SIZE)
print("Key size (bits):", KEY_SIZE*8)
print("Modulus:", 2**(KEY_SIZE*8))

public, private = generateKeyPair(KEY_SIZE)
print("public:", base64.b64encode(public).decode('utf-8'))
print("private:", base64.b64encode(private).decode('utf-8'))

writeEgKeyToFile(public, "egPublic.key")
writeEgKeyToFile(private, "egPrivate.key")
