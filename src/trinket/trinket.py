import os, logging
import json
import socket
import threading
import time
import pprint
from time import sleep
from trinket.network.tcpserversocket import TCPServerSocket
from trinket.threads.commandreader import CommandReader

class Trinket():

    def setEnabled(self, bool):
        self.ENABLED = bool

    def run(self):
        while self.ENABLED:
            continue

    def start(self):
        tm = time.time()
        print("Trinket Server v" + self.VERSION + " protocol version " + self.PROTOCOL_VERSION)
        print("Attempting to open server on " + self.HOST + ":" + str(self.PORT))

        TCPServerSocket(self.HOST, self.PORT, self.LOGGER)
        threading.Thread(target=CommandReader.listen()).start()

        start = time.time() - tm
        print("Started in " + str(round(start, 3)) + " seconds")

        self.run()

    def getProtocol(self):
        return self.PROTOCOL_VERSION

    def __init__(self):
        self.SERVER = False
        self.HOST = '0.0.0.0'
        self.PORT = 33657
        self.BUFFER = 1024

        self.VERSION = '0.1.7'
        self.PROTOCOL_VERSION = '1.0.0'

        self.CLIENTS = list()
        self.THREADS = list()

        self.ENABLED = True

        self.LOGGER = logging.Logger
        self.start()

