import threading
import socket

HOST = 'localhost'
PORT = 12000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

client_list = []
client_names = []

def broadcast(message):
	for client in client_list:
		client.send(message)

def connection_handler(client, count):

	while True:
		try:
			message = client.recv(1024).decode()
			server_response = f"{client_names[count]}: {message}"
			broadcast(server_response.encode())

		except:
			print("Exception occurred oh no")
			client.close()
			break


def main():
	count = 0
	while True:	
	
		client, address = server_socket.accept()
		client.send("Welcome to the chat".encode("ascii"))	
		
		#makes sure first connection is Client X
		if count == 0:
			client_names.append("Client X")
			print(f"Connected to Client X at {str(address)}")
			client_list.append(client)
			thread = threading.Thread(target=connection_handler, args=(client,count))
			thread.start()	
		
		if count == 1:
			client_names.append("Client Y")
			print(f"Connected to Client Y at {str(address)}")
			client_list.append(client)
			thread = threading.Thread(target=connection_handler, args=(client,count))
			thread.start()	

		count += 1




if __name__ == "__main__":
	print(f"Server is listening on Port {PORT}")
	main()






