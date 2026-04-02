from elgamal import generateKeyPair, writeKeyToFile
import base64

KEY_SIZE = 256

print("Key size (bytes):", KEY_SIZE)
print("Key size (bits):", KEY_SIZE*8)
print("Modulus:", 2**(KEY_SIZE*8))

public, private = generateKeyPair(KEY_SIZE)
print("public:", base64.b64encode(public.to_bytes(KEY_SIZE)).decode('utf-8'))
print("private:", base64.b64encode(private.to_bytes(KEY_SIZE)).decode('utf-8'))

writeKeyToFile(public, "public.key", KEY_SIZE)
writeKeyToFile(private, "private.key", KEY_SIZE)