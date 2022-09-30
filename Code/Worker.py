import socket
import Packets

LOADBALANCER_IP = "172.41.0.5"

PORT = 6000
BYTES_PER_PACKET = 512
PACKETS_PER_CHUNK = 32

FILE_DIRECTORY = "../Files/"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))

fileHandler = None

def sendChunk(f):
	packetsSinceAck = 0
	data = f.read(BYTES_PER_PACKET)	
	while data != "" and packetsSinceAck < PACKETS_PER_CHUNK:
		dataPacket = Packets.FileContentsPacket(packetsSinceAck, data)
		sock.sendto(dataPacket.encode(), (LOADBALANCER_IP, PORT))
		packetsSinceAck += 1
		data = f.read(BYTES_PER_PACKET)	

	# End of chunk
	endOfFile = data==""
	if endOfFile:
		f.close()
	endChunkPacket = Packets.EndChunkPacket(endOfFile)
	sock.sendto(endChunkPacket.encode(), (LOADBALANCER_IP, PORT))

while True:
	data, addr = sock.recvfrom(512)

	packet = Packets.decodePacket(data)
	if packet == None:
		continue

	if packet.type == Packets.typeToNum["FileRequest"]:
		print("Recieving request for {} from load balancer.".format(packet.filename, addr[0]))
		fileHandler = open(FILE_DIRECTORY+packet.filename, "rb")
		# Send first chunk
		sendChunk(fileHandler)

	if packet.type == Packets.typeToNum["AckChunk"]:
		print("Ack for last chunk. Sending next chunk.")
		sendChunk(fileHandler)
