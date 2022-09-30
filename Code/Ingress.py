import socket
import Packets

PORT = 6000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))

#availableWorkers = {"172.41.0.2", "172.17.0.3", "172.17.0.4"}
availableWorkers = {"172.41.0.2"}
workerToClient = {}
clientToWorker = {}

while True:
	data, addr = sock.recvfrom(512)

	packet = Packets.decodePacket(data)
	if packet == None:
		continue

	if packet.type == Packets.typeToNum["FileRequest"]:
		print("Recieving request for {} from {}".format(packet.filename, addr[0]))

		# Assign worker.
		currentWorker = availableWorkers.pop()
		workerToClient[currentWorker] = addr[0]
		clientToWorker[addr[0]] = currentWorker

		# Send request to worker.
		sock.sendto(data, (currentWorker, PORT))

	elif packet.type == Packets.typeToNum["FileContents"]:
		print("Recieving file contents from worker {}".format(addr[0]))

		# Get client handled by worker.
		client = workerToClient[currentWorker]
		print("Bound for client {}".format(client))

		# Send data to client.
		sock.sendto(data, (client, PORT))

	elif packet.type == Packets.typeToNum["EndChunk"]:
		print("Recieving end chunk packet from worker {}".format(addr[0]))

		# Get client handled by worker.
		client = workerToClient[currentWorker]
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
