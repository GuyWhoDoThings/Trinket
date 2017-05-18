import random
import sys
import socket

import ipaddress

class Utilities():

    @staticmethod
    def mt_rand(low=0, high = sys.maxsize):
        return random.randint(low, high)

    @staticmethod
    def myAddress(self):
        return socket.gethostbyname(socket.gethostname())