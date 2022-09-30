import socket
import Packets

PORT = 6000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))

while True:
	data, addr = sock.recvfrom(512)

	packet = Packets.decodePacket(data)
	if packet == None:
		continue

	if packet.type == Packets.typeToNum["FileRequest"]:
		print("Recieving request for {} from load balancer.".format(packet.filename, addr[0]))
