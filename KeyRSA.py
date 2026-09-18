from elgamal import exponentiationModulaire
from random_prime_generator import generation

def key(KeySize):
    p,q=generation(KeySize),generation(KeySize)
    n=p*q
    phi=(p-1)*(q-1)
    

    
