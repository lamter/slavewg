import slavewg
from threading import Event
from queue import Queue



def test_runLoop():
    q = Queue()
    s = Event()
    s.set()
    lbl = slavewg.LootBlackLotus(s, q)
    lbl.do(lbl.pos_winterspring_mountain)

