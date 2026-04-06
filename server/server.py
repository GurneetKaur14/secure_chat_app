import socket
import threading

# SERVER ADDRESS
HOST = '127.0.0.1'
PORT = 12345

# STORE CONNECTED CLIENTS
clients = []

# HANDLING EACH CLIENT
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    clients.append(conn)

# RECEIVEING MESSAGES
    while True:
        try:
            message = conn.recv(1024).decode()
            if not message:
                break

            print(f"[{addr}] {message}")
            broadcast(message, conn)

        except:
            break

    print(f"[DISCONNECTED] {addr}")
    clients.remove(conn)
    conn.close()

# BROADCASTING MESSAGE
def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(message.encode())
            except:
                client.close()
                clients.remove(client)

# STARTING SERVER
def start_server():
    # CREATING SOCKET
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[LISTENING] Server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()