import socket
import Packets
import time

LOADBALANCER_IP = "172.41.0.5"

PORT = 6000
DISCOVERYPORT = 6001

BYTES_PER_PACKET = 1024
PACKETS_PER_CHUNK = 32

FILE_DIRECTORY = "../Files/"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))
sock.settimeout(3)

broadcastSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcastSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcastInterval = 10
lastBroadcast = 0

fileHandler = None
bytesSent = 0

currentPackets = {}
lastChunkEnd = False

def sendChunk(f):
	global bytesSent, currentPackets, lastChunkEnd
	packetsSinceAck = 0
	data = f.read(BYTES_PER_PACKET)	

	currentPackets = {}
	
	while data != "" and packetsSinceAck < PACKETS_PER_CHUNK:
		dataPacket = Packets.FileContentsPacket(packetsSinceAck, data)
		currentPackets[packetsSinceAck] = dataPacket
		data = f.read(BYTES_PER_PACKET)	
		packetsSinceAck += 1

	for packet in currentPackets:
		sock.sendto(currentPackets[packet].encode(), (LOADBALANCER_IP, PORT))

	bytesSent += BYTES_PER_PACKET*PACKETS_PER_CHUNK
	if bytesSent%1024 == 0:
		print("{} bytes sent.".format(bytesSent))
	# End of chunk
	endOfFile = data==b''
	lastChunkEnd = endOfFile
	if endOfFile:
		f.close()
	endChunkPacket = Packets.EndChunkPacket(endOfFile)
	sock.sendto(endChunkPacket.encode(), (LOADBALANCER_IP, PORT))

def resendChunk(missingPackets):
	for packet in missingPackets:
		sock.sendto(currentPackets[packet].encode(), (LOADBALANCER_IP, PORT))		
	endChunkPacket = Packets.EndChunkPacket(lastChunkEnd)
	sock.sendto(endChunkPacket.encode(), (LOADBALANCER_IP, PORT))

def recievePacket(data, addr):
	global fileHandler
	packet = Packets.decodePacket(data)
	if packet == None:
		return

	if packet.type == Packets.typeToNum["FileRequest"]:
		print("Recieving request for {} from load balancer.".format(packet.filename, addr[0]))
		fileHandler = open(FILE_DIRECTORY+packet.filename, "rb")
		# Send first chunk
		sendChunk(fileHandler)

	if packet.type == Packets.typeToNum["AckChunk"]:
		print("Ack for last chunk.")
		if len(packet.missingPackets) > 0:
			print("Client requesting resend of packets {}".format(packet.missingPackets))
			resendChunk(packet.missingPackets)
		else:
			print("Sending next packet.")
			sendChunk(fileHandler)

while True:
	try:
		data, addr = sock.recvfrom(512)
	except:
		pass
	else:
		recievePacket(data, addr)

	timeSinceBroadcast = time.time()-lastBroadcast
	if timeSinceBroadcast >= broadcastInterval:
		discoveryPacket = Packets.DiscoveryPacket(Packets.nodeTypes["Worker"])
		broadcastSock.sendto(discoveryPacket.encode(), ("172.41.255.255", DISCOVERYPORT))
		lastBroadcast = time.time()
