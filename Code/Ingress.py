import socket
import Packets

PORT = 6000
DISCOVERYPORT = 6001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))
sock.settimeout(3)

broadcastSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcastSock.bind(("172.41.255.255", DISCOVERYPORT))
broadcastSock.settimeout(0.0)

availableWorkers = set({})
workerToClient = {}
clientToWorker = {}

def recievePacket(data, addr):
	packet = Packets.decodePacket(data)
	if packet == None:
		return

	if packet.type == Packets.typeToNum["FileRequest"]:
		print("Recieving request for {} from {}".format(packet.filename, addr[0]))

		# Assign worker.
		currentWorker = availableWorkers.pop()
		workerToClient[currentWorker] = addr[0]
		clientToWorker[addr[0]] = currentWorker
		print("Assigning worker {} to client {}".format(currentWorker, addr[0]))

		# Send request to worker.
		sock.sendto(data, (currentWorker, PORT))

	elif packet.type == Packets.typeToNum["FileContents"]:
		print("Recieving file contents from worker {}".format(addr[0]))

		# Get client handled by worker.
		client = workerToClient[addr[0]]
		print("Bound for client {}".format(client))

		# Send data to client.
		sock.sendto(data, (client, PORT))

	elif packet.type == Packets.typeToNum["EndChunk"]:
		print("Recieving end chunk packet from worker {}".format(addr[0]))

		# Get client handled by worker.
		client = workerToClient[addr[0]]
		print("Bound for client {}".format(client))

		# Send data to client.
		sock.sendto(data, (client, PORT))

	elif packet.type == Packets.typeToNum["AckChunk"]:
		print("Chunk ack from {}".format(addr[0]))

		# Get worker handled by client.
		worker = clientToWorker[addr[0]]
		print("Bound for worker {}".format(worker))

		# Send data to worker.
		sock.sendto(data, (worker, PORT))

def recieveBroadcast(data, addr):
	packet = Packets.decodePacket(data)

	if packet == None:
		return

	if packet.type == Packets.typeToNum["Discovery"]:
		workerIP = addr[0]
		if workerIP not in availableWorkers:
			print("New worker discovered!")
			availableWorkers.add(workerIP)

while True:
	try:
		data, addr = sock.recvfrom(512)
	except:
		pass
	else:
		recievePacket(data, addr)
		
	try:
		data, addr = broadcastSock.recvfrom(512)
	except:
		pass
	else:
		recieveBroadcast(data, addr)

