import socket
import threading
import time

HOST = 'localhost'
PORT = 12000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

client_list = []
server_messages = []

open = True

def receive_message():
	while True:
		try:
			message = client_socket.recv(1024).decode()
		
			# to terminate socket with Bye look at last 3 characters of message
			message_end = message[-3:]  #Modified this line to properly read the last 3 characters for bye.- Haris
			#Modified the if statement to also check for "bye" - Haris
			if message_end == "Bye" or message_end == "bye":
				client_socket.send(message.encode())  #Added this line, copied from Line 46 - Haris
				client_socket.close()
				break
			else:
				print(message)


		except:
			print("Session terminated")
			client_socket.close()
			break	


def write_message():

	while True:

		try:
			message = f'{input("")}'

			message_end = message[-3:]  #Added this as well - Haris
			if message_end == "Bye" or message_end == "bye":
				client_socket.send(message.encode())
				client_socket.close()
				break
			client_socket.send(message.encode())

		except:
			print("Session terminated")
			client_socket.close()
			break


receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

write_thread = threading.Thread(target=write_message)
write_thread.start()
