import socket

LISTEN_PORT = 6000

listenSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
listenSock.bind(("", LISTEN_PORT))

while True:
    data, addr = listenSock.recvfrom(1024) # buffer size is 1024 bytes
    print("received message: %s" % data)
    print(addr)
