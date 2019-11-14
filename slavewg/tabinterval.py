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


class Tabinterval(BaseOperation):
    def __init__(self, stoped, tasksQueue):
        isinstance(tasksQueue, Queue)
        BaseOperation.__init__(self, stoped, tasksQueue)
        self.log = logging.getLogger('潜行')
        self.interval = 10

    def start(self, key, interval):
        self.interval = interval
        Timer(0.1, self.queue.put, args=(lambda: self.run(key),)).start()

    def run(self, key):
        """
        要指定蹲黑花的位置
        :param pos:
        :return:
        """

        with self.lock:
            self.do(key)

        if not self.stoped.wait(0.1):
            Timer(self.interval, self.queue.put, args=(lambda: self.run(key),)).start()

    def do(self, key):
        time.sleep(0.1)
        self.keyboard.tap_key(key)
