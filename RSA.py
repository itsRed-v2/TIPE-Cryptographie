from elgamal import exponentiationModulaire,textToNumber,numberToText
from primes import euclide_etendu_iteratif
import base64

e = 65537

def chiffrementRSA(msg: str, PublicKey: bytes, Ksize: int):
    e,n = rsaPublicKeyFromBytes(PublicKey,Ksize)
    M=textToNumber(msg,Ksize-1)
    C=exponentiationModulaire(M,e,n)
    return C.to_bytes(Ksize)

def dechiffrementRSA(chiffré: bytes, PrivateKey: bytes, Ksize: int):
    p,q,d = rsaPrivateKeyFromBytes(PrivateKey,Ksize)
    n = p*q
    M=exponentiationModulaire(int.from_bytes(chiffré),d,n)
    return numberToText(M,Ksize - 1)

def dechiffrementTRC(chiffré: bytes, PrivateKey: bytes, Ksize: int):
    p,q,d = rsaPrivateKeyFromBytes(PrivateKey,Ksize)
    c = int.from_bytes(chiffré)
    d_p = d % (p - 1)
    d_q = d % (q - 1)
    m_p = exponentiationModulaire(c,d_p,p)
    m_q = exponentiationModulaire(c,d_q,q)
    if q > p:
        invq,_ = euclide_etendu_iteratif(q,p)
    else:
        _,invq = euclide_etendu_iteratif(p,q)
    m = m_q + q *(((m_p - m_q) * invq) % p)
    return numberToText(m,Ksize-1)

#########################
# MANIPULATION DES CLÉS #
#########################

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

def writeRsaKey(key: bytes, filename: str):
    writeBytesToFile(key, filename)

def readRsaPublicKey(keySize: int, filename: str):
    return readBytesFromFile(keySize, filename)

def readRsaPrivateKey(keySize: int, filename: str):
    return readBytesFromFile(2*keySize, filename)

def rsaPublicKeyToBytes(keySize: int, key: tuple[int,int]):
    _,n = key
    return n.to_bytes(keySize)

def rsaPublicKeyFromBytes(buffer: bytes, keySize: int):
    assert len(buffer) == keySize
    return (e,int.from_bytes(buffer))

def rsaPrivateKeyToBytes(keySize: int, key: tuple[int,int,int]):
    p,q,d = key
    return p.to_bytes(keySize//2) + q.to_bytes(keySize//2) + d.to_bytes(keySize)

def rsaPrivateKeyFromBytes(buffer: bytes, keySize: int):
    assert len(buffer) == 2*keySize
    p = int.from_bytes(buffer[0:keySize//2])
    q = int.from_bytes(buffer[keySize//2:keySize])
    d = int.from_bytes(buffer[keySize:2*keySize])
    return (p,q,d)

