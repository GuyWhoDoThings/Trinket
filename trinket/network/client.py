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
from trinket.network.network import Network
from trinket.network.protocol.packet import Packet, DecodedPacket
from trinket.utils.trinketlogger import TrinketLogger
import json
import threading


class Client:

    def __init__(self, socket, server, tcp):
        self.SOCKET = socket
        self.SERVER = server
        self.CONNECTED = True
        self.TCP = tcp
        threading.Thread(target=self.listen, daemon=True).start()

    def send(self, packet):
        try:
            self.SOCKET.send(packet)
        except Exception as e:
            self.kill()
            TrinketLogger.error(str(e))

    def listen(self):
        while True:
            pk = DecodedPacket(json.loads(self.SOCKET.recv(Network.BUFFER).decode().strip()))
            if pk.get("protocol") != Network.PROTOCOL:
                TrinketLogger.error("Received packet with identifier unknown protocol")
                pk = Packet()
                pk.IDENTIFIER = Network.TYPE_PACKET_DISCONNECT
                self.send(pk.encode())
            elif pk.getID() == Network.TYPE_PACKET_DISCONNECT:
                TrinketLogger.debug("Client " + str(self.SOCKET.getpeername()) + " disconnected")
                return
            elif pk.getID() == Network.TYPE_PACKET_DUMMY:
                pk = Packet()
                pk.IDENTIFIER = Network.TYPE_PACKET_DUMMY
                pk.DATA = self.TCP.getinfo()
                self.send(pk.encode())
        return

    def kill(self):
        pk = Packet()
        pk.IDENTIFIER = Network.TYPE_PACKET_DISCONNECT
        self.send(pk.encode())
        return
