import random
import base64
import sys
sys.setrecursionlimit(10000)

# Dictionnaire des grandeurs caractérisant les groupes cycliques
# qui ont été choisis pour l'algorithme ElGamal, en fonction de la taille
# de clé. Par exemple, l'entrée "256" du dictionnaire contient les valeurs
# de p (module) et de g (générateur) adéquates pour faire de la cryptographie
# sur clés de 256 octets
GROUPS = {
    256: {
        "module": 2231279641809778414042138165334162145657932302276767098151002640656710309689966528617863625161123262024116377345735417270007300588281961430651039766810540737800256188907850671735526523496382227954615505449730148174950259851122637985760498586575137751289603253868148734851071871283863711679605101899165715724400570038677902164403366816258882688939253584026566656805802977640884243599670262630311093709466135319990359031093080198583212098326807764977663061831731367283896166008328080864992085001495739707341519858854821801258959939293936809281644664946582846059330278637172337715040150073770486125845065011305758473241,
        "generator": 21
    },
    128: {
        # Module de 1024 bits (taille maximale)
        "module": 100607772876646128201798332972070110049398790234381925978712721206755231881297020265810465747071262995512830414153850031722437629375800027449928429898489105960686267499465158380871054410705326337713896093359639097537576397923331045485851807545034506007959844528147869262105052741293931362271955074056585931753,
        "generator": 5
    }
}

# Récupère le module et le générateur du groupe configuré pour une taille de clé donnée.
def getGroup(keySize: int):
    if keySize not in GROUPS:
        raise ValueError(f"Aucun groupe configuré pour une taille de clé de {keySize} octets.")
    group = GROUPS[keySize]
    return group["module"], group["generator"]

def textToNumber(text: str, bufferLength: int):
    buffer = text.encode('utf-8')
    if len(buffer) > bufferLength:
        raise ValueError("Text is too long to be converted")
    number = int.from_bytes(buffer)
    if number == 0:
        raise ValueError("Cannot convert empty / null message to number")
    return number

def numberToText(number: int, bufferLength: int):
    return number.to_bytes(bufferLength).decode('utf-8')

def exponentiationModulaireIterative(n: int, k: int, module: int) -> int:
    if k == 0:
        return 1

    acc = 1
    while k > 1:
        if k & 1 == 1:
            acc = (acc * n) % module
            k = k-1
        n = (n*n) % module
        k >>= 1 # Dixvise par 2

    return (n * acc) % module

def exponentiationModulaire(n: int, k: int, module: int) -> int:
    return exponentiationModulaireIterative(n, k, module)

def exponentiationModulaireRecursive(n: int, k: int, module: int, depth = 0):
    # print("depth", depth)
    if k == 0:
        return 1
    if k == 1:
        return n
    if (k & 1 == 1):
        return (n * exponentiationModulaireRecursive((n * n) % module, (k-1) // 2, module, depth + 1)) % module
    else:
        return exponentiationModulaireRecursive((n * n) % module, k // 2, module, depth + 1)

def exponentiationModulaireRecursiveBuggée(n: int, k: int, module: int, depth = 0):
    if k == 0:
        return 1
    if k == 1:
        return n
    if (k & 1 == 1):
        return (n * exponentiationModulaireRecursiveBuggée((n * n), (k-1) // 2, module, depth + 1)) % module
    else:
        return exponentiationModulaireRecursiveBuggée((n * n) % module, k // 2, module, depth + 1) % module

def generateKeyPair(keySize: int):
    p, g = getGroup(keySize)

    x = random.randint(1, p - 1)
    h = exponentiationModulaire(g, x, p)
    publicKey = h
    privateKey = x
    return publicKey.to_bytes(keySize), privateKey.to_bytes(keySize)

# message: entier dans [1, p[
def encrypt(message: int, publicKey: int, keySize: int) -> tuple[int, int]:
    p, g = getGroup(keySize)

    y = random.randint(1, p - 1)
    s = exponentiationModulaire(publicKey,y,p)
    c1 = exponentiationModulaire(g, y, p)
    c2 = (message * s) % p
    ciphertext = (c1, c2)
    return ciphertext

def decrypt(ciphertext: tuple[int, int], privateKey: int, keySize: int):
    p, _g = getGroup(keySize)

    c1, c2 = ciphertext
    sInv = exponentiationModulaire(c1, p - 1 - privateKey, p)
    message = (c2 * sInv) % p
    return message

def chiffrementElGamal(msg: str, publicKey: bytes, keySize: int):
    assert len(publicKey) == keySize
    msgNumber = textToNumber(msg, keySize-1)
    c1, c2 = encrypt(msgNumber, int.from_bytes(publicKey), keySize)
    cyphertext = c1.to_bytes(keySize) + c2.to_bytes(keySize)
    return cyphertext

def déchiffrementElGamal(cyphertext: bytes, privateKey: bytes, keySize: int):
    assert len(privateKey) == keySize
    c1 = int.from_bytes(cyphertext[0:keySize])
    c2 = int.from_bytes(cyphertext[keySize:2*keySize])
    msgNumber = decrypt((c1, c2), int.from_bytes(privateKey), keySize)
    return numberToText(msgNumber, keySize-1)

#######################
# SAUVEGARDE DES CLÉS #
#######################

def writeEgKeyToFile(key: bytes, filename: str):
    with open(filename, 'w') as file:
        keyString = base64.b64encode(key).decode('ascii')
        lines = [keyString[i:i+64] for i in range(0, len(keyString), 64)]
        file.write("\n".join(lines))

def readEgKeyFromFile(filename: str, keySize: int):
    with open(filename, 'r') as file:
        lines = [l.strip() for l in file.readlines()]
        keyString = "".join(lines)
        keyBytes = base64.b64decode(keyString)
        assert len(keyBytes) == keySize and "Key size in file does not match expected size"
        return keyBytes

