import logging
from time import sleep
from threading import Event, Lock, Timer

from pymouse import PyMouse
from pykeyboard import PyKeyboard


class Ads(object):
    """
    定时刷新广告
    """

    def __init__(self, stoped, taskQueue):
        self.log = logging.getLogger('广告')
        self.queue = taskQueue
        self.mouse = PyMouse()
        self.keyboard = PyKeyboard()
        self.interval = 60 * 2  # seconds
        self.stoped = stoped

        self.lock = Lock()

    def start(self):
        self.queue.put(self.run)

    def run(self):
        """

        :return:
        """
        with self.lock:
            self.do()

        if not self.stoped.wait(0.1):
            Timer(self.interval, self.queue.put, args=(self.run,)).start()

    def do(self):
        self.keyboard.tap_key('9')
