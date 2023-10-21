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

# Server configuration
HOST = '10.0.1.2'  # Listen on all available network interfaces
PORT = 2223  # Port for the chat server

# Load the SSL certificate and key
# context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# context.load_cert_chain("chatserver-cert.pem", "chatserver-key.pem")  # Certificate and file names

def broadcast(message, client_socket):
       client_socket.send(message.encode())
       # Close the client if unable to send a message
       remove(client_socket)

def handle_client(client_socket):
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                # Remove disconnected clients
                remove(client_socket)
            else:
                broadcast(message, client_socket)
        except:
            close(client_socket)

def close(client_socket):
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', PORT))
    
    # Load the SSL certificate and key
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="chatserver-cert.pem", keyfile="chatserver-key.pem")
   

    server.listen()

    print(f"Server is listening on port {PORT}")

    while True:
        client_socket, client_address = server.accept()
        secureConnSocket = context.wrap_socket(client_socket, server_side=True)

        print(f"Client {client_address[0]}:{client_address[1]} connected")
        client_thread = threading.Thread(target=handle_client, args=(secureConnSocket,))
        client_thread.start()

if __name__ == "__main__":
    main()
