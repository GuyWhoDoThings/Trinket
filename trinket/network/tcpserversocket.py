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
import os
import pprint
import sys
import socket
import threading
import time

from trinket.network.network import Network
from trinket.network.protocol.packet import Packet, DecodedPacket
from trinket.utils.trinketlogger import TrinketLogger

class TCPServerSocket():

    def getLogger(self):
        return self.LOGGER

    def clientlisten(self):
        while self.ENABLED:
            try:
                try:
                    for serverId in self.CLIENTS:
                        try:
                            c = self.CLIENTS[serverId]
                            j = c.recv(1024)
                            if not j:
                                continue
                            if j == "":
                                continue
                            pckt = DecodedPacket(json.loads(j.strip()))
                            if pckt.getID() == Network.TYPE_PACKET_DUMMY:
                                pk = Packet()
                                pk.IDENTIFIER = Network.TYPE_PACKET_DUMMY
                                c.send(pk.encode())
                                del pk
                                time.sleep(1)
                            elif pckt.getID() == Network.TYPE_PACKET_DISCONNECT:
                                del self.CLIENTS[serverId]
                                TrinketLogger.debug("Client " + str(c.getpeername()) + " disconnected")
                            elif pckt.getID() == Network.TYPE_PACKET_DATA_REQUEST:
                                pk = Packet()
                                pk.IDENTIFIER = Network.TYPE_PACKET_DATA_SEND
                                if pckt.get("data")["type"] == Network.TYPE_DATA_CLIENTLIST:
                                    pk.DATA = self.getClientList()
                                else:
                                    continue
                                c.send(pk.encode())
                            elif pckt.getID() == Network.TYPE_PACKET_DATA_SEND:
                                if pckt.get("data") == Network.TYPE_DATA_CHAT:
                                    pk = Packet()
                                    pk.IDENTIFIER = Network.TYPE_PACKET_DATA_SEND
                                    pk.CHAT = pckt.get("chat")
                                    for sid in self.CLIENTS:
                                        cl = self.CLIENTS[sid]
                                        if cl == c:
                                            continue
                                        c.send(pk.encode())
                            elif pckt.getID() ==  Network.TYPE_PACKET_COMMAND_EXECUTE:
                                try:
                                    data = pckt.get("data")
                                    server = self.CLIENTS[data["id"]]
                                    pk = Packet()
                                    pk.IDENTIFIER = Network.TYPE_PACKET_COMMAND_EXECUTE
                                    pk.DATA = data["command"]
                                    server.send(pk.encode())
                                except Exception:
                                    continue
                        except socket.error:
                            continue
                except RuntimeError:
                    continue
            except (KeyboardInterrupt, SystemExit):
                return


    def setEnabled(self, bool):
        self.ENABLED = bool

    def getClientList(self):
        cl = dict()
        for id in self.CLIENTS:
            sk = self.CLIENTS[id]
            cl[id] = [id, sk.getpeername()]
        return str(cl)

    def listen(self):
        while self.ENABLED:
            try:
                conn, addr = self.s.accept()
                data = json.loads(conn.recv(1024).strip())
                pckt = DecodedPacket(data)
                if pckt.getID() == Network.TYPE_PACKET_LOGIN:
                    pwd = pckt.get('password')
                    if data["serverId"] in self.CLIENTS:
                        pk = Packet()
                        pk.IDENTIFIER = Network.TYPE_PACKET_LOGIN
                        pk.DATA = False
                        pk.ERROR = Network.TYPE_ERROR_SERVER_ID
                        conn.send(pk.encode())
                        TrinketLogger.error("Connection " + str(addr) + " attempted to login with registered serverID")
                        continue
                    if pwd == self.PASSWORD:
                        pk = Packet()
                        pk.IDENTIFIER = Network.TYPE_PACKET_LOGIN
                        pk.DATA = True
                        pk.ERROR = Network.TYPE_ERROR_EMPTY
                        conn.send(pk.encode())
                        self.CLIENTS[data["serverId"]] = conn
                        TrinketLogger.debug("Connection from " + str(addr) + " with ID " + str(pckt.get("serverId")) + " accepted")
                        pk = Packet()
                        pk.IDENTIFIER = Network.TYPE_PACKET_DUMMY
                        pk.ERROR = Network.TYPE_ERROR_EMPTY
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

    def __init__(self, HOST, PORT, logger: logging.Logger, password):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = HOST
        self.PORT = PORT
        self.PASSWORD = password
        self.CLIENTS = dict()
        self.LOGGER = logger
        self.ENABLED = True
        try:
            self.s.bind((self.HOST, self.PORT))
        except Exception as e:
            TrinketLogger.error("FAILED TO BIND TO PORT! Perhaps another server is running on the port?")
            sys.exit()
        finally:
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.listen(5)
            TrinketLogger.info("Trinket running on " + self.HOST + ":" + str(self.PORT))
            threading.Thread(target=self.listen, daemon=True).start()
            threading.Thread(target=self.clientlisten, daemon=True).start()

    def stop(self):
        for sid in self.CLIENTS:
            try:
                c = self.CLIENTS[sid]
                pk = Packet()
                pk.IDENTIFIER = Network.TYPE_PACKET_DISCONNECT
                pk.REASON = Network.TYPE_DISCONNECT_FORCED
                c.send(pk.encode())
            except Exception as e:
                continue