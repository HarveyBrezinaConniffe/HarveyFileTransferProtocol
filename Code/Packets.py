typeToNum = {"FileRequest": 0, "FileContents": 1}

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

class FileContentsPacket():
	def __init__(self, position, data):
		self.type = typeToNum["FileContents"]
		self.position = position
		self.data = data
	
	def encode(self):
		# Store type of packet in first byte
		typeByte = (self.type).to_bytes(1, byteorder='big')
		# Store position in second byte
		positionByte = (self.position).to_bytes(1, byteorder='big')
		return typeByte+positionByte+self.data

	@classmethod
	def decode(cls, packet):
		# Position in second byte
		position = packet[1]
		# Rest is file data
		data = packet[2:]
		return cls(position, data)

numToClass = {0: FileRequestPacket, 1: FileContentsPacket}

def decodePacket(packet):
	packetType = packet[0]
	if packetType not in numToClass:
		return None
	return numToClass[packetType].decode(packet)
