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
import random

class LootBlackLotus(BaseOperation):
    def __init__(self, stoped, tasksQueue):
        """

        """
        isinstance(tasksQueue, Queue)
        BaseOperation.__init__(self, stoped, tasksQueue)
        self.log = logging.getLogger('采黑花')
        self.range = 10

    def start(self, pos, split=6):
        self.queue.put(lambda: self.run(pos, split))

    def run(self, pos, split):
        """
        要指定蹲黑花的位置
        :param pos:
        :return:
        """

        with self.lock:
            self.do(pos, split)

        if not self.stoped.wait(self.interval):
            self.queue.put(lambda: self.run(pos, split))

    def do(self, pos, split):
        # 随机其他动作
        time.sleep(5)
        self.keyboard.press_key('q')
        time.sleep(0.1)
        self.keyboard.release_key('q')
        self.keyboard.press_key('e')
        time.sleep(0.1)
        self.keyboard.release_key('e')
        time.sleep(0.1)

        if random.randint(1,6) == 3:
            self.keyboard.tap_key('8')

        x_dim, y_dim = self.mouse.screen_size()
        print(x_dim, y_dim)
        y = int(y_dim / pos)

        if split == 0:
            x_list = [x_dim/2]
        else:
            x = x_dim / self.range / split

            x_list = []
            for i in range(split + 1):
                x_list.append(x_dim / 2 - (i - split / 2) * x)

        x_list = map(int, x_list)

        for x in x_list:
            time.sleep(1)

            # 移动鼠标
            self.mouse.move(x, y)
            time.sleep(0.1)

            # 拾取
            self.keyboard.press_key(self.keyboard.shift_key)
            self.mouse.click(x, y, 2)
            self.keyboard.release_key(self.keyboard.shift_key)
