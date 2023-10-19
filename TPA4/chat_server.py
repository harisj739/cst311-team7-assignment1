import socket
import threading

# Server configuration
HOST = '0.0.0.0'  # Listen on all available network interfaces
PORT = 12345  # Port for the chat server

# List to store connected clients
clients = []

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
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server is listening on port {PORT}")

    while True:
        client_socket, client_address = server.accept()
        clients.append(client_socket)
        print(f"Client {client_address[0]}:{client_address[1]} connected")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    main()
