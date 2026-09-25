from elgamal import exponentiationModulaire,textToNumber,numberToText
import base64

e = 65537

def chiffrementRSA(msg: str, PublicKey: tuple[int,int], Ksize: int):
    e,n = PublicKey
    M=textToNumber(msg,Ksize-1)
    C=exponentiationModulaire(M,e,n)
    return C

def déchiffrementRSA(chiffré: int, PrivateKey: tuple[int,int,int], Ksize: int):
    p,q,d = PrivateKey
    n = p*q
    M=exponentiationModulaire(chiffré,d,n)
    return numberToText(M,Ksize - 1)

#############################
# MANIPULATION DES FICHIERS #
#############################

def writeBytesToFile(buffer: bytes, filename: str):
    with open(filename, 'w') as file:
        bytesString = base64.b64encode(buffer).decode('ascii')
        lines = [bytesString[i:i+64] for i in range(0, len(bytesString), 64)]
        file.write("\n".join(lines))

def readBytesFromFile(expectedSize: int, filename: str):
    with open(filename, 'r') as file:
        lines = [l.strip() for l in file.readlines()]
        bytesString = "".join(lines)
        buffer = base64.b64decode(bytesString)
        assert len(buffer) == expectedSize and "Key size in file does not match expected size"
        return buffer

def writePublicKey(key: tuple[int,int], keySize: int, filename: str):
    _,n = key
    writeBytesToFile(n.to_bytes(keySize), filename)

def writePrivateKey(key: tuple[int,int,int], keySize: int, filename: str):
    p,q,d = key
    buffer = p.to_bytes(keySize//2) + q.to_bytes(keySize//2) + d.to_bytes(keySize)
    writeBytesToFile(buffer, filename)

def readPublicKey(keySize: int, filename: str):
    buffer = readBytesFromFile(keySize, filename)
    return (e,int.from_bytes(buffer))

def readPrivateKey(keySize: int, filename: str):
    buffer = readBytesFromFile(2*keySize, filename)
    p = int.from_bytes(buffer[0:keySize//2])
    q = int.from_bytes(buffer[keySize//2:keySize])
    d = int.from_bytes(buffer[keySize:2*keySize])
    return (p,q,d)
