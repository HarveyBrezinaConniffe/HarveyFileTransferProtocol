typeToNum = {"FileRequest": 0}

class FileRequestPacket():
	def __init__(self, filename):
		self.type = typeToNum["FileRequest"]
		self.filename = filename
	
	def encode(self):
		# Store type of packet in first byte
		typeByte = (self.type).to_bytes(1, byteorder='big')
		# Convert filename to byte
		fileNameBytes = self.filename.encode("ascii")
		# Return packet bytes
		return typeByte+fileNameBytes

	@classmethod
	def decode(cls, packet):
		# Everything after type byte is filename	
		filename = packet[1:].decode("ascii")	
		return cls(filename)

numToClass = {0: FileRequestPacket}

def decodePacket(packet):
	packetType = packet[0]
	return numToClass[packetType].decode(packet)
