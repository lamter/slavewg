# coding:utf-8
import logging
import os
import json
import time
from pymouse import PyMouse
from pykeyboard import PyKeyboard
from threading import Timer, Lock
from queue import Queue, Empty
from .base import BaseOperation
from itertools import product


class ShamanBotMobs(BaseOperation):
    WINDFURRY_KEY = '2'  # 风怒

    def __init__(self, stoped, tasksQueue):
        """
        萨满挂机原地打小怪
        """
        isinstance(tasksQueue, Queue)
        BaseOperation.__init__(self, stoped, tasksQueue)
        self.log = logging.getLogger('攻击')
        self.interval = 2

    def start(self):
        time.sleep(1)

        #
        # self.queue.put(self.buff)

    def run(self):
        """

        :param pos:
        :return:
        """
        # 每个动作要间隔1.6gcd
        while not self.stoped.wait(1.6):
            try:
                func = self.queue.get(timeout=1)
                with self.lock:
                    func()
            except Empty:
                pass

    def do(self):
        """
        主循环
        :return:
        """

    def loot(self):
        """
        拾取物品
        :return:
        """
        # 垂直下来，点击4个位置，同时点击拾取绑定确认

        x_p = [440, 500]
        y_p = [420, 460]

        # 按下 shift 键
        self.keyboard.press_key(self.keyboard.shift_key)

        for x, y in zip(x_p, y_p):
            x *= self.x_atom
            y *= self.y_atom
            time.sleep(0.5)
            self.mouse.click(x, y, 2, 1)  # 右键拾取
            time.sleep(0.5)
            # 点击确认拾取绑定
            self.mouse.click(self.x_atom * 450, self.y_atom * 250)

        self.keyboard.release_key(self.keyboard.shift_key)

        # 每30秒执行一次
        Timer(60 * 2, self.queue.put, args=(self.buff,)).start()

    def buff(self):
        """
        给自己施加buff
        :return:
        """
        # 风怒
        self.keyboard.tap_key(self.WINDFURRY_KEY)

        # 每2分钟重新补一次buff
        Timer(60 * 2, self.queue.put, args=(self.buff,)).start()
