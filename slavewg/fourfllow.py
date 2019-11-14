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


class FourFllow(BaseOperation):
    def __init__(self, stoped, tasksQueue):
        """
        4个职业同时跟随
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
        # TODO 分别点击4个窗口
        for x, y in self.getXY():
            time.sleep(0.2)
            self.mouse.click(x, y, 1)
            # 选中最近的敌人
            time.sleep(0.2)
            self.keyboard.tap_key('i')
            time.sleep(0.2)
            # 释放戏曲灵魂
            self.keyboard.tap_key('j')

        time.sleep(0.2)
        self.mouse.click(int(self.x_atom * 500), int(self.y_atom * 300), 1)
        self.stop()

    def getXY(self):
        return [
            (int(self.x_atom * 10), int(self.y_atom * 300)),
            (int(self.x_atom * 10), int(self.y_atom * 900)),
            (int(self.x_atom * 990), int(self.y_atom * 300)),
            (int(self.x_atom * 990), int(self.y_atom * 900)),
        ]
