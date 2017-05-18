import os, logging, sys
import threading
import time
os.chdir(os.path.realpath(sys.argv[0]).replace("\startup.py", ""))
from trinket.network.tcpserversocket import TCPServerSocket
from trinket.threads.commandreader import CommandReader
from trinket.utils.trinketlogger import TrinketLogger

class Trinket():

    def setEnabled(self, bool):
        self.ENABLED = bool

    def run(self):
        while self.ENABLED:
            continue

    def start(self):
        dir = os.path.dirname(os.path.realpath(sys.argv[0]))
        tm = time.time()
        TrinketLogger.info("Trinket Server v" + self.VERSION + " protocol version " + self.PROTOCOL_VERSION)
        TrinketLogger.info("Attempting to open server on " + self.HOST + ":" + str(self.PORT))

        self.SOCKET = TCPServerSocket(self.HOST, self.PORT, self.LOGGER, self.PASSWORD)
        CommandReader(self)

        start = time.time() - tm
        print("Started in " + str(round(start, 3)) + " seconds")

        self.run()

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

        self.LOGGER = logging.Logger
        self.start()

