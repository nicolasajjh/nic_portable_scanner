from constant import ip_regex
import re
def extract_ip_port(msg):
    ip= re.search(ip_regex, msg).group()
    port=re.search("\d+",msg).group()
    return ip,port
# print(f"current process = {active_count()}")
# ip_tes()
line="Discovered open port 22/tcp on 1.53.252.124"
print("check--------------------")
ip,port=extract_ip_port(line)
print(ip,port)
