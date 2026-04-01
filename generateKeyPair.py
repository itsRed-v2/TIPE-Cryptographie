from elgamal import generateKeyPair, writeKeyToFile
import base64

public, private = generateKeyPair()
print("public:", base64.b64encode(public.to_bytes(32)).decode('utf-8'))
print("private:", base64.b64encode(private.to_bytes(32)).decode('utf-8'))

writeKeyToFile(public, "public.key")
writeKeyToFile(private, "private.key")