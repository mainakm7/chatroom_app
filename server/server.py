import threading
import socket

HOST = "localhost"
PORT = 12345

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind((HOST, PORT))
SERVER.listen()

clients = {}  # Changed to a dictionary to map nicknames to clients

def broadcast_msg(message, sender_nickname):
    for nickname, client in clients.items():
        if nickname != sender_nickname:
            try:
                client.send(message.encode("utf-8"))
            except Exception as e:
                print(f"Error sending message to {nickname}: {e}")

def send_private_msg(message, sender_nickname, recipient_nickname):
    recipient_client = clients.get(recipient_nickname)
    if recipient_client:
        try:
            recipient_client.send(f"Private from {sender_nickname}: {message}".encode("utf-8"))
        except Exception as e:
            print(f"Error sending private message to {recipient_nickname}: {e}")
    else:
        sender_client = clients.get(sender_nickname)
        if sender_client:
            sender_client.send(f"{recipient_nickname} is not connected.".encode("utf-8"))

def client_handler(client, nickname):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message.startswith("/private"):
                parts = message.split(' ', 2)
                recipient_nickname = parts[1]
                private_message = parts[2]
                send_private_msg(private_message, nickname, recipient_nickname)
            else:
                broadcast_msg(f"{nickname}: {message}", nickname)
        except Exception as e:
            print(f"Error handling client {nickname}: {e}")
            clients.pop(nickname)
            client.close()
            broadcast_msg(f"{nickname} has left the chat", nickname)
            break

def main():
    print(f"Server is listening on {HOST}:{PORT}")
    try:
        while True:
            client, address = SERVER.accept()
            print(f"Client joined from address: {address}")

            client.send("NICKNAME".encode("utf-8"))
            nickname = client.recv(1024).decode("utf-8")

            clients[nickname] = client
            print(f"Nickname of the client is {nickname}")

            broadcast_msg(f"{nickname} joined the chat", nickname)

            client_thread = threading.Thread(target=client_handler, args=(client, nickname))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        for client in clients.values():
            client.close()
        SERVER.close()

if __name__ == "__main__":
    main()
