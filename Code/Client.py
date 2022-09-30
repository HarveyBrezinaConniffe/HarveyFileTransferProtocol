import socket
import Packets

LOADBALANCER_IP = "172.40.0.2"
PORT = 6000

PACKETS_PER_CHUNK = 32

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))

filename = input("What file do you want? ")

print("Sending request!")
requestPacket = Packets.FileRequestPacket(filename)
sock.sendto(requestPacket.encode(), (LOADBALANCER_IP, PORT))

fileRecieved = False
#fileHandler = open("../Downloads/"+filename, 'wb')
chunkbuffer = {}

while not fileRecieved:
	data, addr = sock.recvfrom(512)

	packet = Packets.decodePacket(data)
	if packet == None:
		continue

	if packet.type == Packets.typeToNum["FileContents"]:
		print("Recieving file contents from ingress. Packet {} out of {} in chunk."
			.format(packet.position, PACKETS_PER_CHUNK))
		chunkbuffer[packet.position] = packet.data	

	if packet.type == Packets.typeToNum["EndChunk"]:
		print("End chunk.")
