import threading
import socket

SERVER_HOST = "localhost"   # Put the public IP of the server
SERVER_PORT = 12345

CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENT.connect((SERVER_HOST, SERVER_PORT))

nickname = input("Choose a nickname: ")

def receive_message():
    while True:
        try:
            message = CLIENT.recv(1024).decode("utf-8")
            if message == "NICKNAME":
                CLIENT.send(nickname.encode("utf-8"))
            else:
                print(message)
        except Exception as e:
            print(f"Error encountered: {e}")
            CLIENT.close()
            break

def write_message():
    while True:
        try:
            message = input()
            CLIENT.send(message.encode("utf-8"))
        except Exception as e:
            print(f"Error encountered: {e}")
            CLIENT.close()
            break

def main():
    receive_thread = threading.Thread(target=receive_message)
    receive_thread.start()
    write_thread = threading.Thread(target=write_message)
    write_thread.start()

if __name__ == "__main__":
    main()
