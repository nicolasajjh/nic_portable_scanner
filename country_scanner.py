import multiprocessing.pool as mpool
import multiprocessing
import sys
import subprocess
from multiprocessing import current_process
from threading import Thread
from threading import active_count
import threading
from time import sleep
from IpTools_2 import ip_range_splitter
from scanner import *
import signal
import psutil
import atexit
def clr():
    UP = "\x1B[3A"
    CLR = "\x1B[0K"
    print(UP,CLR,end='')

def printU(msg):#updating message in one line
    print(f"\r{msg}",end='',flush=True)
def extract_ip_port(msg):
    ip= re.search(constant.ip_regex, msg).group()
    port=re.search("\d+",msg).group()
    return ip,port

def masscan_ips(country_code,target_port,ip_range):
    cmd = ["masscan","-p"+f"{target_port}", "--range", f"{ip_range}"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)#,stderr=subprocess.DEVNULL)

    while p.poll() is None:
        line = p.stdout.readline().decode('utf-8').strip()
        # print("checkpoint")
        if bool(line): #jika ada isinya
            # clr()
            print(line)
            print(f"current process = {active_count()}")

            #Discovered open port 22/tcp on 1.53.252.124
            ip,port=extract_ip_port(line)
            # print("ip danport = ",ip,port)
            send_msg_to_server(country_code,ip,port)
    # p.wait()

    # with subprocess.Popen(cmd, stdout=subprocess.PIPE) as p:
    #     while p.poll() is None:
    #         line = p.stdout.readline().decode('utf-8').strip()
    #         # print("checkpoint")
    #         if bool(line):  # jika ada isinya
    #             # clr()
    #             print(line)
    #             print(f"current process = {active_count()}")
    #
    #             # Discovered open port 22/tcp on 1.53.252.124
    #             ip, port = extract_ip_port(line)
    #             # print("ip danport = ",ip,port)
    #             insert_ip(country_code, ip, port)
    #     p.wait()

# def cur_process():

def range_scanner(country_code,port,ranges):

    for range in ranges:
        masscan_ips(country_code,port,range)


# signal.signal(signal.SIGCHLD, signal.SIG_IGN)
# signal.SIGCHLD
def initializer():
    """Ignore SIGINT in child workers."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    # signal.signal(signal.SIGCLD, signal.SIG_IGN)

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
def kill_all_process():
    atexit.register(cleanup)
    sys.exit()


def main(country_code,ip_ranges,port):
    max_concurrent_thread = 3

    # parmap.map(range_scanner,pm_processes=4)
    try:
        pool = multiprocessing.get_context('spawn').Pool(max_concurrent_thread,maxtasksperchild=max_concurrent_thread)#initializer)
        for ip_range in ip_ranges:
            pool.apply_async(range_scanner, args=(country_code,port, ip_range))
        print("active child = 1", multiprocessing.active_children())
        input("Hit enter to terminate")
        # kill_all_process()

        pool.close()
        print("active child = 1", multiprocessing.active_children())
        for child in multiprocessing.active_children():
            child.terminate()
    except KeyboardInterrupt:
        print("CTRL+C")
    finally:
        pool.terminate()
        pool.join()
        print("Bye have a g"
              "reat time!")
        print("active child = 3", multiprocessing.active_children())

def multi_thread(country_code,ip_ranges,port):
    for ip_range in ip_ranges:
        t=Thread(target=range_scanner,args=(country_code,port,ip_range))
        t.start()
# def country_scanner(country_code,port,hosts_per_thread):


if __name__=="__main__":
    country_code="vn"
    port=22
    hosts_per_thread=500000
    # country_scanner(country_code,22,200000)
    ip_ranges = ip_range_splitter(country_code, hosts_per_thread)

    #single masscan--------------
    # ip_range=ip_ranges[0]
    # range=ip_range[0]
    # masscan_ips(country_code,port,range)

    #running multiple masscan
    multi_thread(country_code,ip_ranges, port)
