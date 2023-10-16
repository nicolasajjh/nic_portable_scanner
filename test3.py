import subprocess

cmd = ["masscan","-p22", "--range", f"{'192.168.1.1-192.168.1.254'}"]
with subprocess.Popen(cmd,stdout=subprocess.PIPE) as p:

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
            insert_ip(country_code,ip,port)
    p.wait()