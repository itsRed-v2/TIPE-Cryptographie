from primes import genere_nb_premier_crible_rabin, test_primalité
import time

def measure(nom: str, func):
    start = time.time()
    for i in range(1):
        func()
    end = time.time()
    elapsed = end - start
    print(f"'{nom}': {elapsed:.6f}")
    return elapsed

def generatePrimeWithLargeDivisor(byteLength: int):
    q_upper_bound = 2**(8*byteLength - 1) - 1
    while True:
        q = genere_nb_premier_crible_rabin(q_upper_bound, 2)
        for r in range(2,10):
            p = 2*r*q + 1
            if test_primalité(p, 2):
                return q,r,p
        print("false")

def generateGenerator(n, factorisation: list[tuple[int, int]]):
    pass

print(generatePrimeWithLargeDivisor(256))

# p = 7810396139864507092826132549272952014573737275090886821459844712634635100010684936462249266950270509181666418055488025595826655257594481558013226920603945630763712837086896458041657192995574457106868726161064212769342239440837441599743376622149930083111099536082440132714054633982289004024025520491395520704554594135955480012667380966824969814577616293124887432345846133157415934463626171622588895478796352260056658499260724462739257659625715733515025502665655478103913708178271856175129406813112673078667310174407018583413911053433944307374302178376596044028281198651275291462335316201900689708744565326430341285147
#
# measure("sieve", lambda: test_primalité(20497*p, 50))
# measure("rabin", lambda: MillerRabin(20497*p, 50))

