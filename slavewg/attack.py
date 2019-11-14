# coding:utf-8
import logging
import os
import json
import time
from pymouse import PyMouse
from pykeyboard import PyKeyboard
from threading import Timer, Lock
from queue import Queue
from .base import BaseOperation


class Attack(BaseOperation):
    def __init__(self, stoped, tasksQueue):
        """

        """
        isinstance(tasksQueue, Queue)
        BaseOperation.__init__(self, stoped, tasksQueue)
        self.log = logging.getLogger('攻击')
        self.interval = 2

    def start(self, x, y, key):
        self.queue.put(lambda: self.run(x, y, key))

    def run(self, x, y, key):
        """
        要指定蹲黑花的位置
        :param pos:
        :return:
        """

        with self.lock:
            self.do(x, y, key)

        if not self.stoped.wait(0.1):
            Timer(self.interval, self.queue.put, args=(lambda: self.run(x, y, key),)).start()

    def do(self, x, y, key):
        x_dim, y_dim = self.mouse.screen_size()
        x = int(x_dim / x)
        y = int(y_dim / y)
        time.sleep(0.1)
        self.mouse.click(x, y, 2)
        time.sleep(0.1)
        self.keyboard.tap_key(key)
