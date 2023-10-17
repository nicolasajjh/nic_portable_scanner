import atexit
from time import sleep
import multiprocessing.pool as mpool
import sys
def kill_all_process():
    atexit.register(cleanup)
    sys.exit()


def cleanup():
    timeout_sec = 5

    all_process = psutil.Popen.children()
        # psutil.Process())
    children = all_process.children(recursive=True)
    for child in children:
        print('Child pid is {}'.format(child.pid))
    print("checkpoint",all_process)
    # input("enter again to kill process")
    # for p in all_process:  # list of your processes
    #     p_sec=0
    #     for second in range(timeout_sec):
    #         if p.poll() == None:
    #             time.sleep(1)
    #             p_sec += 1
    #     if p_sec >= timeout_sec:
    #         p.kill()  # supported from python 2.6
    # print("cleaned up!")
