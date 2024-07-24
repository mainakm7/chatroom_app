import threading
import socket


HOST = "localhost"
PORT = 12345

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind((HOST, PORT))
SERVER.listen()

clients, nicknames = [], []

def broadcast_msg(message):
    for client in clients:
        try:
            client.send(message.encode("utf-8"))
        except Exception as e:
            print(f"Error sending message to {client}: {e}")

def client_handler(client):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            broadcast_msg(message)
        except Exception as e:
            print(f"Error handling client {client}: {e}")
            client_index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[client_index]
            broadcast_msg(f"{nickname} has left the chat")
            nicknames.remove(nickname)
            break

def main():
    print(f"Server is listening on {HOST}:{PORT}")
    try:
        while True:
            print("Server is listening")
            client, address = SERVER.accept()
            print(f"Client joined from address: {address}")

            client.send("NICKNAME".encode("utf-8"))
            nickname = client.recv(1024).decode("utf-8")

            clients.append(client)
            nicknames.append(nickname)
            print(f"Nickname of the client is {nickname}")

            broadcast_msg(f"{nickname} joined the chat")

            client_thread = threading.Thread(target=client_handler, args=(client,))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        for client in clients:
            client.close()
        SERVER.close()

if __name__ == "__main__":
    main()
