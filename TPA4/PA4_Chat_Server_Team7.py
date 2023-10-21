"""Chat client for CST311 Programming Assignment 4"""
__author__ = "Team 7 - SSS"
__credits__ = [
  "Andrew Grant",
  "Anthony Matricia",
  "Haris Jilani"
]

import socket
import threading
import ssl  # Import the SSL module
import time

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Server configuration
HOST = '10.0.1.2'  # Listen on all available network interfaces
PORT = 2223  # Port for the chat server

# The context is the TLS Protocol.
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="chatserver-cert.pem", keyfile="chatserver-key.pem")

def handle_client(thread, client_socket, secure_socket, addr, clients):
        try:
            message = secure_socket.recv(1024).decode()
            
            # Log query information
            log.info("Connected to client at " + str(addr))
  	    # makes first client to respond first in host_list and sets to X
            if thread == 0:
                clients.append(f"X : \"{message}\" ")  
            else:
                clients.append(f"Y : \"{message}\" ")

            log.info(f"Received query test \" {message} \" ")

  	    #make sure list has two elements, if not insert short delay
            while len(clients) < 2:
                time.sleep(5)

	    #combine client messages into single response
            response = f"{clients[0]}, {clients[1]}"
            secure_socket.send(response.encode())
            secure_socket.close()
            # client_socket.close()
        except:
            secure_socket.close()
            client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', PORT))
    
    clients = []
   
    server.listen(5)

    print(f"Server is listening on port {PORT}")
    
    try:
         for i in range(2):
    	        # When a client connects, create a new socket and record their address
                client_socket, client_address = server.accept()
                print("The i value is: ", i)
                log.info("Connected to at " + str(client_address))
        	# Uses the context to establish a secure TCP socket laced with TLS.
                secureConnSocket = context.wrap_socket(client_socket, server_side=True)
        	
        	# Pass the new socket and address off to a connection handler function in a thread.
      		# Here we create a thread for each secure TCP connection established:
                threading.Thread(target=handle_client, args=(i, client_socket, secureConnSocket, client_address, clients)).start()
                client_socket.close()
    
    finally: 
    	 server.close()
if __name__ == "__main__":
    main()
