import socket
import time

import Server

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_host = "10.0.0.1"
server_port = 12000

ping_message = "PING"

def main():
    for i in range(10):
        try:
            send_time = time.time()
            client_socket.sendto(ping_message.encode(), (server_host, server_port))
            client_socket.settimeout(1)
            response, server = client_socket.recvfrom(1024)
            receive_time = time.time()
            sample_rtt = receive_time - send_time
            print(f'Ping {i+1}: Sample RTT = {sample_rtt:.3f} ms')
    
        except socket.timeout:
            print(f'Ping {i+1}: Request timed out')

    client_socket.close()

if __name__ == "__main__":
  main()
