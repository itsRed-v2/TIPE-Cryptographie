from primes import genere_nb_premier, testPrimalitéFermat

def generatePrimeWithLargeDivisor(byteLength: int):
    q_upper_bound = 2**(8*byteLength - 1) - 1
    while True:
        q = genere_nb_premier(q_upper_bound)
        for r in range(2,200):
            p = 2*r*q + 1
            if testPrimalitéFermat(p):
                return q,r,p

print(generatePrimeWithLargeDivisor(256))


def generateGenerator(n, factorisation: list[tuple[int, int]]):
    pass
