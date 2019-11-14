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


class CollectSoulPicese(BaseOperation):
    def __init__(self, stoped, tasksQueue):
        """
        打灵魂石
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

        mins = 60 * 2 # 2小时后自动关闭
        self.log.warning('{} 分钟后自动关闭'.format(mins))
        self.put(60 * mins, self.close)

    def move(self):
        self.loop()

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
        # 给自己反隐
        moment = 0
        self.antiInvisibility()

        moment += self.interval
        self.put(moment, self.target)

        # 宝宝攻击
        moment += self.interval
        self.put(moment, self.petAttack)

        # 捡东西g
        moment += 1
        self.put(moment, self.loop)

        # 控制宝宝回来
        moment += 3
        self.put(moment, self.petback)

        # 选择最后一个有敌意的目标
        moment += 1
        self.put(moment, self.targetAgain)

        # 释放技能
        moment += 4
        skillNum = 5
        for skill in range(1, skillNum + 1):
            self.put(moment, self.spell, skill)
            moment += 2

        # 等待吸碎片完成，重新开始
        moment += 30
        self.put(moment, self.do)

    def target(self):
        self.keyboard.tap_key('=')

    def petAttack(self):
        self.keyboard.press_keys([self.keyboard.shift_key, 'q'])

    def antiInvisibility(self):
        self.keyboard.press_keys([self.keyboard.shift_key, '-'])
        self.keyboard.tap_key('-')

    def loop(self):
        x, y = self.loopXY()
        self.mouse.move(x, y)
        self.keyboard.press_key(self.keyboard.shift_key)
        self.mouse.click(x, y, 2)
        self.keyboard.release_key(self.keyboard.shift_key)

    def loopXY(self):
        x = self.x_atom * 650
        y = self.y_atom * 700
        return int(x), int(y)

    def petback(self):
        self.keyboard.press_keys([self.keyboard.shift_key, 'w'])

    def targetAgain(self):
        self.keyboard.tap_key('g')

    def spell(self, skill):
        """

        :param skill:
        :return:
        """
        self.keyboard.tap_key('{}'.format(skill))
