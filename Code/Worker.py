import socket
import Packets
import time

LOADBALANCER_IP = "172.41.0.5"

PORT = 6000
BYTES_PER_PACKET = 1024
PACKETS_PER_CHUNK = 32

FILE_DIRECTORY = "../Files/"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))

broadcastSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcastSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcastInterval = 10
lastBroadcast = 0

fileHandler = None
bytesSent = 0

def sendChunk(f):
	global bytesSent
	packetsSinceAck = 0
	data = f.read(BYTES_PER_PACKET)	
	while data != "" and packetsSinceAck < PACKETS_PER_CHUNK:
		dataPacket = Packets.FileContentsPacket(packetsSinceAck, data)
		sock.sendto(dataPacket.encode(), (LOADBALANCER_IP, PORT))
		packetsSinceAck += 1
		data = f.read(BYTES_PER_PACKET)	

	bytesSent += BYTES_PER_PACKET*PACKETS_PER_CHUNK
	if bytesSent%1024 == 0:
		print("{} bytes sent.".format(bytesSent))
	# End of chunk
	endOfFile = data==b''
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

	timeSinceBroadcast = time.time()-lastBroadcast
	if timeSinceBroadcast >= broadcastInterval:
		discoveryPacket = Packets.DiscoveryPacket(Packets.nodeTypes.Worker)
		broadcastSock.sendto(discoveryPacket.encode(), ("255.255.255.255", PORT))
		lastBroadcast = time.time()
