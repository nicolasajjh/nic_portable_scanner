import socket
def send_msg_to_server(country_code,ip,service_port):
    server_ip = '192.168.1.12'  # as both code is running on same pc
    server_port = 7777  # socket server port number
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    msg=(f"{country_code};{ip};{service_port}")
    # try:
    client_socket.connect((server_ip,server_port))
    client_socket.send(msg.encode())
    # return 0
    # except:
    #     print("not connected")
    #     return 1
    # client_socket.close()

if __name__ == '__main__':
    send_msg_to_server("vn","123","123")
