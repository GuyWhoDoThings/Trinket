import random
import sys
import socket

import ipaddress

class Utilities:

    TYPE_JSON = 0
    TYPE_MESSAGE = 1

    @staticmethod
    def mt_rand(low=0, high = sys.maxsize):
        return random.randint(low, high)

    @staticmethod
    def myAddress(self):
        return socket.gethostbyname(socket.gethostname())
