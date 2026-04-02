import socket
import threading
from elgamal import encrypt, decrypt, numberToText, textToNumber, readKeyFromFile, KEY_SIZE

HOST_ADDRESS = ('172.20.31.80', 6008)
REMOTE_ADDRESS = ('172.20.30.51', 6008)

hostPrivateKey = readKeyFromFile("hostPrivate.key")
remotePublicKey = readKeyFromFile("remotePublic.key")

def read_stdin():
    while True:
        msg = input().strip()
        msgNumber = textToNumber(msg)
        c1, c2 = encrypt(msgNumber, remotePublicKey)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect(REMOTE_ADDRESS)
        clientSocket.send(c1.to_bytes(KEY_SIZE))
        clientSocket.send(c2.to_bytes(KEY_SIZE))
        clientSocket.close()

def listen_socket():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(HOST_ADDRESS)
    serverSocket.listen(5) # become a server socket, maximum 5 connections
    while True:
        connection, address = serverSocket.accept()
        c1 = int.from_bytes(connection.recv(KEY_SIZE))
        c2 = int.from_bytes(connection.recv(KEY_SIZE))
        msgNumber = decrypt((c1, c2), hostPrivateKey)
        msg = numberToText(msgNumber)
        print(msg)

threading.Thread(target=read_stdin).start()
threading.Thread(target=listen_socket).start()