import time
from threading import Event, Thread
from queue import Empty, Queue
import sys

try:
    keeping_time, wait_time = sys.argv[1:3]
except IndexError:
    print('默认挂机 62 分钟')
    keeping_time = None
    wait_time = None

import slavewg

if __name__ == '__main__':
    stoped = Event()
    stoped.wait(2)
    tasks_queue = Queue()

    fishing = slavewg.Fishing(stoped, tasks_queue, keeping_time, wait_time)
    # fishing.move()
    # fishing.record()

    fishing.start()
    fishing.run()
