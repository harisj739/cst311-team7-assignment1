'''
Team 7
Andrew Grant
Anthony Matricia
Haris Jilani
'''

import threading
import socket

HOST = 'localhost'
PORT = 12000

#creating socket connection
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

#lists to hold client sockets and names of each like Client X, Client Y
client_list = []
client_names = []

#send message to all connected clients
def broadcast(message):
	for client in client_list:
		client.send(message)

def connection_handler(client, count):
	while True:
		try:
			#receive message, reformat and broadcast to all clients
			message = client.recv(1024).decode()
			server_response = f"{client_names[count]}: {message}"
			broadcast(server_response.encode())

		except:
			print("Exception occurred")
			client.close()
			break


def main():
	count = 0
	while True:	
		#accept socket connection to establish client socket and address
		client, address = server_socket.accept()
		
		# Modified the welcome message	
		client.send("Welcome to the chat! To send a message, type the message and click enter.".encode("ascii"))	
		
		#makes sure first connection is Client X
		if count == 0:
			#add Client X to name
			client_names.append("Client X")
			print(f"Connected to Client X at {str(address)}")
			
			#add client socket to client_list
			client_list.append(client)

			#creating thread and passing the function the client socket and count variable 
			thread = threading.Thread(target=connection_handler, args=(client,count))
			thread.start()	
		
		if count == 1:
			client_names.append("Client Y")
			print(f"Connected to Client Y at {str(address)}")
			client_list.append(client)

			#creating second additional thread
			thread = threading.Thread(target=connection_handler, args=(client,count))
			thread.start()	

		count += 1




if __name__ == "__main__":
	print(f"Server is listening on Port {PORT}")
	main()
