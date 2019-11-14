# coding:utf-8
import time
from queue import Queue, Empty
from threading import Event, Thread
import slavewg

stoped = Event()
tasks_queue = Queue()

# 要执行的脚本
# ads = slavewg.Ads(stoped, tasks_queue)
# ads.run()

lbl = slavewg.LootBlackLotus(stoped, tasks_queue)
lbl.run(lbl.position['燃烧石锤山黑花'])

s = slavewg.Sneak(stoped, tasks_queue)
s.run('=')


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
