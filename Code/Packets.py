typeToNum = {"FileRequest": 0, "FileContents": 1, "EndChunk": 2, "AckChunk": 3, "DiscoveryPacket": 4}
nodeTypes = {"Worker": 0}

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

class EndChunkPacket():
	def __init__(self, endOfFile=False):
		self.type = typeToNum["EndChunk"]
		self.endOfFile = endOfFile
	
	def encode(self):
		# Store type of packet in first byte
		typeByte = (self.type).to_bytes(1, byteorder='big')
		endOfFileByte = int(self.endOfFile).to_bytes(1, byteorder='big')
		return typeByte+endOfFileByte

	@classmethod
	def decode(cls, packet):
		endOfFile = packet[1] == 1
		return cls(endOfFile)

class AckChunkPacket():
	def __init__(self):
		self.type = typeToNum["AckChunk"]

	def encode(self):
		typeByte = (self.type).to_bytes(1, byteorder='big')
		return typeByte

	@classmethod
	def decode(cls, packet):
		return cls()

class DiscoveryPacket():
	def __init__(self, nodeType):
		self.type = typeToNum["DiscoveryPacket"]
		self.nodeType = nodeTypes[nodeType]

	def encode(self):
		typeByte = (self.type).to_bytes(1, byteorder='big')
		nodeTypeByte = (self.nodeType).to_bytes(1, byteorder='big')
		return typeByte+nodeTypeByte

	@classmethod
	def decode(cls, packet):
		return cls(packet[1])

numToClass = {0: FileRequestPacket, 1: FileContentsPacket, 2: EndChunkPacket, 3: AckChunkPacket, 4: DiscoveryPacket}

def decodePacket(packet):
	packetType = packet[0]
	if packetType not in numToClass:
		return None
	return numToClass[packetType].decode(packet)
