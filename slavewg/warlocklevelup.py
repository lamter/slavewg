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


class WarlockLevelup(BaseOperation):
    def __init__(self, stoped, tasksQueue):
        """
        术士升级
        """
        isinstance(tasksQueue, Queue)
        BaseOperation.__init__(self, stoped, tasksQueue)
        self.log = logging.getLogger()
        self.log.setLevel(logging.INFO)

        self.x_dim, self.y_dim = self.mouse.screen_size()
        self.x_atom, self.y_atom = self.x_dim / 1000, self.y_dim / 1000

        self.opreationInterval = 1  # 普通操作间隔
        self.spellInterval = 3  # 施法间隔
        self.players = None  # 角色列表
        self.player = None  # 当前角色
        self.turning = False # 正在转身

    def start(self):
        self.queue.put(self.do)
        # self.queue.put(self.move)

        # # 定时关闭
        # def close():
        #     self.log.warning('定时关闭')
        #     x, y = int(self.x_atom * 286), int(self.y_atom * 30)
        #     self.mouse.click(x, y, 1, 2)
        #     self.stoped.set()
        #
        #
        # mins = 59  # 分钟后关闭
        # self.log.warning('{} 分钟后自动关闭'.format(mins))
        # Timer(60 * mins, close).start()

    def move(self):
        pos = self.launchPos()
        for x, y in pos:
            self.mouse.click(x, y, 2)
            self.mouse.click(x + 10, y+1, 1)

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

        # 每个号轮流释放技能
        if not self.player:
            self.players = self.launchPos()

        # 取当前角色的启动器坐标
        try:
            x, y = next(self.players)
        except StopIteration:
            self.players = None
            self.put(self.opreationInterval, self.do)
            return

        # 选择启动器
        self.mouse.click(x, y, 2)

        # 点击启动器
        self.put(self.opreationInterval, self.launch, x, y)

    def launch(self, x, y):
        # 右键打开启动器
        self.mouse.click(x + 10, y + 2, 1)
        self.put(self.opreationInterval, self.turnAround)

    def turnAround(self):
        """
        转身
        :return:
        """
        if self.turning:
            # 停止转身
            self.keyboard.release_key('a')
            # 开始攻击
            self.put(self.opreationInterval, self.petAttack)
        else:
            self.keyboard.press_key('a')
            # 转身时间0.3秒
            self.turning = True
            self.put(0.3, self.turnAround)

    def launchPos(self):
        """
        启动器坐标
        :return:
        """
        x_list = [int(self.x_atom * 230)]
        playersNum = 1  # 玩家数量
        y_list = [int(self.y_atom * i) for i in range(110, 160, 14)][:playersNum]

        pos = []
        for x in x_list:
            for y in y_list:
                pos.append((x, y))
        for x, y in pos:
            yield x, y

    def target(self):
        """
        选中目标
        :return:
        """
        # 选中目标
        self.keyboard.tap_key('t')

        # 1秒后控制小鬼进攻5
        self.put(self.opreationInterval, self.petAttack, )

    def petAttack(self):
        """
        控制小鬼攻击
        :return:
        """

        self.keyboard.press_keys([self.keyboard.shift_key, 'q'])

        # 选中小鬼的目标
        self.put(self.opreationInterval, self.chosePet, )

    def chosePet(self):
        """
        选中宠物
        :return:
        """
        self.keyboard.press_keys([self.keyboard.shift_key, 'l'])

        # 协助目标
        self.put(self.opreationInterval, self.helpTarget, )

    def helpTarget(self):
        """

        :return:
        """
        self.keyboard.tap_key('f')

        # 开始释放技能
        self.put(self.opreationInterval, self.startAttack)

    def startAttack(self):
        """

        :return:
        """
        sec = 0
        for key in range(1, 7):
            self.put(sec, self.keyboard.tap_key, '{}'.format(key))
            sec += self.spellInterval

        # 重新开始
        self.put(sec, self.do)
