import threading, time, random
from queue import Queue

jobs = Queue()

max_running_threads=5
def do_stuff(q):
    while not q.empty():
        value = q.get()
        time.sleep(2)
        print(value)
        q.task_done()

for i in range(10):
    jobs.put(i)

for i in range(max_running_threads):
    worker = threading.Thread(target=do_stuff, args=(jobs,))
    worker.start()

print("waiting for queue to complete", jobs.qsize(), "tasks")
jobs.join()
print("all done")