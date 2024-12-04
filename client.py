import socket

def start_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, server_port))

        while True:
            response = client_socket.recv(1024).decode()
            if not response:
                break
            print(response, end="")

            user_input = input()
            client_socket.send(user_input.encode())
    finally:
        client_socket.close()

if __name__ == "__main__":
    server_ip = input("Enter server IP: ")
    server_port = int(input("Enter server port: "))
    start_client(server_ip, server_port)
