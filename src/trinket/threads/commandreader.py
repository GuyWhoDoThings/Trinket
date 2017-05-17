import os
import threading
from trinket.utils.trinketlogger import TrinketLogger
class CommandReader():

    def __init__(self, trinket):
        self.TRINKET = trinket
        threading.Thread(target=self.listen()).start()

    def listen(self):
        while True:
            cmd = str(input("")).strip()
            if cmd == "stop" or cmd == "close":
                TrinketLogger.warning("Stopping server...")
                self.TRINKET.SOCKET.stop()
                os._exit(0)
                return
            else:
                TrinketLogger.info("Unknown Command")
                continue

