import socket
import threading
from elgamal import encrypt, decrypt, numberToText, textToNumber, readKeyFromFile
from enum import Enum
import sys
import os
import signal

# =================
# === CONSTANTS ===
# =================

HOST_ADDRESS = ('localhost', 6008)
REMOTE_ADDRESS = ('localhost', 6008)

KEY_SIZE = 256

hostPrivateKey = readKeyFromFile("hostPrivate.key", KEY_SIZE)
hostPublicKey = readKeyFromFile("hostPublic.key", KEY_SIZE)

# ========================
# === GLOBAL VARIABLES ===
# ========================

remotePublicKey: int | None = None;
remoteKeySize: int | None = None;

# =====================================
# === CLASS AND FUNCTION DEFINITION ===
# =====================================

# PACKET LAYOUT: | content length (2B) | packet type (1B) | content |

class PacketType(Enum):
    MESSAGE = 1
    PUBKEY_SHARE = 2

    def byte(self):
        return self.value.to_bytes(1)

def send_message(sock: socket.socket, message: str):
    if remotePublicKey == None or remoteKeySize == None:
        print("Error: Cannot send message to peer, public key not yet received.")
        return

    msgNumber = textToNumber(message, remoteKeySize)
    c1, c2 = encrypt(msgNumber, remotePublicKey, remoteKeySize)
    content = c1.to_bytes(remoteKeySize) + c2.to_bytes(remoteKeySize)
    length = len(content)
    packet = length.to_bytes(2) + PacketType.MESSAGE.byte() + content
    sock.send(packet)

def send_key(sock: socket.socket, key: bytes):
    length = len(key)
    packet = length.to_bytes(2) + PacketType.PUBKEY_SHARE.byte() + key
    sock.send(packet)

def read_stdin(connection: socket.socket):
    while True:
        msg = input().strip()
        send_message(connection, msg)

def listen_for_peers():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(HOST_ADDRESS)
    serverSocket.listen() # become a server socket, maximum 5 connections
    print("Listening for incoming connections...")
    connection, address = serverSocket.accept()
    print(f"Received connection from {address}.")
    start_communicating(connection)

def connect_to_peer():
    connection = socket.create_connection(REMOTE_ADDRESS)
    print(f"Engaged connection with peer {REMOTE_ADDRESS}")
    start_communicating(connection)

def start_communicating(connection: socket.socket):
    connection.setblocking(True)

    send_key(connection, hostPublicKey.to_bytes(KEY_SIZE))

    threading.Thread(target=read_stdin, args=[connection]).start()

    while True:
        header = connection.recv(3)
        if len(header) == 0:
            print("Connection closed.")
            os._exit(0)
        assert len(header) == 3
        content_size = int.from_bytes(header[0:2])
        packet_type = int.from_bytes(header[2:3])
        content = connection.recv(content_size)
        assert len(content) == content_size

        if packet_type == PacketType.MESSAGE.value:
            receive_message(content)
        elif packet_type == PacketType.PUBKEY_SHARE.value:
            receive_key(content)

def receive_message(packetContent: bytes):
    c1 = int.from_bytes(packetContent[0:KEY_SIZE])
    c2 = int.from_bytes(packetContent[KEY_SIZE:2*KEY_SIZE])
    msgNumber = decrypt((c1, c2), hostPrivateKey, KEY_SIZE)
    msg = numberToText(msgNumber, KEY_SIZE)
    print("Message received:", msg)

def receive_key(packetContent: bytes):
    global remotePublicKey, remoteKeySize
    remoteKeySize = len(packetContent)
    remotePublicKey = int.from_bytes(packetContent)
    print(f"Received public key from peer. Key size: {remoteKeySize}B.")

def sigint_handler(_sig, _frame):
    print("Exiting.")
    os._exit(0)

# ===================
# === ACTUAL CODE ===
# ===================

signal.signal(signal.SIGINT, sigint_handler)

assert len(sys.argv) == 2

if sys.argv[1] == "listen":
    listen_for_peers()
elif sys.argv[1] == "connect":
    connect_to_peer()
else:
    print(f"Unknown argument: {sys.argv[1]}")

