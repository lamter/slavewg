# coding:utf-8
import logging
import os
import json
import time
import platform
# from pymouse.mac import PyMouse
# from pykeyboard.mac import PyKeyboard
from pymouse import PyMouse
from pykeyboard import PyKeyboard
from threading import Timer, Lock
from queue import Queue

pos_file = os.path.join(os.path.split(__file__)[0], 'position.json')

with open(pos_file, 'r', encoding='utf8') as f:
    position = json.load(f)


# class Mouse(PyMouse):
#
#     def move(self, x, y):
#         if platform.system() == 'Darwin':
#             # OS 操作系统
#             return super(self).move(x, y)
#         if platform.system() == 'Windows':
#
#         else:
#             raise ValueError('unknow system')
class BaseOperation(object):
    def __init__(self, stoped, tasksQueue):
        """

        """
        isinstance(tasksQueue, Queue)
        self.log = logging.getLogger()
        self.queue = tasksQueue  # 任务队列
        self.mouse = PyMouse()
        self.keyboard = PyKeyboard()
        self.position = position
        self.interval = 1  # seconds
        self.stoped = stoped
        self.lock = Lock()
        self.isMac = platform.system() == 'Darwin'

        self.x_dim, self.y_dim = self.mouse.screen_size()
        self.x_atom, self.y_atom = self.x_dim / 1000, self.y_dim / 1000

    def run(self, *args, **kwargs):
        """
        计时循环
        :param args:
        :param kwargs:
        :return:
        """
        pass


    def do(self, *args, **kwargs):
        pass

    def stop(self):
        self.stoped.set()


    def put(self, sec, func, *args, **kwargs):

        if not callable(func):
            print(func)
            raise TypeError('func is not callable!')

        def foo():
            if args and kwargs:
                func(*args, **kwargs)
            elif args:
                func(*args)
            elif kwargs:
                func(**kwargs)
            else:
                func()
        Timer(sec, lambda :self.queue.put(foo)).start()

    # 定时关闭
    def close(self):
        self.log.warning('定时关闭')
        x, y = int(self.x_atom * 286), int(self.y_atom * 30)
        self.mouse.click(x, y, 1, 2)
        self.stoped.set()


if __name__ == '__main__':
    from threading import Event
    stoped = Event()
    stoped.wait(2)
    tasks_queue = Queue()
    bo = BaseOperation(stoped, tasks_queue)
    bo.keyboard.tap_key('escape')
