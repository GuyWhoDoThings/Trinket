import os, sys
import threading
from trinket.utils.trinketlogger import TrinketLogger
class CommandReader():

    def __init__(self, trinket):
        self.TRINKET = trinket
        self.TRINKET.finish()
        threading.Thread(target=self.listen(), daemon=True).start()

    def listen(self):
        while self.TRINKET.ENABLED:
            try:
                cmd = str(input("")).strip()
                if cmd == "stop" or cmd == "close":
                    TrinketLogger.warning("Stopping server...")
                    sys.exit()
                else:
                    TrinketLogger.info("Unknown Command")
                    continue
            except (KeyboardInterrupt, SystemExit):
                return

