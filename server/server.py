import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# IMPORT REQUIRED LIBRARIES
import ssl        #FOR SECURE COMMUNICATION
import socket     #FOR NETWORK COMMUNICATION
import threading  #FOR HANDLING MULTIPLE CLIENTS SIMULTANEOUSLY

#IMPORT AUTHENTICATION FUNCTIONS
from utils.auth import register_user, login_user

#IMPORT DATABASE FUNCTION TO STORE MESSAGES
from database.db import save_message

# SERVER ADDRESS
HOST = '127.0.0.1'
PORT = 12345

# STORE CONNECTED CLIENTS
clients = []

# FUNCTION TO HANDLE EACH CONNECTED CLIENT
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    try:
        conn.send("Welcome! Type REGISTER or LOGIN: ".encode())
        choice = conn.recv(1024).decode().strip().upper()
        if not choice:
            conn.send("No option received. Disconnecting.\n".encode())
            conn.close()
            return

        conn.send("Username: ".encode())
        username = conn.recv(1024).decode().strip()
        if not username:
            conn.send("No username received. Disconnecting.\n".encode())
            conn.close()
            return

        conn.send("Password: ".encode())
        password = conn.recv(1024).decode().strip()
        if not password:
            conn.send("No password received. Disconnecting.\n".encode())
            conn.close()
            return

        if choice == "REGISTER":
            if register_user(username, password):
                conn.send("Registration successful! You can now chat.\n".encode())
            else:
                conn.send("Username already exists. Disconnecting.\n".encode())
                conn.close()
                return

        elif choice == "LOGIN":
            if login_user(username, password):
                conn.send("Login successful! You can now chat.\n".encode())
            else:
                conn.send("Invalid credentials. Disconnecting.\n".encode())
                conn.close()
                return
        else:
            conn.send("Invalid option. Disconnecting.\n".encode())
            conn.close()
            return

        # Add authenticated client
        clients.append(conn)
        broadcast(f"{username} joined the chat!", conn)

        while True:
            message = conn.recv(1024).decode()
            if not message:
                break

            full_message = f"{username}: {message}"
            print(full_message)

            # SAVE TO DATABASE
            save_message(username, message)

            broadcast(full_message, conn)

    except Exception as e:
        import traceback
        print(f"[ERROR] {addr}")
        traceback.print_exc()

    finally:
        if conn in clients:
            clients.remove(conn)
        conn.close()
        print(f"[DISCONNECTED] {addr}")

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
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="ssl_cert.pem", keyfile="ssl_key.pem")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = context.wrap_socket(server, server_side=True)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[LISTENING] Server running on {HOST}:{PORT}")

    #ACCEPTS CLIENT CONTINOUSLY 
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

# RUN SERVER
if __name__ == "__main__":
    start_server()