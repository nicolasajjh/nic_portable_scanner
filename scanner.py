import subprocess
import socket
import constant
# from IPy import IP
import re
from IpTools_2 import ip_range_splitter

def filter(message):#jika mengandung ip
    # ip_payload=r'(?:\d{1,3}\.)+(?:\d{1,3})'
    a=re.search("Discovered",message)
    if a:
        b=re.search(constant.ip_regex,message)
        if b:
            return(message)
    # print(IP(message))

def send_msg_to_server(country_code,ip,service_port):
    host = '192.168.1.12'  # as both code is running on same pc
    port = 7777  # socket server port number
    client_socket = socket.socket()  # instantiate
    msg=(country_code,ip,service_port)
    try:
        client_socket.connect((host, port))
        return 0
    except:
        print("not connected")
        return 1
    client_socket.send(msg.encode())


# target_port=22
# ip_range="101.204.0.0-101.207.255.255"

def masscan_ips(target_port,ip_range):
    cmd = ["masscan","-p"+f"{target_port}", "--range", f"{ip_range}"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    while p.poll() is None:
        line = p.stdout.readline().decode('utf-8').strip()
        if bool(line): #jika ada isinya
            print(line)
            # send_msg_to_server(f"__scan__ip:{},port:{}")


# def establish_connection(country_code,port):
#     print("establishing database")
#
#     msg = send_msg_to_server(f"__init__country_code:{country_code},port:{port}")
#     if msg==0:
#         print("success establishing")
#     wait for server respond
#         if server said okay then process





