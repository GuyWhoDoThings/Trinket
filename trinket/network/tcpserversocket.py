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
import logging
import sys
import socket
import threading
from trinket.network.network import Network
from trinket.network.protocol.packet import Packet, DecodedPacket
from trinket.utils.trinketlogger import TrinketLogger
from trinket.network.client import Client


class TCPServerSocket:

    def getserverid(self, addr):
        for serverid in self.CLIENTS:
            conn = self.CLIENTS[serverid]
            if conn.getpeername()[0] == addr:
                return conn
        return False

    def getinfo(self):
        pcount = 0
        for identifier in self.INFO:
            info = self.INFO[identifier]
            pcount += int(info["online"])
        return json.dumps({"protocol": Network.PROTOCOL, "version": '1.0.0', "players": int(pcount)})

    def listen(self):
        while True:
            try:
                conn, addr = self.s.accept()
                data = json.loads(conn.recv(Network.BUFFER).decode().strip())

                pckt = DecodedPacket(data)
                pwd = pckt.get("password")
                if pwd == self.PASSWORD:
                    pk = Packet()
                    pk.IDENTIFIER = Network.TYPE_PACKET_LOGIN
                    pk.DATA = True
                    pk.ERROR = Network.TYPE_ERROR_EMPTY
                    conn.send(pk.encode())
                    self.CLIENTS[data["serverId"]] = Client(conn, data["serverId"], self)
                    self.INFO[str(pckt.get("serverId"))] = {"online": 0}
                    TrinketLogger.debug("Connection from " + str(addr) + " with ID " + str(pckt.get("serverId")) + " accepted")
                    pk = Packet()
                    pk.IDENTIFIER = Network.TYPE_PACKET_DUMMY
                    conn.send(pk.encode())
                    continue
                else:
                    pk = Packet()
                    pk.IDENTIFIER = Network.TYPE_PACKET_LOGIN
                    pk.DATA = False
                    pk.ERROR = Network.TYPE_ERROR_INVALID_PASSWORD
                    conn.send(pk.encode())
                    TrinketLogger.debug("Connection from " + str(addr) + " refused, Invalid Password")
                    continue
            except (KeyboardInterrupt, SystemExit):
                return

    def __init__(self, host, port, logger: logging.Logger, password):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = host
        self.PORT = port
        self.PASSWORD = password
        self.CLIENTS = dict()
        self.INFO = dict()
        self.LOGGER = logger
        try:
            self.s.bind((self.HOST, self.PORT))
        except self.s.error:
            TrinketLogger.error("FAILED TO BIND TO PORT! Perhaps another server is running on the port?")
            sys.exit()
        finally:
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.listen(5)
            TrinketLogger.info("Trinket running on " + self.HOST + ":" + str(self.PORT))
            threading.Thread(target=self.listen, daemon=True).start()
