from random import randint
from elgamal import exponentiationModulaire

def testPrimalitéFermat(n):
    if exponentiationModulaire(2,n-1,n) != 1:
        return False

    for i in range(50):
        a = randint(3,n-2)
        r = exponentiationModulaire(a,n-1,n)
        if r != 1:
            print("Fermat a attrapé un menteur !!")
            return False
    return True

# def genere_nombre(amount):
#     c = 0
#     for i in range(1, 100*amount):
#         a=randint(1,2**(8*256) - 1)
#         if testPrimalitéFermat(a):
#             c += 1
#             print("Nombre premier numéro:", c, ":", a)
#         if i % amount == 0:
#             print(i // amount, "%")
#     return "premier", c

def genere_nb_premier(valeurMax):
    a=randint(2,valeurMax)
    while testPrimalitéFermat(a) == False:
        a=randint(2, valeurMax)
    print("Fermat a attrapé un nombre premier sauvage !!")
    return a

def euclide_etendu_iteratif(a,b):
    """
    Contrat: a et b doivent être premiers entre eux et a > b
    Retourne: les coefficients de bezout associés à a et b
    """
    if a <= b:
        raise ValueError("Euclide étendu: il faut a > b")
    Q = [a // b]
    r = a % b
    while r != 1:
        a = b
        b = r
        Q.append(a // b)
        r = a % b

        if r == 0:
            raise ValueError("Euclide étendu: a et b ne sont pas premiers entre eux")

    nombreEtape = len(Q)
    signe = -1 if nombreEtape % 2 == 0 else 1

    u = 1
    v = Q.pop()
    while not len(Q) == 0:
        (u, v) = (v, v * Q.pop() + u)

    return signe * u, -signe * v

def euclide_etendu_recursif(a,b):
    """
    Contrat: a et b doivent être premiers entre eux et a > b
    Retourne: les coefficients de bezout associés à a et b
    """
    if a <= b:
        raise ValueError("Euclide étendu: il faut a > b")
    q = a//b
    r = a % b
    if r == 1:
        return 1, -q
    elif r == 0:
        raise ValueError("Euclide étendu: a et b ne sont pas premiers entre eux")
    u,v = euclide_etendu_recursif(b,r)

    return v, -q*v + u

def MillerRabin(n,t):
    r=n-1
    s=0
    while r & 1 == 0:
        s+=1
        r=r//2
    for i in range(1,t+1):
        a=randint(2,n-2)
        y= exponentiationModulaire(a,r,n)
        if y!=1 and y!=n-1 :
            j=1
            while j<=s-1 and y != n-1:
                y = (y**2)%n
                if y==1 :
                    return False
                j+=1
            if y!= n-1:
                return False
    return True

def genere_nb_premierRabin(valeurMax,t):
    a=randint(2,valeurMax)
    while MillerRabin(a,t) == False:
        a=randint(2, valeurMax)
    print("Rabin a attrapé un nombre premier sauvage !!")
    return a

