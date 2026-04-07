import sys
import os
import socket
import ssl
import threading

# Add project root to Python path to import modules if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Server configuration
HOST = '127.0.0.1'
PORT = 12345

# Function to receive messages from server
def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                print("\n[INFO] Server closed connection.")
                client.close()
                break
            print("\n" + message)  # Print with newline to avoid overwriting input
        except Exception as e:
            print(f"\n[ERROR] Disconnected from server: {e}")
            client.close()
            break

# Function to start client
def start_client():
    # Setup SSL context
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    # Create socket and wrap with SSL
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_client = context.wrap_socket(client, server_hostname=HOST)
    secure_client.connect((HOST, PORT))

    print("Connected to secure server 🔐\n")

    # Step-by-step interaction
    while True:
        server_msg = secure_client.recv(1024).decode()
        if not server_msg:
            print("[INFO] Server closed connection.")
            secure_client.close()
            return

        print(server_msg, end="")

        if "chat" in server_msg.lower() or "disconnecting" in server_msg.lower():
            break

        user_input = input()
        secure_client.send(user_input.encode())

    # Step 2: Start receiving messages in a separate thread
    thread = threading.Thread(target=receive_messages, args=(secure_client,), daemon=True)
    thread.start()

    # Step 3: Chat loop
    while True:
        try:
            message = input()
            if message.lower() == "exit":
                print("[INFO] Disconnecting from chat...")
                secure_client.close()
                break
            secure_client.send(message.encode())
        except Exception as e:
            print(f"[ERROR] Connection lost: {e}")
            secure_client.close()
            break

# Run client
if __name__ == "__main__":
    start_client()