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

# Client configuration
SERVER_HOST = '10.0.1.2'  # Server's IP address of h4
SERVER_PORT = 2223  # Port used by the chat server

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            # Handle connection errors or server disconnection
            print("Connection to the server is lost.")
            client_socket.close()
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client = ssl.wrap_socket(client, ssl_version=ssl.PROTOCOL_TLS_CLIENT)  # Wrap the socket with SSL

    client.connect((SERVER_HOST, SERVER_PORT))

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    while True:
        message = input()
        client.send(message.encode('utf-8'))

if __name__ == "__main__":
    main()
