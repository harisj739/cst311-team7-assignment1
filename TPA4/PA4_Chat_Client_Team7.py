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
import PA4_Chat_Server_Team7 as SERVER
# from certificate_generation import chat_server_common_name

with open("common_name.txt", "r") as file:
    SERVER_NAME = file.read()
# Client configuration
SERVER_HOST = SERVER.HOST  # Server's IP address of h4
SERVER_PORT = SERVER.PORT  # Port used by the chat server

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            # Handle connection errors or server disconnection
            print("Connection to the server is lost.")
            client_socket.close()
            break

def main():
    context = ssl.create_default_context()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secureClient = context.wrap_socket(client, server_hostname=SERVER_NAME)  # Wrap the socket with SSL
    secureClient.connect((SERVER_NAME, SERVER.PORT))

    receive_thread = threading.Thread(target=receive_messages, args=(secureClient,))
    receive_thread.start()

    while True:
        message = input("Input a lowercase sentence: ")
        client.send(message.encode())

if __name__ == "__main__":
    main()
