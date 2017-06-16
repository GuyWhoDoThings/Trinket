import sys, os
os.chdir(os.path.realpath(sys.argv[0]).replace(str(os.sep) + "startup.py", ""))
from trinket.trinket import Trinket
from trinket.utils.config import Config
from subprocess import call
import platform
if platform.system() == "Linux":
    call("export PYTHONPATH=$PYTHONPATH:" + os.path.realpath(sys.argv[0]).replace(str(os.sep) + "startup.py", ""))

if sys.version_info < (3,5):
    print("It looks like you're running an unsupported version of Python!")
    print("Please update python to 3.5+")
    sys.exit(0)
else:
    cfg = Config.handle()
    Trinket(cfg["host"], int(cfg["port"]), cfg["password"])