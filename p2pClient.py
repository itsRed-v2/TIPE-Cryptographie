import socket
import threading
from elgamal import encrypt, decrypt, numberToText, textToNumber

publicKey = 98480326830221655152937220702365073953858155354977805770798587194533294300529
privateKey = 60120861764318186023758850434217284955860885101117782415664692375684178754848

HOST_ADDRESS = ('172.20.10.3', 6008)
REMOTE_ADDRESS = ('172.20.10.14', 6008)

def read_stdin():
    while True:
        msg = input().strip()
        msgNumber = textToNumber(msg)
        c1, c2 = encrypt(msgNumber, publicKey)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect(REMOTE_ADDRESS)
        clientSocket.send(c1.to_bytes(32))
        clientSocket.send(c2.to_bytes(32))
        clientSocket.close()

def listen_socket():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(HOST_ADDRESS)
    serverSocket.listen(5) # become a server socket, maximum 5 connections
    while True:
        connection, address = serverSocket.accept()
        c1 = int.from_bytes(connection.recv(32))
        c2 = int.from_bytes(connection.recv(32))
        msgNumber = decrypt((c1, c2), privateKey)
        msg = numberToText(msgNumber)
        print(msg)

threading.Thread(target=read_stdin).start()
threading.Thread(target=listen_socket).start()