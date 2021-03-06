# coding:utf-8
import time
from queue import Queue, Empty
from threading import Event, Thread
import slavewg

stoped = Event()
tasks_queue = Queue()

# 要执行的脚本
# ads = slavewg.Ads(stoped, tasks_queue)
# ads.start()

lbl = slavewg.LootBlackLotus(stoped, tasks_queue)
lbl.start(lbl.position['东泉熊怪贼黑花'], split=0)

# 攻击
att = slavewg.Attack(stoped, tasks_queue)
att.start(2, lbl.position['东泉熊怪贼黑花'], '0')

# 潜行
sneak = slavewg.Sneak(stoped, tasks_queue)
sneak.start('=')


def run():
    time.sleep(5)
    while not stoped.wait(0.1):
        try:
            func = tasks_queue.get(timeout=1)
            func()
        except Empty:
            pass


Thread(target=run, daemon=True).start()

input_ = input('Enter Any key to Stop:')
stoped.set()
