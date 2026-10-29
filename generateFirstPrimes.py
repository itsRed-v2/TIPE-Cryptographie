from primes import MillerRabin

P = [2, 3]
for i in range(4, 200):
    if MillerRabin(i, 10):
        P.append(i)

print(P)
print(len(P))
