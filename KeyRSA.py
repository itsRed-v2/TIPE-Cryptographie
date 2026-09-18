from elgamal import exponentiationModulaire
from random_prime_generator import generation,Euclide_etendu_recursif

e=65537
def key(KeySize):
    p,q=generation(KeySize),generation(KeySize)
    n=p*q
    phi=(p-1)*(q-1)
    _,d=Euclide_etendu_recursif(phi,e)
    return (e,n),(p,q,d)

    

