from primes import genere_nb_premier, euclide_etendu_recursif
from RSA import rsaPrivateKeyToBytes, rsaPublicKeyToBytes, writeRsaKey, e, generateKeyPair


Ksize = 256



public,private = generateKeyPair(Ksize)

print("public:", public.hex())
print("private:", private.hex())

writeRsaKey(public, "RSApublic.key")
writeRsaKey(private, "RSAprivate.key")
