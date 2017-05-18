"""
$$$$$$$$\        $$\           $$\                  $$\
\__$$  __|       \__|          $$ |                 $$ |
   $$ | $$$$$$\  $$\ $$$$$$$\  $$ |  $$\  $$$$$$\ $$$$$$\
   $$ |$$  __$$\ $$ |$$  __$$\ $$ | $$  |$$  __$$\\_$$  _|
   $$ |$$ |  \__|$$ |$$ |  $$ |$$$$$$  / $$$$$$$$ | $$ |
   $$ |$$ |      $$ |$$ |  $$ |$$  _$$<  $$   ____| $$ |$$\
   $$ |$$ |      $$ |$$ |  $$ |$$ | \$$\ \$$$$$$$\  \$$$$  |
   \__|\__|      \__|\__|  \__|\__|  \__| \_______|  \____/

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU Lesser General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
"""
import json
from trinket.network.network import Network
class Packet():

    def __init__(self):
        self.IDENTIFIER = 0x001
        self.ERROR = Network.TYPE_ERROR_EMPTY
        self.PASSWORD = Network.TYPE_STRING_EMPTY
        self.DATA = Network.TYPE_DATA_EMPTY
        self.REASON = Network.TYPE_DATA_EMPTY
        self.CHAT = Network.TYPE_STRING_EMPTY
        self.TO = False
        self.SELECTION = Network.TYPE_SELECTION_PLAYERS_ALL
        self.PROTOCOL = Network.PROTOCOL

    def encode(self):
        arr = {"id": self.IDENTIFIER, "error": self.ERROR, "password": self.PASSWORD, "data": self.DATA, "to": self.TO, "reason": self.REASON, "chat": self.CHAT, "selection": self.SELECTION, "protocol": self.PROTOCOL}
        return json.dumps(arr).ljust(1024, ' ').encode()

class DecodedPacket():

    def __init__(self, data):
        self.DATA = data
        self.IDENTIFIER = data["id"]

    def getID(self):
        return self.IDENTIFIER

    def get(self, index):
        try:
            k = self.DATA[index]
            return k
        except KeyError:
            return ""

