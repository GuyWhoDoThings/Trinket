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
import time
from trinket.network.network import Network
from trinket.network.protocol.packet import Packet, DecodedPacket
from trinket.utils.trinketlogger import TrinketLogger


class TCPServerSocket():

    def getClientDataAll(self):
        array = list()
        for c in self.CLIENTS:
            array.append(c)
        return array

    def getClientList(self):
        array = dict()
        for c in self.CLIENTS:
            array[c] = self.INFO[c]
        return array

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
                            if len(j) != 1024:
                                continue
                            pckt = DecodedPacket(json.loads(j.decode().strip()))
                            if pckt.get("protocol") != Network.PROTOCOL:
                                pk = Packet()
                                pk.IDENTIFIER = Network.TYPE_PACKET_DISCONNECT
                                c.send(pk.encode())
                                TrinketLogger.debug("Received packet from " + str(c.getpeername()) + " with unknown protocol")
                            self.LAST_PACKET[str(serverId)] = time.time()
                            if pckt.getID() == Network.TYPE_PACKET_PING:
                                pk = Packet()
                                pk.IDENTIFIER = Network.TYPE_PACKET_PONG
                                c.send(pk.encode())
                            elif pckt.getID() == Network.TYPE_PACKET_DUMMY:
                                pk = Packet()
                                pk.IDENTIFIER = Network.TYPE_PACKET_DUMMY
                                c.send(pk.encode())
                                del pk
                                pk = Packet()
                                pk.IDENTIFIER = Network.TYPE_PACKET_INFO
                                pk.DATA = self.getClientDataAll()
                            elif pckt.getID() == Network.TYPE_PACKET_DISCONNECT:
                                del self.CLIENTS[serverId]
                                TrinketLogger.debug("Client " + str(c.getpeername()) + " disconnected")
                            elif pckt.getID() == Network.TYPE_PACKET_COMMAND:
                                cmd = pckt.get("data")
                                to = pckt.get("to")
                                if to in self.CLIENTS:
                                    pk = Packet()
                                    pk.IDENTIFIER = Network.TYPE_PACKET_COMMAND_EXECUTE
                                    pk.DATA = cmd
                                    self.CLIENTS[to].send(pk.encode())
                                else:
                                    continue
                            elif pckt.getID() == Network.TYPE_PACKET_COMMAND_EXECUTE:
                                continue
                            elif pckt.getID() == Network.TYPE_PACKET_LOGIN:
                                continue
                            elif pckt.getID() == Network.TYPE_PACKET_CHAT:
                                if pckt.get("data") == Network.TYPE_STRING_EMPTY:
                                    continue
                                if str(pckt.get("data")) == "":
                                    continue
                                pk = Packet()
                                pk.IDENTIFIER = Network.TYPE_PACKET_CHAT
                                pk.DATA = pckt.get("data")
                                if pckt.get("to") in self.CLIENTS:
                                    tmp = self.CLIENTS[pckt.get("to")]
                                    tmp.send(pk.encode())
                                    continue
                                TrinketLogger.info(str(pckt.get("data")))
                                for t in self.CLIENTS:
                                    if t == serverId:
                                        continue
                                    tmp = self.CLIENTS[t]
                                    tmp.send(pk.encode())
                            elif pckt.getID() == Network.TYPE_PACKET_INFO_SEND:
                                self.INFO[serverId] = pckt.get("data")
                            elif pckt.getID() == Network.TYPE_PACKET_DATA_REQUEST:
                                pk = Packet()
                                pk.IDENTIFIER = Network.TYPE_PACKET_DATA_SEND
                                pk.DATA = self.getClientList()
                                c.send(pk.encode())
                        except socket.error:
                            continue
                except RuntimeError:
                    continue
            except (KeyboardInterrupt, SystemExit):
                return


    def setEnabled(self, value):
        self.ENABLED = value

    def listen(self):
        while self.ENABLED:
            try:
                conn, addr = self.s.accept()
                data =  json.loads(conn.recv(1024).decode().strip())
                pckt = DecodedPacket(data)
                if pckt.getID() == Network.TYPE_PACKET_LOGIN:
                    pwd = pckt.get('password')
                    if data["serverId"] in self.CLIENTS:
                        tm = time.time() - self.LAST_PACKET[str(pckt.get("serverId"))]
                        if tm < 5:
                            pk = Packet()
                            pk.IDENTIFIER = Network.TYPE_PACKET_LOGIN
                            pk.DATA = False
                            pk.ERROR = Network.TYPE_ERROR_SERVER_ID
                            conn.send(pk.encode())
                            TrinketLogger.error("Connection " + str(addr) + " attempted to login with registered serverID")
                            continue
                        else:
                            TrinketLogger.debug("Client " + str(conn.getpeername()) + " timed out")
                            del self.CLIENTS[str(data["serverId"])]

                    if pwd == self.PASSWORD:
                        pk = Packet()
                        pk.IDENTIFIER = Network.TYPE_PACKET_LOGIN
                        pk.DATA = True
                        pk.ERROR = Network.TYPE_ERROR_EMPTY
                        conn.send(pk.encode())
                        self.CLIENTS[data["serverId"]] = conn
                        data = pckt.get("data")
                        self.INFO[str(pckt.get("serverId"))] = data
                        TrinketLogger.debug("Connection from " + str(addr) + " with ID " + str(pckt.get("serverId")) + " accepted")
                        pk = Packet()
                        pk.IDENTIFIER = Network.TYPE_PACKET_DUMMY
                        conn.send(pk.encode())
                        self.LAST_PACKET[str(pckt.get("serverId"))] = time.time()
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
        self.LAST_PACKET = dict()
        self.LOGGER = logger
        self.ENABLED = True
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
            threading.Thread(target=self.clientlisten, daemon=True).start()

    def stop(self):
        for sid in self.CLIENTS:
            try:
                c = self.CLIENTS[sid]
                pk = Packet()
                pk.IDENTIFIER = Network.TYPE_PACKET_DISCONNECT
                pk.REASON = Network.TYPE_DISCONNECT_FORCED
                c.send(pk.encode())
            except RuntimeError:
                continue
