from elgamal import exponentiationModulaire,textToNumber,numberToText,readKeyFromFile
from random_prime_generator import generation,Euclide_etendu_recursif
Ksize= 256
e=65537
PrivateKey,PublicKey = readKeyFromFile("RSApublic.key",Ksize),readKeyFromFile("RSAprivate.key",Ksize)
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



def chiffrementRSA(msg):
    M=textToNumber(msg,Ksize-1)
    C=exponentiationModulaire(M,PublicKey[0],PublicKey[1])
    return C
Message=chiffrementRSA("Hello tout le monde")
print(Message)   

def déchiffrementRSA(chiffré):
    M=exponentiationModulaire(chiffré,PrivateKey[2],PublicKey[1])
    return numberToText(M,Ksize - 1)
print(déchiffrementRSA(Message))


