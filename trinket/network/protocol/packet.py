import json
from trinket.network.network import Network
class Packet():

    def __init__(self):
        self.IDENTIFIER = 0x001
        self.ERROR = Network.TYPE_ERROR_EMPTY
        self.PASSWORD = ""
        self.DATA = {}
        self.REASON = ""
        self.CHAT = ""
        self.SELECTION = 10001101
        self.PROTOCOL = Network.PROTOCOL

    def encode(self):
        arr = {"id": self.IDENTIFIER, "error": self.ERROR, "password": self.PASSWORD, "data": self.DATA, "reason": self.REASON, "chat": self.CHAT, "selection": self.SELECTION, "protocol": self.PROTOCOL}
        return json.dumps(arr).ljust(1024, ' ').encode()

class DecodedPacket():

    def __init__(self, data):
        self.DATA = data
        self.IDENTIFIER = data["id"]

    def getID(self):
        return self.IDENTIFIER

    def get(self, index):
        return self.DATA[index]

    def getAll(self):
        return self.DATA

