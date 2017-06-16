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
import sys
import threading
from trinket.utils.trinketlogger import TrinketLogger


class CommandReader:

    def __init__(self, trinket):
        self.TRINKET = trinket
        self.TRINKET.finish()
        threading.Thread(target=self.listen(), daemon=True).start()

    def listen(self):
        while self.TRINKET.ENABLED:
            try:
                cmd = str(input("")).strip()
                if cmd == "stop" or cmd == "close" or cmd == "shutdown":
                    TrinketLogger.warning("Stopping server...")
                    sys.exit()
                else:
                    TrinketLogger.info("Unknown Command")
                    continue
            except (KeyboardInterrupt, SystemExit):
                return
