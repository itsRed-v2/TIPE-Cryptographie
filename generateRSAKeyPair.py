from functions.RSA import writeRsaKey, generateKeyPair

Ksize = 256

public,private = generateKeyPair(Ksize)

print("public:", public.hex())
print("private:", private.hex())

writeRsaKey(public, "RSApublic.key")
writeRsaKey(private, "RSAprivate.key")
