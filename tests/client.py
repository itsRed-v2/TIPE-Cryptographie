# Source - https://stackoverflow.com/a/18297623
# Posted by David, modified by community. See post 'Timeline' for change history
# Retrieved 2026-03-19, License - CC BY-SA 3.0

import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('172.20.30.5', 6008))
clientsocket.send('hello'.encode("utf-8"))
