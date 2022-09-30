import socket
import Packets

LOADBALANCER_IP = "172.41.0.5"

PORT = 6000
BYTES_PER_PACKET = 512
PACKETS_PER_CHUNK = 32

FILE_DIRECTORY = "../Files/"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))

while True:
	data, addr = sock.recvfrom(512)

	packet = Packets.decodePacket(data)
	if packet == None:
		continue

	if packet.type == Packets.typeToNum["FileRequest"]:
		print("Recieving request for {} from load balancer.".format(packet.filename, addr[0]))

		packetsSinceAck = 0
		with open(FILE_DIRECTORY+packet.filename, "rb") as f:
			data = f.read(BYTES_PER_PACKET)	
			while data != "" and packetsSinceAck < PACKETS_PER_CHUNK:
				dataPacket = Packets.FileContentsPacket(packetsSinceAck, data)
				sock.sendto(dataPacket.encode(), (LOADBALANCER_IP, PORT))
				packetsSinceAck += 1

