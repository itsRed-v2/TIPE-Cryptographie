import time
from RSA import generateKeyPair
from matplotlib import pyplot as plt


def measure(nom: str, func):
    start = time.time()
    for i in range(1):
        func()
    end = time.time()
    elapsed = end - start
    print(f"'{nom}': {elapsed:.6f}")
    return elapsed


def GenerationPlot():
    sizes = []
    times = []
    for keySize in range(16, 64, 2):
        valeur=0
        for i in range(100):
            a=times.append(measure(f"Generation de clé de taille {keySize}", lambda: generateKeyPair(valeur)) * 1000)
            
            valeur+=a
        valeur/=100
        sizes.append(keySize)
        times.append(valeur)

    plt.plot(sizes, times, "+", label = "Clé")
    plt.xlabel("taille des entiers x et n (bytes)")
    plt.ylabel("temps (ms)")
    plt.legend()
    plt.grid()

    plt.title("Temps d'exécution de la Génération de clé pour RSA")
    plt.show()  

GenerationPlot()