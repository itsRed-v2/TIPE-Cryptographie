import time
from RSA import generateKeyPair,generateKeyPair_Rabin,chiffrementRSA
from matplotlib import pyplot as plt
from math import sqrt 

def measure(nom: str, func):
    start = time.time()
    for i in range(1):
        func()
    end = time.time()
    elapsed = end - start
    print(f"'{nom}': {elapsed:.6f}")
    return elapsed


def GenerationPlotRSAFermat():
    sizes = []
    times = []
    erreur=[]
    for keySize in range(128, 257, 128):
        valeur=0
        valeur2=0
        for i in range(100):
            a=measure(f"Generation de clé de taille {keySize}", lambda: generateKeyPair(keySize)) * 1000
            
            valeur+=a
            valeur2+=a**2
        valeur/=100
        valeur2/100
        ecart_type=sqrt(valeur2-valeur**2)
        sizes.append(keySize)
        times.append(valeur)
        erreur.append(ecart_type/sqrt(100))

    #plt.plot(sizes, times, "+", label = "Clé")
    plt.errorbar(sizes,times,yerr=erreur,fmt="o")
    plt.legend()
    plt.grid()
    plt.xlabel("Taille de Clé")
    plt.ylabel("Temps d'exécution plus ou moins l'erreur")
    plt.title("Temps d'exécution de la Génération de clé pour RSA pour Fermat")
    plt.show()  


def GenerationPlotRSARabin():
    sizes = []
    times = []
    erreur=[]
    for keySize in range(128, 257, 128):
        valeur=0
        valeur2=0
        for i in range(100):
            a=measure(f"Generation de clé de taille {keySize}", lambda: generateKeyPair_Rabin(keySize)) * 1000
            
            valeur+=a
            valeur2+=a**2
        valeur/=100
        valeur2/=100
        ecart_type=sqrt(valeur2-valeur**2)
        sizes.append(keySize)
        times.append(valeur)
        erreur.append(ecart_type/sqrt(100))

    
    plt.errorbar(sizes,times,yerr=erreur,fmt="o")
    plt.legend()
    plt.grid()
    plt.xlabel("Taille de Clé")
    plt.ylabel("Temps d'exécution plus ou moins l'erreur")
    plt.title("Temps d'exécution de la Génération de clé pour RSA avec Miller-Rabin")
    plt.show()  
    print(erreur[0]/erreur[1])
GenerationPlotRSARabin()