from trinket.network.network import Network
from trinket.network.protocol.packet import Packet, DecodedPacket
from trinket.utils.trinketlogger import TrinketLogger
import json
class ClientHandle():

    def __init__(self, logger):
        self.CLIENTS = {}
        self.LOGGER = logger

    def listen(self):
        for addr in self.CLIENTS:
            c = self.CLIENTS[addr]
            try:
                js = c.recv(1024)
                if not js:
                    continue
                if js == "" or js == "NULL":
                    continue

                pckt = DecodedPacket(json.loads(js.strip()))
                if pckt.getID() == Network.TYPE_PACKET_DUMMY:
                    pk = Packet()
                    pk.IDENTIFIER = Network.TYPE_PACKET_DUMMY
                    self.SOCKET.direct()
            except c.error:
                self.LOGGER.error(addr + " unexpectedly disconnected")
                del self.CLIENTS[addr]
