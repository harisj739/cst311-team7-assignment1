import socket
import time

import Server

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create the UDP socket

server_host = "10.0.0.1" # IP
server_port = 12000 # Port number

ping_message = "PING" # Ping message

def main():
    min_rtt = float('inf')  # Initialize min_rtt
    max_rtt = 0  # Initialize max_rtt
    total_rtt = 0  # Initialize total_rtt
    successful_pings = 0 # Initialize the number of pings that didnt timeout
    
    for i in range(10): # 10 ping trials
        try:
            send_time = time.time() # Record time and store it in send_time
            client_socket.sendto(ping_message.encode(), (server_host, server_port)) # Send request
            client_socket.settimeout(1) # Set timeout for receiving request
            response, server = client_socket.recvfrom(1024) # Receive request
            receive_time = time.time() # Record time and store it in receive_time
            sample_rtt = receive_time - send_time # Subtract to find how much time it took
            print(f'Ping {i+1}: Sample RTT = {sample_rtt:.3f} ms') # Output sample RTT
            
            # Update min_rtt, max_rtt, and the total rtt which will be used to calculate the average
            min_rtt = min(min_rtt, sample_rtt)
            max_rtt = max(max_rtt, sample_rtt)
            total_rtt += sample_rtt
            successful_pings += 1
    
        except socket.timeout:
            print(f'Ping {i+1}: Request timed out') # Catch timeout exception and print

    client_socket.close() # Close socket
    
    # Calculate average RTT and Print summary values
    average_rtt = total_rtt / successful_pings if total_rtt > 0 else 0
    print(f'Summary Values: ')
    print(f'Min RTT = {min_rtt:.3f} ms')
    print(f'Max RTT = {max_rtt:.3f} ms')
    print(f'Average RTT = {average_rtt:.3f} ms')

if __name__ == "__main__":
  main()
