import os, sys
import json
import secrets
class Config():

    @staticmethod
    def handle():
        path = os.path.dirname(os.path.realpath(sys.argv[0])) + "/settings.json"
        if os.path.isfile(path):
            target = open(path, 'r')
            return json.loads(target.read())
        else:
            target = open(path, 'w')
            print("Welcome to the Trinket setup wizard.")
            print("Please input the following.")
            host = input("Host: ")
            port = input("Port: ")
            config = {"host": host, "port": int(port), "password": secrets.token_hex(8)}
            target.write(json.dumps(config, ensure_ascii=False, indent=4, sort_keys=True))
            return config
