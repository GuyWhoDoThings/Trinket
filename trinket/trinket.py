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
import os, sys
import time
import logging

from trinket.network.tcpserversocket import TCPServerSocket
from trinket.threads.commandreader import CommandReader
from trinket.utils.trinketlogger import TrinketLogger
from trinket.network.network import Network
from trinket.network.protocol.packet import Packet

class Trinket():

    def setEnabled(self, bool):
        self.ENABLED = bool

    def run(self):
        while self.ENABLED:
            continue

    def start(self):
        dir = os.path.dirname(os.path.realpath(sys.argv[0]))

        TrinketLogger.info("Trinket Server v" + self.VERSION + " protocol version " + self.PROTOCOL_VERSION)
        TrinketLogger.info("Attempting to open server on " + self.HOST + ":" + str(self.PORT))

        self.SOCKET = TCPServerSocket(self.HOST, self.PORT, self.LOGGER, self.PASSWORD)
        self.COMMAND = CommandReader(self)
        self.ENABLED = False

        TrinketLogger.info("Disconnecting all clients...")
        for sid in self.SOCKET.CLIENTS:
            c = self.SOCKET.CLIENTS[sid]
            pk = Packet()
            pk.IDENTIFIER = Network.TYPE_PACKET_DISCONNECT
            try:
                c.send(pk.encode())
            except c.error:
                continue

    def finish(self):
        start = time.time() - self.tm
        TrinketLogger.info("Started in " + str(round(start, 3)) + " seconds")

    def __init__(self, host, port, password):
        self.SERVER = False
        self.HOST = host
        self.PORT = port
        self.BUFFER = 1024
        self.PASSWORD = password

        self.VERSION = '0.1.7'
        self.PROTOCOL_VERSION = '1.0.0'

        self.CLIENTS = list()
        self.THREADS = list()

        self.ENABLED = True
        self.SOCKET = ""
        self.COMMAND = ""
        self.tm = time.time()

        self.LOGGER = logging.Logger
        self.start()

