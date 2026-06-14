from elgamal import exponentiationModulaireIterative, exponentiationModulaireRecursive, \
    exponentiationModulaireRecursiveBuggée
from matplotlib import pyplot as plt
import time
import random

def measure(nom: str, func):
    start = time.time()
    func()
    end = time.time()
    elapsed = end - start
    print(f"'{nom}': {elapsed:.6f}")
    return elapsed

def generateOperationsPlot():
    fig, axs = plt.subplots(2)

    sizes = []
    times1 = []
    times2 = []
    times3 = []
    times4 = []
    for keySize in range(32, 500000, 2500):
        module = 2**(8 * keySize)
        x = random.randint(1, module - 1)

        sizes.append(keySize)
        times1.append(measure(f"Simple {keySize}", lambda: x > 1) * 1000)
        times2.append(measure(f"Simple {keySize}", lambda: x == 1) * 1000)
        times3.append(measure(f"Simple {keySize}", lambda: x + 1) * 1000)
        times4.append(measure(f"Simple {keySize}", lambda: x << 1) * 1000)

    axs[0].plot(sizes, times1, "+", label = "x > 1")
    axs[0].plot(sizes, times2, "+", label = "x == 1")
    axs[0].plot(sizes, times3, "+", label = "x + 1")
    axs[0].plot(sizes, times4, "+", label = "x << 1")
    axs[0].set_xlabel("taille de l'entier x (bytes)")
    axs[0].set_ylabel("temps (ms)")
    axs[0].legend()
    axs[0].grid()

    sizes = []
    times1 = []
    times2 = []
    times3 = []
    times4 = []
    for keySize in range(16, 2048, 16):
        module = 2**(8 * keySize)
        x = random.randint(1, module - 1)
        x2 = x*x

        sizes.append(keySize)
        times1.append(measure(f"mult {keySize}", lambda: x * x) * 1000)
        times2.append(measure(f"mult {keySize}", lambda: x * (x+1)) * 1000)
        times3.append(measure(f"mult {keySize}", lambda: x * (x-1)) * 1000)
        times4.append(measure(f"mult {keySize}", lambda: x2 % module) * 1000)

    axs[1].plot(sizes, times1, "+", label = "x * x")
    axs[1].plot(sizes, times2, "+", label = "x * (x+1)")
    axs[1].plot(sizes, times3, "+", label = "x * (x-1)")
    axs[1].plot(sizes, times4, "+", label = "x² % n")
    axs[1].set_xlabel("taille de l'entier x (bytes)")
    axs[1].set_ylabel("temps (ms)")
    axs[1].legend()
    axs[1].grid()
    
    plt.suptitle("Temps d'exécution des opérations élémentaires en fonction de la taille des entiers")
    plt.tight_layout()
    plt.show()

def generateExponentiationPlot():
    sizes = []
    times1 = []
    times2 = []
    times3 = []
    for keySize in range(16, 512, 16):
        module = 2**(8 * keySize)
        x = random.randint(1, module - 1)

        sizes.append(keySize)
        times1.append(measure(f"Iteratif {keySize}", lambda: exponentiationModulaireIterative(3, x, module)) * 1000)
        times2.append(measure(f"Recursif {keySize}", lambda: exponentiationModulaireRecursive(3, x, module)) * 1000)
        # times3.append(measure(f"Recursif buggé {keySize}", lambda: exponentiationModulaireRecursiveBuggée(3, x, module)) * 1000)

    plt.plot(sizes, times1, "+", label = "3^x mod n (Itératif)")
    plt.plot(sizes, times2, "+", label = "3^x mod n (Récursif)")
    # plt.plot(sizes, times3, "+", label = "3^x (Récursif buggé)")
    plt.xlabel("taille des entiers x et n (bytes)")
    plt.ylabel("temps (ms)")
    plt.legend()
    plt.grid()
    
    plt.title("Temps d'exécution de l'exponentiation modulaire")
    plt.show()

generateOperationsPlot()
# generateExponentiationPlot()

