from primes import genere_nb_premier, euclide_etendu_recursif
from rsa import writePublicKey, writePrivateKey

Ksize = 256
e=65537

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
    return (e,n),(p,q,d)

public,private = generateKeyPair(Ksize)

print("public", public)
print("private", private)
print((public[1].bit_length() + 7)//8)
print((private[0].bit_length() + 7)//8)
print((private[1].bit_length() + 7)//8)
print((private[2].bit_length() + 7)//8)

writePublicKey(public, Ksize, "RSApublic.key")
writePrivateKey(private, Ksize, "RSAprivate.key")
