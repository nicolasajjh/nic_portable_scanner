import multiprocessing
import subprocess
from multiprocessing import current_process
from threading import Thread, active_count
import threading
from IpTools_2 import ip_range_splitter
from send_msg_to_server import send_msg_to_server
import signal
from constant import ip_regex
import re

def clr():
    UP = "\x1B[3A"
    CLR = "\x1B[0K"
    print(UP,CLR,end='')

def printU(msg):#updating message in one line
    print(f"\r{msg}",end='',flush=True)

def extract_ip_port(msg):
    ip= re.search(ip_regex, msg).group()
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
            # print("check--------------------")
            ip,port=extract_ip_port(line)
            # print(ip,port,"why not executed---------------")
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




def multi_process(country_code,ip_ranges,port):
    #user variable----------------------------------------------------------------------------------------------
    max_concurrent_thread = 5

    # parmap.map(range_scanner,pm_processes=4)
    try:                      #.get_context('spawn')
        pool = multiprocessing.Pool(max_concurrent_thread,initializer=initializer)#,maxtasksperchild=max_concurrent_thread)
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
        print("Bye have a g""reat time!")
        print("active child = 3", multiprocessing.active_children())

def multi_thread(country_code,ip_ranges,port):
    for ip_range in ip_ranges:
        t=Thread(target=range_scanner,args=(country_code,port,ip_range))
        t.start()


if __name__=="__main__":
    #---------------------------------
    #Dependencies
    #User input----------------------------------------------------------------
    mode="real"
    country_code="vn"
    port=22
    hosts_per_thread=200000
    #max_concurrent_threads di main()
    #----------------------------------------------

    # country_scanner(country_code,22,200000)
    ip_ranges = ip_range_splitter(country_code, hosts_per_thread)
    if mode=="tes":
    #single masscan--------------
        ip_range=ip_ranges[0]
        range=ip_range[0]
        masscan_ips(country_code,port,range)
    elif mode=="real":
    #   running multiple masscan
        # multi_thread(country_code,ip_ranges, port)
        multi_process(country_code,ip_ranges,port)
