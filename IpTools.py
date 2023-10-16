"""
    Operations based around ip.
    Copyright (C) 2020  Dimitrije Karanfilović
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

from pathlib import Path

def dot_decimal_to_binary(address):
    list_of_parts = address.split(".")
    res = ""
    for part in list_of_parts:
        p = from_decimal_to_binary(int(part))
        res += str(p)
    return res


def from_decimal_to_binary(n):
    res = ""
    while True:
        digit = n % 2
        res += str(digit)
        n = n // 2
        if n == 0:
            break
    if len(res) < 8:
        while True:
            res += "0"
            if len(res) == 8:
                break
    return res[-1::-1]


def count_ones(net_mask):
    mask_list = net_mask.split(".")
    res = ""
    for elem in mask_list:
        part = from_decimal_to_binary(int(elem))
        res += part
    count = 0
    for i in range(len(res)):
        if res[i] == "1":
            count += 1
    return count


def binary_to_dot_decimal(binary_number):
    res = ""
    low = 0
    high = 8
    for i in range(4):
        part = binary_number[low:high]
        _help = int(part, 2)
        res += str(_help)
        res += "."
        low += 8
        high += 8
    return res.strip(".")


def make_net_mask(number_of_ones):
    curr = ""
    for i in range(number_of_ones):
        curr += "1"
    if len(curr) < 32:
        while True:
            curr += "0"
            if len(curr) == 32:
                break
    return binary_to_dot_decimal(curr)


def make_broadcast_mask(net_mask):
    mask_parts = net_mask.split(".")
    res = ""
    for i in range(4):
        part = int(mask_parts[i]) ^ 0xff
        res += str(part)
        res += "."
    return res.strip(".")


def calculate_net_id(ip, mask):
    ip_parts = ip.split(".")
    mask_parts = mask.split(".")
    res = ""
    for i in range(4):
        part = int(ip_parts[i]) & int(int(mask_parts[i]))
        res += str(part)
        res += "."
    return res.strip(".")


def calculate_broadcast_address(ip, net_mask):
    broadcast_mask = make_broadcast_mask(net_mask)
    broad_parts = broadcast_mask.split(".")
    ip_parts = ip.split(".")
    res = ""
    for i in range(4):
        part = int(ip_parts[i]) | int(broad_parts[i])
        res += str(part)
        res += "."
    return res.strip(".")


def max_hosts(number_of_ones):
    return 2 ** (32 - number_of_ones) - 2


def calculate_all_parameters(ip, net_mask):
    ip_id = calculate_net_id(ip, net_mask)
    ip_id_parts = ip_id.split(".")
    ip_id_parts[3] = str(int(ip_id_parts[3]) + 1)

    broadcast = calculate_broadcast_address(ip, net_mask)
    broadcast_parts = broadcast.split(".")
    broadcast_parts[3] = str(int(broadcast_parts[3]) - 1)

    first = ""
    last = ""
    for i in range(4):
        first += ip_id_parts[i]
        last += broadcast_parts[i]
        first += "."
        last += "."
    first = first.strip(".")
    last = last.strip(".")

    max_number_of_hosts = max_hosts(count_ones(net_mask))
    return ip_id, first, last, broadcast, max_number_of_hosts

def ipv4_net_list_by_country(country_code):
    # dir_path=Path(__file__).parents[1]
    # country_code="sg"
    ip_list_path=(fr"country/{country_code.lower()}/ipv4-aggregated.txt")
    file=open(ip_list_path,'r')
    lines=file.readlines()
    inet_list=[]

    for line in lines:
        line=line.strip()
        if "#" not in line:
            inet_list.append(line)
    return inet_list

def get_ip_netmask_by_inet(inet):
    ip,net_mask=inet.split("/")
    net_mask=net_decimal_to_real_netmask(net_mask)
    return ip, net_mask

def max_hosts_by_inet(inet):
    ip,net_mask=get_ip_netmask_by_inet(inet)
    # net_mask=net_decimal_to_real_netmask(net_mask)
    # print("netmask =",net_mask)
    max_number_of_hosts = max_hosts(count_ones(net_mask))
    return max_number_of_hosts

def total_ip_by_country_code(country_code):
    inet_list = ipv4_net_list_by_country(country_code)
    total_ips=0
    for inet in inet_list:
        total_ips+=max_hosts_by_inet(inet)
    return total_ips

class network_info():
    def __init__(self,inet):
        self.ip, self.net_mask=get_ip_netmask_by_inet(inet)
        self.network_ip,self.first_ip,self.last_ip,self.broadcast,self.max_hosts=calculate_all_parameters(self.ip,self.net_mask)
        self.ip_range=self.first_ip+'-'+self.last_ip
def networks(country_code):

    tmp_list=[]
    inet_list = ipv4_net_list_by_country(country_code)
    for inet in inet_list:
        tmp_list.append(network_info(inet))
    return tmp_list

def split_address(ip_address, number_of_ones):
    mask = make_net_mask(number_of_ones)
    net_id = calculate_all_parameters(ip_address, mask)[0]
    binary = dot_decimal_to_binary(net_id)
    address1 = ""
    address2 = ""
    for i in range(len(binary)):
        if i == number_of_ones:
            address1 += "1"
            address2 += "0"
        address1 += str(binary[i])
        address2 += str(binary[i])

    address1 = binary_to_dot_decimal(address1)
    address2 = binary_to_dot_decimal(address2)

    paramaters1 = calculate_all_parameters(address1, make_net_mask(number_of_ones + 1))
    paramaters2 = calculate_all_parameters(address2, make_net_mask(number_of_ones + 1))
    return paramaters1, paramaters2

# def max_hosts_by_ip_netmask(ip,netmask):

#def get_ipv4_list_by_country(country_code):
#     python path
# def read_from_txt

def net_decimal_to_real_netmask(net):
    list = net.split(".")
    if len(list) < 4:
        net = make_net_mask(int(net))
        return net

if __name__ == "__main__":
    ip = input("Enter ip: ")
    net = input("Enter number of ones or net mask: ")
    net= net_decimal_to_real_netmask(net)
    a = calculate_all_parameters(ip, net)
    for elem in a:
        print(elem)
