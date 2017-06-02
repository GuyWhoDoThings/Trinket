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
from trinket.utils.color import Color
from trinket.utils.utils import Utils


class TrinketLogger:

    @staticmethod
    def log(msg, prefix, color, threadname):
        print(Utils.format(color + "[" + threadname + "/" + prefix + "]: " + msg))

    @staticmethod
    def error(msg):
        TrinketLogger.log(msg, "ERROR", Color.RED, "Trinket")

    @staticmethod
    def warning(msg):
        TrinketLogger.log(msg, "WARNING", Color.YELLOW, "Trinket")

    @staticmethod
    def info(msg):
        TrinketLogger.log(msg, "INFO", "", "Trinket")

    @staticmethod
    def debug(msg):
        TrinketLogger.log(msg, "DEBUG", Color.GRAY, "Trinket")

    @staticmethod
    def typed(msg):
        TrinketLogger.log(msg, "TYPED", Color.GREEN, "Trinket")
