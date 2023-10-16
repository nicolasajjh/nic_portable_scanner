import asyncio
from time import sleep
from threading import Thread, active_count
import multiprocessing

#bisa di stop and max thread, and not leaving zombies

import threading
max_running_threads=5
threadLimiter = threading.BoundedSemaphore(max_running_threads)
class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def run(self):

        threadLimiter.acquire()
        try:
            self.Executemycode()
        finally:
            threadLimiter.release()
multiprocessing.Pool()
    def Executemycode(self):
        print(" Hello World!")
        sleep(5)
    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

a = StoppableThread()
for b in range(100):
    a.run()