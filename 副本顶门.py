import time
from threading import Event, Thread
from queue import Empty, Queue

import slavewg

if __name__ == '__main__':
    stoped = Event()
    stoped.wait(2)
    tasks_queue = Queue()

    fishing = slavewg.EnterGate(stoped, tasks_queue)
    fishing.start()

    fishing.run()
