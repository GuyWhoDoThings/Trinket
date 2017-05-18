import os
import threading
from trinket.utils.trinketlogger import TrinketLogger
class CommandReader():

    def __init__(self, trinket):
        self.TRINKET = trinket
        self.TRINKET.finish()
        threading.Thread(target=self.listen()).start()

    def listen(self):
        while self.TRINKET.ENABLED:
            try:
                cmd = str(input("")).strip()
                if cmd == "stop" or cmd == "close":
                    TrinketLogger.warning("Stopping server...")
                    os._exit(0)
                else:
                    TrinketLogger.info("Unknown Command")
                    continue
            except SystemExit:
                return

