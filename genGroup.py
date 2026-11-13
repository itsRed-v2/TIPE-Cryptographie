from elgamal import exponentiationModulaire
from primes import genere_nb_premier_crible_rabin, test_primalité

def generatePrimeWithLargeDivisor(byteLength: int):
    # m: nombre de bits alloués à r. Une plus grande valeur accélère le calcul
    # tandis que une plus petite valeur diminue le nombre de facteurs dans la
    # décomposition en facteurs premiers de p = 2*r*q+1
    m = 4
    # Nombre de bytes pour q: 8*byteLength - m - 1
    # car p = 2*r*q+1 et 2*r est un nombre de m+1 bits au plus (preuve détaillée dans le carnet de TIPE)
    q_max = 2**(8*byteLength - m - 1) - 1
    r_max = 2**m - 1 # 255 quand m vaut 8
    while True:
        q = genere_nb_premier_crible_rabin(q_max, 2)
        for r in range(2,r_max):
            p = 2*r*q + 1
            if test_primalité(p, 2):
                return q,r,p
        print("q ne convient pas")

def factor(n: int) -> list[tuple[int,int]]:
    if n == 1:
        return []
    for p in range(2, n+1):
        if n % p == 0:
            e = 1
            while n % p**(e+1) == 0:
                e += 1
            return [(p, e)] + factor(n // p**e)
    assert False # La boucle ne peut pas se terminer autrement que par le return.

def generateGenerator(n, factorisation: list[tuple[int, int]]):
    p = n + 1 # Module du groupe cyclique
    g = 1
    while True:
        g += 1
        for pi, _ei in factorisation:
            assert n % pi == 0
            # vérifie g^k n'est pas égal à 1 pour k les diviseurs maximaux de n
            if exponentiationModulaire(g, n//pi, p) == 1:
                break
        else:
            return g

def indicatrice_euler(factorisation):
    phi = 1
    for pi,ei in factorisation:
        phi *= (pi**ei - pi**(ei-1))
    return phi

def generateGroupAndGenerator(byteLength: int):
    q,r,p = generatePrimeWithLargeDivisor(byteLength)
    bitLength = p.bit_length()
    if bitLength <= 8*(byteLength - 1):
        print("Erreur: le nombre premier généré est trop petit.")
        print(f"Longueur de p: {bitLength} bits. Attendu: {8*byteLength} >= l > {8*(byteLength-1)}")

    # décomposition en facteurs premier de p - 1 = 2*r*q
    facteurs = [(q, 1)] + factor(2*r)
    print("facteurs:", facteurs)

    phi = indicatrice_euler(facteurs)
    print("phi =", phi)
    print(f"proportion de générateurs: {100*phi/(p-1):.1f}%")
    g = generateGenerator(p-1, facteurs)
    return p,g

p,g = generateGroupAndGenerator(256)
print((p,g))
print("bit length of p:", p.bit_length())

