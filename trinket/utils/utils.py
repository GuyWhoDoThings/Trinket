import platform
from trinket.utils.color import Color


class Utils:

    @staticmethod
    def format(msg):
        if Utils.getos() == "Windows":
            msg = msg.replace(Color.BLACK, "\033[0;30m")
            msg = msg.replace(Color.DARK_BLUE, "")
            msg = msg.replace(Color.DARK_GREEN, "\033[0;32m")
            msg = msg.replace(Color.DARK_AQUA, "\033[0;34m")
            msg = msg.replace(Color.DARK_RED, "\033[0;31m")
            msg = msg.replace(Color.DARK_PURPLE, "\033[0;35m")
            msg = msg.replace(Color.GOLD, "")
            msg = msg.replace(Color.GRAY, "\033[0;37m")
            msg = msg.replace(Color.DARK_GRAY, "\033[1;30m")
            msg = msg.replace(Color.BLUE, "\033[1;34m")
            msg = msg.replace(Color.GREEN, "\033[1;32m")
            msg = msg.replace(Color.AQUA, "\033[1;34m")
            msg = msg.replace(Color.RED, "\033[1;31m")
            msg = msg.replace(Color.LIGHT_PURPLE, "\033[1;35m")
            msg = msg.replace(Color.YELLOW, "\033[93m")
            msg = msg.replace(Color.WHITE, "\033[1;37m")
            msg = msg.replace(Color.BOLD, "")
            msg = msg.replace(Color.OBFUSCATED, "")
            msg = msg.replace(Color.STRIKETHROUGH, "")
            msg = msg.replace(Color.UNDERLINE, "\033[0;4;37m")
            msg = msg.replace(Color.ITALIC, "")
            msg = msg.replace(Color.RESET, "\033[0;0m")
            return msg + "\033[0;0m"
        elif Utils.getos() == "Linux":
            msg = msg.replace(Color.BLACK, "")
            msg = msg.replace(Color.DARK_BLUE, "")
            msg = msg.replace(Color.DARK_GREEN, "")
            msg = msg.replace(Color.DARK_AQUA, "")
            msg = msg.replace(Color.DARK_RED, "")
            msg = msg.replace(Color.DARK_PURPLE, "")
            msg = msg.replace(Color.GOLD, "")
            msg = msg.replace(Color.GRAY, "")
            msg = msg.replace(Color.DARK_GRAY, "")
            msg = msg.replace(Color.BLUE, "")
            msg = msg.replace(Color.GREEN, "")
            msg = msg.replace(Color.AQUA, "")
            msg = msg.replace(Color.RED, "")
            msg = msg.replace(Color.LIGHT_PURPLE, "")
            msg = msg.replace(Color.YELLOW, "")
            msg = msg.replace(Color.WHITE, "")
            msg = msg.replace(Color.BOLD, "")
            msg = msg.replace(Color.OBFUSCATED, "")
            msg = msg.replace(Color.STRIKETHROUGH, "")
            msg = msg.replace(Color.UNDERLINE, "")
            msg = msg.replace(Color.ITALIC, "")
            msg = msg.replace(Color.RESET, "")
            return msg

    @staticmethod
    def getos():
        return platform.system()
