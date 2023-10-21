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

# List to store connected clients
clients = []

# Load the SSL certificate and key
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain("chatserver-cert.pem", "chatserver-key.pem")  # Certificate and file names

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                # Remove the client if unable to send a message
                remove(client)

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            print(f"{message}")
            if not message:
                # Remove disconnected clients
                remove(client_socket)
            else:
                broadcast(message, client_socket)
        except:
            continue

def remove(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', PORT))
    
    # Load the SSL certificate and key
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="chatserver-cert.pem", keyfile="chatserver-key.pem")
    
    # Wrap the server socket in the SSL context
    server = context.wrap_socket(server, server_side=True)

    server.listen()

    print(f"Server is listening on port {PORT}")

    while True:
        client_socket, client_address = server.accept()
        secureConnSocket = context.wrap_socket(client_socket, server_side=True)
        clients.append(client_socket)

        print(f"Client {client_address[0]}:{client_address[1]} connected")
        client_thread = threading.Thread(target=handle_client, args=(secureConnsocket,))
        client_thread.start()

if __name__ == "__main__":
    main()
