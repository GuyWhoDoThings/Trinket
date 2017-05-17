from trinket.trinket import Trinket
from trinket.utils.config import Config
cfg = Config.handle()
Trinket(cfg["host"], int(cfg["port"]), cfg["password"])