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