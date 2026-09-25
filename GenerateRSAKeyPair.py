from elgamal import writeKeyToFile
from random_prime_generator import generation,Euclide_etendu_recursif
Ksize= 256
e=65537
def key(KeySize): 
    valeurMax = 2**(8*KeySize) - 1
    p,q=generation(valeurMax),generation(valeurMax)
    n=p*q
    phi=(p-1)*(q-1)
    if (phi <= e):
        print("Phi est trop petit")
        exit()
    _,d=Euclide_etendu_recursif(phi,e)
    return (e,n),(p,q,d)

public,private = key(Ksize)
writeKeyToFile(public, "RSApublic.key", Ksize)
writeKeyToFile(private, "RSAprivate.key", Ksize)