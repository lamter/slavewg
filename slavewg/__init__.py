import logging.config
import os

floder = os.path.split(__file__)[0]
floder = os.path.split(floder)[0]
try:
    logging_conf = os.path.join(floder, 'logging.conf')
except FileNotFoundError:
    logging.warning('未找到日志文件')

from .loopBlackLotus import LootBlackLotus
from .ads import Ads
from .sneak import Sneak
from .attack import Attack
from .tabinterval import Tabinterval
from .fishing import Fishing
from .warlocklevelup import WarlockLevelup
from .entergate import EnterGate
from .collectsoulpices import CollectSoulPicese
from .fourcollectsoulpicese import FourCollectSoulPicese
from .fourfllow import FourFllow
from .windstone import WindStone
from .smbotmob import ShamanBotMobs
from .shamanbotwinterfall import ShamanBotWinterfall