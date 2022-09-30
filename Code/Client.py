import socket
import Packets

LOADBALANCER_IP = "172.40.0.2"
PORT = 6000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))

filename = input("What file do you want? ")

print("Sending request!")
requestPacket = Packets.FileRequestPacket(filename)
sock.sendto(requestPacket.encode(), (LOADBALANCER_IP, PORT))

