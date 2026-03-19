import socket
import select
import sys

HOST_ADDRESS = ('192.168.1.37', 6008)
REMOTE_ADDRESS = ('192.168.1.188', 6008)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(HOST_ADDRESS)
serverSocket.listen(5) # become a server socket, maximum 5 connections

read_list = [serverSocket, sys.stdin]
while True:
    readable, _, _ = select.select(read_list, [], [], 1)
    for stream in readable:
        if stream is serverSocket:
            clientSocket, address = serverSocket.accept()
            buf = clientSocket.recv(64)
            if len(buf) > 0:
                print(buf)
        elif stream is sys.stdin:
            line = sys.stdin.readline().strip()
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect(REMOTE_ADDRESS)
            clientSocket.send(line.encode("utf-8"))
            clientSocket.close()
