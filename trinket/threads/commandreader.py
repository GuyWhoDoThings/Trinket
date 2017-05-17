import os
class CommandReader():

    @staticmethod
    def listen():
        while True:
            cmd = str(input("")).strip()
            if cmd == "stop" or cmd == "close":
                print("Stopping server...")
                os._exit(0)
                return
            else:
                print("Unknown Command")
                continue

