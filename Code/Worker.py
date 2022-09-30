import socket
import Packets

LISTEN_PORT = 6000

listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
listener.bind(("", LISTEN_PORT))

while True:
	data, addr = listener.recvfrom(512)

	packet = Packets.decodePacket(data)
	if packet == None:
		continue

	if packet.type == Packets.typeToNum["FileRequest"]:
		print("Recieving request for {} from load balancer.".format(packet.filename, addr[0]))
