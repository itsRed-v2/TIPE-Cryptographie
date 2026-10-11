from primes import genere_nb_premier, euclide_etendu_recursif
from RSA import rsaPrivateKeyToBytes, rsaPublicKeyToBytes, writeRsaKey, e

Ksize = 256

def generateKeyPair(KeySize):
    valeurMax = 2**(4*KeySize) - 1
    p, q = genere_nb_premier(valeurMax), genere_nb_premier(valeurMax)
    n=p*q
    phi=(p-1)*(q-1)
    if (phi <= e):
        raise ValueError("Phi est trop petit")
    _,d=euclide_etendu_recursif(phi,e)
    if d < 0:
        d += phi
    return rsaPublicKeyToBytes(KeySize, (e,n)), rsaPrivateKeyToBytes(KeySize, (p,q,d))

public,private = generateKeyPair(Ksize)

print("public:", public.hex())
print("private:", private.hex())

writeRsaKey(public, "RSApublic.key")
writeRsaKey(private, "RSAprivate.key")
