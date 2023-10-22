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

with open("common_name.txt", "r") as file:
   SERVER_NAME = file.read()
# Client configuration
SERVER_HOST = SERVER.HOST  # Server's IP address of h4
SERVER_PORT = SERVER.PORT  # Port used by the chat server
print(f'The port number is {SERVER_PORT} and the server name is {SERVER_NAME}.')

context = ssl.create_default_context()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secureClient = context.wrap_socket(client, server_hostname=SERVER_NAME)  # Wrap the socket with SSL
secureClient.connect((SERVER_NAME, SERVER_PORT))

message = input('Input message: ')
secureClient.send(message.encode())
    
response = secureClient.recv(1024)
print('From Server: ', response.decode())
client.close()
