import socket
import threading
import time

# Set global variables
HOST = 'localhost'
PORT = 12000

# Create client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Lists to store client data and server messages
client_list = []
server_messages = []

# Bool to control main loop
open = True

def receive_message():
	while True:
		try:
			# Receive a message from the server
			message = client_socket.recv(1024).decode()
			# to terminate socket with Bye look at last 3 characters of message
			message_end = message[-3:]  #Modified this line to properly read the last 3 characters for bye.- Haris
			#Modified the if statement to also check for "bye" - Haris
			if message_end == "Bye" or message_end == "bye":
				print(message)
				client_socket.send(message.encode())  #Added this line, copied from Line 46 - Haris
				client_socket.close()
				break
			else:
				print(message)

		# Handle exceptions, i.e. a terminated session
		except:
			# print("Session terminated")
			# client_socket.close()
			break	

# Send messages to the server
def write_message():

	while True:

		try:
			# Read a message from the user's input
			message = f'{input("")}'

			# Check if the message ends with "Bye" or "bye" to terminate the connection
			message_end = message[-3:]  #Added this as well - Haris
			if message_end == "Bye" or message_end == "bye":
				client_socket.send(message.encode())
				# client_socket.close()
				break
			client_socket.send(message.encode())
		# Handle exceptions, i.e. a terminated session
		except:
			# print("Session terminated")
			# client_socket.close()
			break

# Thread for receiving messages
receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

# Thread for sending messages
write_thread = threading.Thread(target=write_message)
write_thread.start()
