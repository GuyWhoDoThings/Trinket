import sys, os
os.chdir(os.path.realpath(sys.argv[0]).replace(str(os.sep) + "startup.py", ""))
from trinket.trinket import Trinket
from trinket.utils.config import Config
import platform
if platform.system() != "Windows":
    print("Trinket doesn't support " + platform.platform())
    sys.exit(0)

if sys.version_info < (3,4):
    print("It looks like you're running an unsupported version of Python!")
    print("Please update python to 3.4+")
    sys.exit(0)
else:
    cfg = Config.handle()
    Trinket(cfg["host"], int(cfg["port"]), cfg["password"])
