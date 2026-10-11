import socket
import threading
from RSA import chiffrementRSA, dechiffrementRSA, readRsaPrivateKey, readRsaPublicKey
from elgamal import chiffrementElGamal, déchiffrementElGamal, readEgKeyFromFile
from enum import Enum
import sys
import os
import signal

# =================
# === CONSTANTS ===
# =================

HOST_PORT = 6008
KEY_SIZE = 256

rsaPrivateKeyFile = "RSAprivate.key"
rsaPublicKeyFile = "RSApublic.key"
egPrivateKeyFile = "egPrivate.key"
egPublicKeyFile = "egPublic.key"

# =====================================
# === CLASS AND FUNCTION DEFINITION ===
# =====================================

# PACKET LAYOUT: | content length (2B) | packet type (1B) | content |

class PacketType(Enum):
    MESSAGE = 1
    PUBKEY_SHARE = 2

    def byte(self):
        return self.value.to_bytes(1)

class KeyType(Enum):
    ELGAMAL = 1
    RSA = 2

    def byte(self):
        return self.value.to_bytes(1)

# Détermine l'adresse à laquelle le PC peut être contacté
# sur le réseau LOCAL où il est connecté.
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # doesn't even have to be reachable
    s.connect(('10.254.254.254', 1))
    IP = s.getsockname()[0]
    s.close()
    return IP

# Cette fonction, executée dans un thread parallèle, envoie les messages écrits
# par l'utilisateur.
def read_stdin(connection: socket.socket, remotePublicKey: bytes):
    while True:
        msg = input().strip()
        send_message(connection, msg, remotePublicKey)

# Cette fonction crée un serveur qui va réceptionner une éventuelle connection
# de la part d'un ordinateur qui veut communiquer.
def listen_for_peers():
    HOST_IP = get_ip()

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((HOST_IP, HOST_PORT))
    serverSocket.listen(0) # become a server socket, only one connection allowed (no backlog).
    print(f"Listening for incoming connections on local network at {HOST_IP}:{HOST_PORT}")

    # La fonction accept est bloquante et retourne un socket
    # dès qu'une connection est reçue par le serveur.
    connection, address = serverSocket.accept()
    print(f"Received connection from {address}.")
    start_communicating(connection)

# Cette fonction sert à se connecter à un ordinateur qui a créé un serveur
# avec listen_for_peers
def connect_to_peer(ip: str, port: int):
    connection = socket.create_connection((ip, port),timeout=1)
    print(f"Created connection with peer {ip}:{port}")
    start_communicating(connection)

# Une fois la connection établie, les deux paires entrent dans cette fonction,
# qui gère les packets reçus.
def start_communicating(connection: socket.socket):
    # on demande que recv soit bloquant:
    # l'execution est en pause tant qu'aucun message n'est recu
    connection.setblocking(True)

    # On envoie notre clé publique à la paire pour qu'elle puisse nous envoyer des messages.
    send_key(connection, publicKey, protocol)

    key_received = False

    while True:
        try:
            header = connection.recv(3)

            # Si recv retourne 0 bytes, cela veut dire que la connection a été fermée.
            if len(header) == 0:
                print("Connection closed.")
                os._exit(0)

            # On vérifie que tous les octets du header ont bien été recus.
            assert len(header) == 3
            # extraction des données du header: deux bytes pour la taille et 1 pour le type.
            content_size = int.from_bytes(header[0:2])
            packet_type = int.from_bytes(header[2:3])
            # maintenant qu'on sait la longueur exacte du packet, on peut lire le contenu sur le socket.
            content = connection.recv(content_size)
            # on vérifie que tous les octets du contenu ont bien été recus.
            assert len(content) == content_size
        except AssertionError:
            print("Error: received incomplete or malformed packet. Exiting.")
            os._exit(0)
        else:
            if packet_type == PacketType.MESSAGE.value:
                receive_message(content)
            elif packet_type == PacketType.PUBKEY_SHARE.value and not key_received:
                receive_key(content, connection)
                # On note que la clé a été reçue pour ne pas appeler deux fois receive_key,
                # sinon deux treads seraient créés qui écouteraient stdin simultanément
                key_received = True

# Crypte et envoie un message
def send_message(sock: socket.socket, message: str, remotePublicKey: bytes):
    remoteKeySize = len(remotePublicKey)
    if protocol == KeyType.ELGAMAL:
        content = chiffrementElGamal(message, remotePublicKey, remoteKeySize)
    else:
        content = chiffrementRSA(message, remotePublicKey, remoteKeySize)
    length = len(content)
    # Création du paquet par concaténation de bytes
    # (2 bytes pour la longueur, 1 byte pour le type de packet, puis le contenu)
    packet = length.to_bytes(2) + PacketType.MESSAGE.byte() + content
    sock.send(packet)

# Décrypte et affiche un message reçu.
def receive_message(packetContent: bytes):
    if protocol == KeyType.ELGAMAL:
        msg = déchiffrementElGamal(packetContent, privateKey, KEY_SIZE)
    else:
        msg = dechiffrementRSA(packetContent, privateKey, KEY_SIZE)
    print("Message received:", msg)

def send_key(sock: socket.socket, key: bytes, keyType: KeyType):
    length = 1 + len(key)
    # Création du paquet par concaténation de bytes
    # (2 bytes pour la longueur, 1 byte pour le type de packet, puis le contenu)
    packet = length.to_bytes(2) \
            + PacketType.PUBKEY_SHARE.byte() \
            + keyType.byte() \
            + key
    sock.send(packet)

def receive_key(packetContent: bytes, connection: socket.socket):
    # Premier byte: type de clé (RSA = 1, ELGAMAL = 2)
    keyTypeByte = packetContent[:1]
    if keyTypeByte != protocol.byte():
        print("Error: received wrong key type. Exiting.")
        os._exit(0)

    # 2e byte: la clé
    remotePublicKey = packetContent[1:]
    remoteKeySize = len(packetContent) - 1
    print(f"Received public key from peer. Key size: {remoteKeySize}B.")
    print("You can now send messages to the peer.")

    # Une fois la clé reçue, on invoque read_stdin dans un thread
    # parallèle pour permettre à l'utilisateur d'écrire des messages.
    threading.Thread(target=read_stdin, args=(connection, remotePublicKey)).start()

# Cette fonction est executée quand l'utilisateur fait CTRL+C
def sigint_handler(_sig, _frame):
    print("Exiting.")
    os._exit(0)

def print_help():
    print("Syntax:")
    print(sys.argv[0], "rsa listen")
    print(sys.argv[0], "rsa connect ip:port")
    print(sys.argv[0], "elgamal listen")
    print(sys.argv[0], "elgamal connect ip:port")

# ============
# === CODE ===
# ============

# On dit à python d'appeler sigint_handler quand l'utilisateur fait CTRL+C
signal.signal(signal.SIGINT, sigint_handler)

# On fait l'action demandée par l'utilisateur, ou on affiche le message d'aide
# si les arguments sont mal formés.
# sys.argv[1] est le premier argument de ligne de commande
# sys.argv[2] est le deuxième.
if len(sys.argv) <= 2:
    print_help()
    exit(1)

if sys.argv[1].lower() == "rsa":
    protocol = KeyType.RSA
    privateKey = readRsaPrivateKey(KEY_SIZE,rsaPrivateKeyFile)
    publicKey = readRsaPublicKey(KEY_SIZE,rsaPublicKeyFile)
elif sys.argv[1].lower() == "eg" or sys.argv[1].lower() == "elgamal":
    protocol = KeyType.ELGAMAL
    privateKey = readEgKeyFromFile(egPrivateKeyFile, KEY_SIZE)
    publicKey = readEgKeyFromFile(egPublicKeyFile, KEY_SIZE)
else:
    print_help()
    exit(1)

if sys.argv[2] == "listen":
    listen_for_peers()
elif sys.argv[2] == "connect":
    try:
        addr_str = sys.argv[3]
        [ip,port] = addr_str.split(":")
        port = int(port)
    except:
        print_help()
    else:
        connect_to_peer(ip,port)
else:
    print_help()

