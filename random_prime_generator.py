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

def generation(valeurMax):
    a=randint(2,valeurMax)
    while fermat(a) == False:
        a=randint(2, valeurMax)
    return a

def Euclide_Etendu(a,b):
    u = 1
    v = 0
    r = a
    u2 = 1
    v2 = 0
    r2 = b
    while r2!=0:
        q=r%r2
        u,v,r,u2,v2,r2=u2,v2,r2,u-(q*u2),v-(q*v2),r-(q*r2)
    return r,u,v

""" def Euclide_etendu_recursif(a, b):
    a, b = max(a, b), min(a, b)
    L=[]
    while b != 1:
        q = a // b
        r = a % b
        a = b
        b = r
        L.append((a,b,q,r)) """

def Euclide_etendu_recursif(a,b):
    """
    Contrat: a et b doivent être premiers entre eux et a > b
    Retourne: les coefficients de bezout associés à a et b
    """
    if a <= b:
        print("Il faut a > b")
        exit()
    q = a//b
    r = a % b
    if r == 1:
        return 1, -q
    u,v = Euclide_etendu_recursif(b,r)

    return v, -q*v + u

