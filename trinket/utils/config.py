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
import os, sys
import json
import random
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
            config = {"host": host, "port": int(port), "password": random.randint(1,9999999)}
            target.write(json.dumps(config, ensure_ascii=False, indent=4, sort_keys=True))
            return config
