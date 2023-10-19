import socket
import threading

# Client configuration
SERVER_HOST = '127.0.0.1'  # Server's IP address *DOUBLE CHECK WHEN RUN*
SERVER_PORT = 12345  # Port used by the chat server

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
    client.connect((SERVER_HOST, SERVER_PORT))

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    while True:
        message = input()
        client.send(message.encode('utf-8'))

if __name__ == "__main__":
    main()
