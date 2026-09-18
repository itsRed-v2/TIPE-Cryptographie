from random import*
from elgamal import exponentiationModulaire
def fermat(n):
    if exponentiationModulaire(2,n-1,n)==1:
        return True
    else:
        return False
def premier_test(p):
    c = 0
    for i in range(1, 100*p):
        a=randint(1,2**(8*256) - 1)
        if fermat(a):
            c += 1
            print("Nombre premier numéro:", c, ":", a)
        if i % p == 0:
            print(i // 100, "%")
    return "premier", c

def generation(KeySize):
    a=randint(1,KeySize)
    while fermat(a) == False:
        a=randint(1,KeySize)
    return a

def Euclide_Etendu():
    pass