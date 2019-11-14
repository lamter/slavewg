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


class WindStone(BaseOperation):
    def __init__(self, stoped, tasksQueue):
        """
        风石混声望
        """
        isinstance(tasksQueue, Queue)
        BaseOperation.__init__(self, stoped, tasksQueue)
        self.log = logging.getLogger()
        self.log.setLevel(logging.INFO)

        self.x_dim, self.y_dim = self.mouse.screen_size()
        self.x_atom, self.y_atom = self.x_dim / 1000, self.y_dim / 1000

        self.interval = 0.3

    def start(self):
        self.queue.put(self.do)
        # self.queue.put(self.move)

    def move(self):
        for x, y in self.getXY():
            self.mouse.click(x, y, 1)
            time.sleep(1)

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
        # 点击团队确认
        moment = 0
        self.put(moment, self.confirm)

        # 选中目标
        moment = 1
        self.put(moment, self.target)

        # 施法
        moment = 2
        for key in [4, 5]:
            self.put(moment, self.attack, key)
            moment += 3

        self.put(moment + 3, self.do)

    def target(self):
        self.keyboard.tap_key('=')

    def attack(self, key):
        self.keyboard.tap_key('{}'.format(key))

    def getXY(self):
        return [
            (int(self.x_atom * 10), int(self.y_atom * 300)),
            (int(self.x_atom * 10), int(self.y_atom * 900)),
            (int(self.x_atom * 990), int(self.y_atom * 300)),
            (int(self.x_atom * 990), int(self.y_atom * 900)),
        ]

    def confirm(self):
        x, y = self.confirmXY()
        self.mouse.click(x, y, 2)

    def confirmXY(self):
        if self.isMac:
            return [

                int(self.x_atom * 650), int(self.y_atom * 650),
            ]
        else:
            return [
                int(self.x_atom * 600), int(self.y_atom * 520),
            ]
