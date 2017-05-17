from trinket.utils.color import Color
class TrinketLogger:

    @staticmethod
    def log(msg, prefix, color, threadname):
        print(color + "[" + threadname + "/" + prefix + "]: " + msg + Color.RESET)

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
        TrinketLogger.log(msg, "DEBUG", Color.OKBLUE, "Trinket")
