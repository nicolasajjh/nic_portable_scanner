import multiprocessing
from time import sleep
import signal
def initializer():
    """Ignore SIGINT in child workers."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def worker():
    print("sleeep")
    sleep(10)
def main():
    try:
        pool = multiprocessing.Pool(5, initializer=initializer)

        for i in range(0, 5):
            pool.apply_async(worker, args=(i,))

        pool.close()

        input("Hit enter to terminate")
    except KeyboardInterrupt:
        print("CTRL+C")
    finally:
        pool.terminate()
        pool.join()

        print("Bye have a great time!")

if __name__ == '__main__':
    main()