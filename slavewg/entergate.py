# coding:utf-8
import logging
import time
import pyaudio
import numpy
import platform
import itertools

from threading import Timer, Event
from queue import Queue, Empty
from .base import BaseOperation


class EnterGate(BaseOperation):
    def __init__(self, stoped, tasksQueue):
        """
        副本顶门
        """
        isinstance(tasksQueue, Queue)
        BaseOperation.__init__(self, stoped, tasksQueue)
        self.log = logging.getLogger()
        self.log.setLevel(logging.INFO)

        self.x_dim, self.y_dim = self.mouse.screen_size()
        self.x_atom, self.y_atom = self.x_dim / 1000, self.y_dim / 1000

    def start(self):
        self.queue.put(self.do)
        # self.queue.put(self.move)

    def run(self):
        """
        计时循环
        :param pos:
        :return:
        """
        while not self.stoped.wait(0):
            try:
                func = self.queue.get(timeout=1)
                if func:
                    with self.lock:
                        func()
            except Empty:
                pass

    def do(self):
        """

        :return:
        """
        # 前进1秒
        self.keyboard.press_key('w')
        time.sleep(2)
        self.keyboard.release_key('w')

        # 后退1秒
        self.keyboard.press_key('s')
        time.sleep(1)
        self.keyboard.release_key('s')

        self.put(1, self.do)
