from primes import MillerRabin

# Le but de ce script est de générer des nombres pour le crible
# d'érathosthène. Il ne peut donc pas, par principe, utiliser le
# test de primalité basé sur le crible.
P = [2, 3]
for i in range(4, 200):
    if MillerRabin(i, 10):
        P.append(i)

print(P)
print(len(P))
