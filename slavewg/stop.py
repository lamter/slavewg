from pykeyboard import PyKeyboardEvent
import time

class TapRecord(PyKeyboardEvent):
    def __init__(self):
        PyKeyboardEvent.__init__(self)

    def tap(self, character, n, interval):
        print(character)


t = TapRecord()
t.start()
# t.run()

