# coding:utf-8
import logging
import time
import pyaudio
import numpy
import platform
import datetime
import random

from threading import Timer, Event
from queue import Queue, Empty
from .base import BaseOperation

# 定义数据流块
CHUNK = 1024
FORMAT = pyaudio.paInt16
# CHANNELS = 1 # 声卡
CHANNELS = 2  # 麦克风
RATE = 44100
# 录音时间
RECORD_SECONDS = 1


class Fishing(BaseOperation):
    BAIT_KEY = '0'  # 鱼饵键
    CASTING_KEY = '-'  # 抛竿键
    LIVE_KEY = 'b'  # 维持在线的技能

    def __init__(self, stoped, tasksQueue, keeping_time=62, wait_time=0):
        """
        抛竿为-键
        鱼诱为0键
        """
        isinstance(tasksQueue, Queue)
        BaseOperation.__init__(self, stoped, tasksQueue)
        self.log = logging.getLogger()
        self.log.setLevel(logging.INFO)

        self.isNeedHooks = True
        self.range = 10
        self.waveData = None  # 起勾音频数据
        self.isWaitColletiting = True  # 等待起勾
        if isinstance(keeping_time, str):
            keeping_time = int(keeping_time)
        if isinstance(wait_time, str):
            wait_time = int(wait_time)

        self.keeping_time = keeping_time or 62  # 钓鱼持续时间
        self.wait_time = wait_time or 0  # 多久之后才开始钓鱼，开始之前挂机等待

    def start(self):

        # self.isNeedHooks = False
        # Timer(60 * 10 + 10, lambda :setattr(self, 'isNeedHooks', True))

        if self.wait_time > 0:
            self.queue.put(self.wait)
            return

        self.queue.put(self.do)
        # self.queue.put(self.move)

        mins = self.keeping_time  # 分钟后关闭
        self.log.warning('{} 分钟后自动关闭'.format(mins))
        self.put(60 * mins, self.close)

    def wait(self):
        start = datetime.datetime.now()
        self.log.warning(f'{self.wait_time} 分钟后开始钓鱼')
        wait_time = datetime.timedelta(minutes=self.wait_time)
        while True:
            pass_time = datetime.datetime.now() - start
            print(pass_time, pass_time > wait_time)
            if pass_time > wait_time:
                break

            time.sleep(random.randint(30, 50))
            # 保持在线
            self.keyboard.tap_key(self.LIVE_KEY)
            time.sleep(2)
            self.keyboard.tap_key(self.LIVE_KEY)

        self.wait_time = 0
        self.start()

    def move(self):
        # x, y = int(self.x_atom * 286), int(self.y_atom * 30)
        # self.mouse.move(x, y)
        # self.mouse.click(x, y, 1, 2)

        x_list, y_list = self.getXY()
        for x in x_list:
            for y in y_list:
                time.sleep(1)
                self.mouse.move(x, y)

    def run(self):
        """
        计时循环
        :param pos:
        23:return:
        """
        while not self.stoped.wait(0):
            try:
                func = self.queue.get(timeout=1)
                with self.lock:
                    func()
            except Empty:
                pass

    def getXY(self):
        # mac 大屏幕分辨率
        if self.isMac:
            # x_list = [self.x_atom * 640]
            # y_list = [self.y_atom * 702, self.y_atom * 650, self.y_atom * 730, self.y_atom * 676]
            x_list = [self.x_atom * x for x in range(430, 580, 25)]
            x_list = random.sample(x_list, len(x_list))
            y_list = [self.y_atom * 550]
        else:
            # windows
            # x_list = [self.x_atom * 650, self.x_atom * 670, self.x_atom * 630]
            x_list = [self.x_atom * 650]
            y_list = [self.y_atom * 620, self.y_atom * 590, self.y_atom * 680, self.y_atom * 660]

        return [int(i) for i in x_list], [int(i) for i in y_list]

    def collect(self):
        """
        收杆动作
        :return:
        """
        stoped = Event()
        self.log.warning('收杆')

        x_list, y_list = self.getXY()

        self.keyboard.press_key(self.keyboard.shift_key)
        for x in x_list:
            for y in y_list:
                stoped.wait(0.2)
                self.mouse.click(x, y, 2, 1)
        self.keyboard.release_key(self.keyboard.shift_key)
        # time.sleep(0.5)
        # self.keyboard.tap_key(self.keyboard.escape_key)

        # 已经起勾，重新开始
        Timer(1, lambda: self.queue.put(self.do)).start()

    def do(self):
        """
        钓鱼动作循环
        :return:
        """
        # if self.isNeedHooks:
        #     self.hooks()
        #     return

        # 抛竿
        self.log.warning('抛竿')
        self.keyboard.tap_key(self.CASTING_KEY)

        # 录音点
        # recordMoments = list(range(14, 29, 2))
        recordMoments = list(range(2, 29, 2))
        startTime = time.time()

        def moments():
            for m in recordMoments:
                yield m

        m = moments()
        nextMoment = next(m)

        self.log.warning('{} 秒后开始录音'.format(nextMoment))
        while self.isWaitColletiting and not self.stoped.wait(0.1):
            delta = time.time() - startTime
            if delta >= nextMoment:
                try:
                    nextMoment = next(m)
                except StopIteration:
                    self.isWaitColletiting = False
                    break
                # 录音时机
                self.log.warning('第 {} 秒录音'.format(round(delta, 1)))
                self.record()
                self.anayVedio()

        # 上钩了
        self.isWaitColletiting = True
        self.collect()

    def hooks(self):
        """
        上鱼饵
        :return:
        """
        stoped = Event()

        self.log.warning('点击鱼饵')
        # 点击鱼饵
        self.keyboard.tap_key(self.BAIT_KEY)

        Timer(1, lambda: self.queue.put(self.putbait)).start()

        # 设置重新上鱼饵的时间
        Timer(60 * 10 + 10, lambda: setattr(self, 'isNeedHooks', True)).start()
        # Timer(60 * 5 + 10, lambda: setattr(self, 'isNeedHooks', True)).start()

        stoped.clear()

    def putbait(self):
        """
        鱼饵放到钩上
        :return:
        """

        # 移动鼠标到鱼竿上，上鱼饵
        if self.isMac:
            x, y = self.x_atom * 100, self.y_atom * 670
        else:
            # Windows 系统
            x, y = self.x_dim / 100 * 39, self.y_dim / 100 * 63

        x, y = int(x), int(y)
        self.mouse.move(x, y)
        Timer(1, lambda: self.queue.put(lambda: self.movebait(x, y))).start()

    def movebait(self, x, y):
        x, y = int(x), int(y)
        self.log.warning('挂鱼饵')
        self.mouse.click(x, y, 1)

        self.isNeedHooks = False

        # 重新开始抛竿
        Timer(6, lambda: self.queue.put(self.do)).start()

    def record(self):
        """
        录音
        :return:
        """
        # 创建PyAudio对象
        p = pyaudio.PyAudio()

        # 打开数据流
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        self.log.warning("* recording")

        # 开始录音
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        self.log.warning("* done recording")

        wave_data = numpy.fromstring(b''.join(frames), dtype=numpy.short)
        wave_data.shape = -1, 2
        # 将数组转置
        wave_data = wave_data.T
        self.waveData = wave_data
        stream.close()

    def anayVedio(self):
        """
        分析音频
        :return:
        """
        start = 0  # 开始采样位置
        df = RATE / (RATE - 1)  # 分辨率
        freq = [df * n for n in range(0, RATE)]  # N个元素
        wave_data2 = self.waveData[0][start:start + RATE]
        c = numpy.fft.fft(wave_data2) * 2 / RATE
        # 常规显示采样频率一半的频谱
        d = int(len(c) / 2)
        # 仅显示频率在4000以下的频谱
        while freq[d] > 2100:
            d -= 10

        f, h = 0, 0
        # 取4个频率的音量
        freqtest = [500, 1000, 1500, 2000]
        for i in freqtest:
            h += abs(c[i])

        # 音量足够大时，说明上钩了
        self.log.warning('音量 {}'.format(h))

        if self.isMac:
            soundVolume = 1
        else:
            soundVolume = 0.5

        if h > soundVolume:
            # 起勾动作
            self.isWaitColletiting = False
            self.log.warning('音效分析 上钩')
        else:
            # 没有上钩
            self.log.warning('音效分析 没有上钩')
