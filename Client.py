import socket
import time

import Server

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create the UDP socket

server_host = "10.0.0.1" # IP
server_port = 12000 # Port number

ping_message = "PING" # Ping message
ALPHA = 0.125 #Used to calculate estimated RTT
BETA = 0.25 #Used to calculate deviation RTT

def main():
    min_rtt = float('inf')  # Initialize min_rtt
    max_rtt = 0  # Initialize max_rtt
    total_rtt = 0  # Initialize total_rtt
    successful_pings = 0 # Initialize the number of pings that didnt timeout
    estimated_rtt = 0 #Intialize the estimated RTT value
    dev_rtt = 0 #Initialize the deviation RTT value
    prevEstimated_rtt = 0 #Keeps track of the previous estimated RTT value used to calculate the new estimated RTT value
    prevDev_rtt = 0 #Keeps track of the previous deviation RTT value used to calculate the new deviation RTT value
    timeout_interval = 0 #Initialize the timeout interval
    
    for i in range(10): # 10 ping trials
        try:
            send_time = time.time() # Record time and store it in send_time
            client_socket.sendto(ping_message.encode(), (server_host, server_port)) # Send request
            client_socket.settimeout(1) # Set timeout for receiving request
            response, server = client_socket.recvfrom(1024) # Receive request
            receive_time = time.time() # Record time and store it in receive_time
            sample_rtt = receive_time - send_time # Subtract to find how much time it took
            
            # The following code calculates the estimated RTT and deviation RTT using the given formulas.
            # The initial estimated and deviation RTT differ as both values are dependent on the 
            # previous values of estimated and deviation RTT. We simply use the sample RTT as our 
            # estimated RTT in this case, and the deviation RTT is half of the sample RTT.
            if i == 0:
            	estimated_rtt = sample_rtt
            	dev_rtt = sample_rtt/2
            else:
            	estimated_rtt = (1 - ALPHA) * prevEstimated_rtt + ALPHA * sample_rtt
            	dev_rtt = (1 - BETA) * prevDev_rtt + BETA * abs(sample_rtt - estimated_rtt) 
            
            print(f'Ping {i+1}: Sample RTT = {sample_rtt:.3f} ms, Estimated RTT = {estimated_rtt:.3f} ms, Dev RTT = {dev_rtt:.3f} ms')
            prevEstimated_rtt = estimated_rtt
            prevDev_rtt = dev_rtt
            
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
    
    # Using the last estimated RTT and deviation RTT values, 
    # we calculatethe timeout interval using the following formula:
    timeout_interval = estimated_rtt + (4 * dev_rtt)
    
    print(f'Summary Values: ')
    print(f'Min RTT = {min_rtt:.3f} ms')
    print(f'Max RTT = {max_rtt:.3f} ms')
    print(f'Average RTT = {average_rtt:.3f} ms')
    print(f'Timeout Interval = {timeout_interval:.3f} ms')
    
if __name__ == "__main__":
  main()
