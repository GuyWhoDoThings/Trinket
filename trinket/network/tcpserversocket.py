import socket
import json
import threading
import pprint
import time
import logging
from trinket.network.packet import Packet, DecodedPacket
from trinket.network.network import Network
class TCPServerSocket():

    def getLogger(self):
        return self.LOGGER

    def clientlisten(self):
        while True:
            try:
                for serverId in self.CLIENTS:
                    try:
                        c = self.CLIENTS[serverId]
                        j = c.recv(1024)
                        if not j:
                            continue
                        if j == "":
                            continue
                        if j == "null" or j == "NULL":
                            continue
                        pckt = DecodedPacket(json.loads(j))
                        if pckt.getID() == Network.TYPE_PACKET_DUMMY:
                            pk = Packet()
                            pk.IDENTIFIER = 0x01
                            c.send(pk.encode())
                            del pk
                            time.sleep(1)
                        elif pckt.getID() == Network.TYPE_PACKET_DISCONNECT:
                            del self.CLIENTS[serverId]
                            print("Client " + str(c.getpeername()) + " disconnected")
                        elif pckt.getID() == Network.TYPE_PACKET_DATA_REQUEST:
                            pk = Packet()
                            pk.IDENTIFIER = Network.TYPE_PACKET_DATA_SEND
                            pk.DATA = self.getClientList()
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
                    except socket.error as e:
                        continue
            except RuntimeError:
                continue

    def getClientList(self):
        cl = dict()
        for id in self.CLIENTS:
            sk = self.CLIENTS[id]
            cl[id] = [id, sk.getpeername()]
        return str(cl)

    def listen(self):
        while True:
            conn, addr = self.s.accept()
            data = json.loads(conn.recv(1024))
            pckt = DecodedPacket(data)
            #pprint.pprint(data)
            if pckt.getID() == Network.TYPE_PACKET_LOGIN:
                pwd = pckt.get('password')
                self.PASSWORD = "by90sose"
                if pwd == self.PASSWORD:
                    pk = Packet()
                    pk.IDENTIFIER = Network.TYPE_PACKET_LOGIN
                    pk.DATA = True
                    pk.ERROR = ""
                    conn.send(pk.encode())
                    self.CLIENTS[data["serverId"]] = conn
                    print("Connection from " + str(addr) + " accepted")
                    continue
                else:
                    pk = Packet()
                    pk.IDENTIFIER = Network.TYPE_PACKET_LOGIN
                    pk.DATA = False
                    pk.ERROR = Network.TYPE_ERROR_INVALID_PASSWORD
                    conn.send(pk.encode())
                    print("Connection from " + str(addr) + " refused, Invalid Password")
                    continue

    def __init__(self, HOST, PORT, logger: logging.Logger):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = HOST
        self.PORT = PORT
        self.CLIENTS = dict()
        self.LOGGER = logger
        try:
            self.s.bind((self.HOST, self.PORT))
        except Exception as e:
            print("FAILED TO BIND TO PORT! Perhaps another server is running on the port?")
        finally:
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.listen(5)
            print("Trinket running on " + self.HOST + ":" + str(self.PORT))
            threading.Thread(target=self.listen).start()
            threading.Thread(target=self.clientlisten).start()

    def __del__(self):
        for c in self.CLIENTS:
            try:
                pk = Packet()
                pk.IDENTIFIER = 82
                pk.REASON = 11000001
                c.send(pk.encode())
            except Exception as e:
                continue
