import sys, os
os.chdir(os.path.realpath(sys.argv[0]).replace(str(os.sep) + "startup.py", ""))
from trinket.trinket import Trinket
from trinket.utils.config import Config

if sys.version_info < (3,5):
    print("It looks like you're running an unsupported version of Python!")
    print("Please update python to 3.5+")
    os._exit(0)
else:
    cfg = Config.handle()
    Trinket(cfg["host"], int(cfg["port"]), cfg["password"])