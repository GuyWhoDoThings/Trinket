import json
class Packet():

    def __init__(self):
        self.IDENTIFIER = 0x001
        self.ERROR = ""
        self.PASSWORD = ""
        self.DATA = {}
        self.REASON = ""
        self.CHAT = ""
        self.SELECTION = 10001101
        self.PROTOCOL = '1.0.0'

    def encode(self):
        arr = {"id": self.IDENTIFIER, "error": self.ERROR, "password": self.PASSWORD, "data": self.DATA, "reason": self.REASON, "chat": self.CHAT, "selection": self.SELECTION, "protocol": self.PROTOCOL}
        return json.dumps(arr).encode()

class DecodedPacket():

    def __init__(self, data):
        self.IDENTIFIER = data["id"]
        self.ARRAY = data

    def getID(self):
        return self.IDENTIFIER

    def get(self, index):
        return self.ARRAY[index]
