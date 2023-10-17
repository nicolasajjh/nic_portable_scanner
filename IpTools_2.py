
from math import ceil
from ipaddress import IPv4Address as ipv4
from IpTools import *

def ip_range(ip1,ip2):
    ipv4_range=str(ip1)+'-'+str(ip2)
    return ipv4_range
def extract_ip_from_str_range(range):
    ip1, ip2 = range.split("-")
    print(ip1, ip2)
    return ip1, ip2

def total_ips_in_range(ip1, ip2):
    total_ip = int(ipv4(ip2)) - int(ipv4(ip1))
    return total_ip


def total_ips_in_str_range(range):
    ip_1, ip_2 = extract_ip_from_str_range(range)
    return total_ips_in_range(ip_1, ip_2)

def ip_range_splitter(country_code,hosts_per_thread):
    # hosts_per_thread = 200000
    # country_code = "vn"
    total_threads = ceil(total_ip_by_country_code(country_code) / hosts_per_thread)
    # print(total_threads)
    t=[]
    country_networks = networks(country_code)
    # print(len(country_networks))
    index_inet=0
    # for network in country_networks:
    #     print(index_inet, network.ip_range)
    #     index_inet+=1

    next_range=True
    # print("init")
    tmp_ip_range_list=[]
    tmp_hosts_per_thread=hosts_per_thread
    i=0 #thread indexer
    def submit():
        t.append(tmp_ip_range_list)
    while i <= total_threads:
        if next_range==True:

            # print(index_inet)
            first_ip = country_networks[index_inet].first_ip
            last_ip = country_networks[index_inet].last_ip


        total_ip_in_range=total_ips_in_range(first_ip,last_ip)
        # print(total_ip_in_range)
        if tmp_hosts_per_thread>=total_ip_in_range:
            tmp_ip_range_list.append(ip_range(first_ip,last_ip))
            tmp_hosts_per_thread-=total_ip_in_range
            next_range=True
            if index_inet != len(country_networks) - 1:
                index_inet += 1
            else:
                submit()#submit
                break

        else:
            next_ip=ipv4(first_ip)+tmp_hosts_per_thread
            tmp_ip_range_list.append(ip_range(first_ip,next_ip))
            first_ip=ipv4(next_ip)+1
            next_range=False #artinya belum habis, next thread = true
            submit()
            tmp_ip_range_list = []
            tmp_hosts_per_thread = hosts_per_thread
            i+=1

    return t


def range_checker(ranges):
    total = 0
    index = 0
    for range_list in ranges:

        total_ips = 0
        for range in range_list:
            total_ips += total_ips_in_str_range(range)
        print("total = ", total_ips)
        total += total_ips
        index += 1
    print("total = ", total, index)


if __name__ =="__main__":
    ranges=ip_range_splitter(200000,"vn")
