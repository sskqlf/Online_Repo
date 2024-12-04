import socket

# 사용자 데이터베이스 (단순 예제)
USER_DB = {
    "user1": "password1",
    "user2": "password2",
    "admin": "admin123"
}

def handle_client(client_socket):
    try:
        client_socket.send(b"Username: ")
        username = client_socket.recv(1024).decode().strip()

        client_socket.send(b"Password: ")
        password = client_socket.recv(1024).decode().strip()

        if username in USER_DB and USER_DB[username] == password:
            client_socket.send(b"Login successful!\n")
        else:
            client_socket.send(b"Invalid username or password.\n")
    finally:
        client_socket.close()

def start_server(host='0.0.0.0', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server()
