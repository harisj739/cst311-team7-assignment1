#!env python

"""Chat server for CST311 Programming Assignment 3"""
__author__ = "Team 7"
__credits__ = [
  "Haris Jilani",
  "Anthony Matricia",
  "Andrew Grant"
]

import socket as s
import time
import threading

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

server_port = 12000


def connection_handler(thread, connection_socket, address, host_list):
  # Read data from the new connectio socket
  #  Note: if no data has been sent this blocks until there is data
  query = connection_socket.recv(1024).decode()
  
  # Log query information
  log.info("Connected to client at " + str(address) ) 

  # makes first client to respond first in host_list and sets to X
  if thread == 0:
    host_list.append(f"X : \"{query}\" ")  
  else:
    host_list.append(f"Y : \"{query}\" ")

  log.info(f"Received query test \" {query} \" ")

  #make sure list has two elements, if not insert short delay
  while len(host_list) < 2:
    time.sleep(1)

  #combine client messages into single response
  response = f"{host_list[0]}, {host_list[1]}"
  
  # Sent response over the network, encoding to UTF-8
  connection_socket.send(response.encode())
  
  # Close client socket
  connection_socket.close()
  

def main():
  # Create a TCP socket
  # Notice the use of SOCK_STREAM for TCP packets

  server_socket = s.socket(s.AF_INET,s.SOCK_STREAM)
  
  # Assign IP address and port number to socket, and bind to chosen port

  server_socket.bind(('',server_port))
  
  # Configure how many requests can be queued on the server at once

  server_socket.listen(1)
  
  # Alert user we are now online
  log.info("The server is ready to receive on port " + str(server_port))

  #declare emtpy list
  host_list = []
  
  # Surround with a try-finally to ensure we clean up the socket after we're done
  try:

    #for loop to create two threads and establish two connections
    for i in range(2):

      # When a client connects, create a new socket and record their address
      connection_socket, address = server_socket.accept()
      log.info("Connected to at " + str(address))

      # Pass the new socket and address off to a connection handler function in a thread.
      # Here we create a thread for each TCP connection established: 
      threading.Thread(target=connection_handler, args=(i, connection_socket, address, host_list)).start()
 
      # connection_handler(connection_socket, address) -> commented out for lines above ^
  finally:
    server_socket.close()

if __name__ == "__main__":
  main()
