import socket
import threading
import os
import time

def writing_thread(client_socket, server_host, server_port, my_name):
    client_socket.connect((server_host, server_port))
    conn = client_socket

    # Send name first
    conn.sendall(my_name.encode())


    while True:
        message = input("")
        conn.sendall(message.encode())

        # Print an indication that a message has been sent
        

        if message.startswith("transfer "):
            filename = message.split()[1]
            if os.path.exists(filename):
                print(f"Sending file '{filename}'...")
                conn.sendall(f"FILE {filename} {os.path.getsize(filename)}".encode())  # Send file header
                with open(filename, 'rb') as f:
                    while True:
                        data = f.read(1024)
                        conn.sendall(data)
                        if not data:
                            break
                print(f"File '{filename}' successfully sent.")
            else:
                print("File not found.")


def main():

    name = input('Whats your name: ')

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 0))
    server_port = server_socket.getsockname()[1]
    print(f"Listening on port: {server_port}")
    server_socket.listen()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    server_host = 'localhost'
    server_port = int(input("Enter the server port: "))  # Use the port number shown by the server
    
    
    # Receive the initial connection confirmation message from the server
  
    # Start threads for both client and server
   
    writing = threading.Thread(target=writing_thread , args=(client_socket , server_host , server_port ,name,))
    writing.start()
    
    conn, addr = server_socket.accept()
    
    data = conn.recv(1024)
    client_name = data.decode()

    print(f"Connected to {client_name}")

    while True:
        data = conn.recv(1024)
        if not data:
            print("Connection closed.")
            break

        message = data.decode()  # Decode the received data

        # Indicate that a message has been received
        if message.startswith("FILE "):
            filename = "new" + message.split()[1]
            size = int(message.split()[2])
            i = 0
            print(f"Receiving file '{filename}'...")
            with open(filename, 'wb') as f:
                while True:
                    data = conn.recv(1024)
                    i += len(data)
                    f.write(data)
                    
                    if i == size:  # transfer complete
                        break
                    

            print(f"File '{filename}' successfully received.")
        else:
            print(f" {client_name}: {message}")



if __name__ == "__main__":
    main()
