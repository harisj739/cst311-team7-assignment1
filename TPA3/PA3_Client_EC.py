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
			message_end = message[10:]
			if message_end == "Bye":
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

			if message == "Bye":
				client_socket.send("Bye".encode())
				client_socket.close()
				break

			client_socket.send(message.encode())

		except:
			print("Session terminated")
			client_socket.close()


receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

write_thread = threading.Thread(target=write_message)
write_thread.start() 			
