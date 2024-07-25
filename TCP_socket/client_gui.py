import threading
import socket
import tkinter as tk
from tkinter import scrolledtext, simpledialog

SERVER_HOST = "192.168.1.156"  # Change to the server's public IP if needed
SERVER_PORT = 12345

class Client:
    def __init__(self, host, port):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect((host, port))
        
        self._nickname = self.nickname()
        
        self.running = True
        self.gui_done = False
        self.chatbox = None
        
        self.stop_event = threading.Event()
        
        # Start the receiving messages thread
        self.receive_thread = threading.Thread(target=self.receive_msg)
        self.receive_thread.start()

        # Start the GUI in the main thread
        self.gui()

    def nickname(self):
        temp_root = tk.Tk()
        temp_root.withdraw()  
        nickname = simpledialog.askstring("Nickname", "Please enter your nickname", parent=temp_root)
        temp_root.destroy()  
        return nickname
    
    def new_nickname(self):
        temp_root = tk.Tk()
        temp_root.withdraw()  
        nickname = simpledialog.askstring("Nickname", "Please enter another nickname; Old one taken", parent=temp_root)
        temp_root.destroy()  
        return nickname

    def gui(self):
        self.chatbox = tk.Tk()
        self.chatbox.geometry("800x800")
        self.chatbox.title(f"Welcome to the chatroom: {self._nickname}")
        
        self.chatlabel = tk.Label(self.chatbox, text="All chat", font=("Arial", 12))
        self.chatlabel.pack(padx=10, pady=10)
        
        self.chat_area = scrolledtext.ScrolledText(self.chatbox)
        self.chat_area.pack(padx=10, pady=10)
        self.chat_area.config(state="disabled")
        
        self.msglabel = tk.Label(self.chatbox, text="Your messages here:", font=("Arial", 12))
        self.msglabel.pack(padx=10, pady=10)
        
        self.msg_area = tk.Text(self.chatbox, height=10)
        self.msg_area.pack(padx=10, pady=10)
        
        self.button = tk.Button(self.chatbox, text="Send Msg", font=("Arial", 10), command=self.write_msg)
        self.button.pack(padx=10, pady=10)
        
        self.gui_done = True
        self.chatbox.protocol("WM_DELETE_WINDOW", self.stop)
        self.chatbox.mainloop()
    
    def receive_msg(self):
        while self.running and not self.stop_event.is_set():
            try:
                msg = self._client.recv(1024).decode("utf-8")
                if msg == "NICKNAME":
                    self._client.send(self._nickname.encode("utf-8"))
                elif msg == "NICKNAME in use, please change":
                    # Update the nickname
                    self._nickname = self.new_nickname()
                    self._client.send(self._nickname.encode("utf-8"))
                    
                    # Recreate GUI in the main thread
                    self.chatbox.after(0, self.restart_gui)

                else:
                    if self.gui_done:
                        self.chatbox.after(0, self.update_chat_area, msg)
            except Exception as e:
                print(f"Error occurred while receiving msg: {e}")
                self.stop()
                break
    
    def update_chat_area(self, msg):
        self.chat_area.config(state="normal")
        self.chat_area.insert("end", msg + "\n")
        self.chat_area.yview("end")
        self.chat_area.config(state="disabled")
    
    def restart_gui(self):
        if self.chatbox:
            self.chatbox.quit()  # Exit the mainloop
            self.chatbox.destroy()
        self.gui()
    
    def write_msg(self):
        msg = self.msg_area.get("1.0", "end").strip()
        self.msg_area.delete("1.0", "end")
        try:
            self._client.send(msg.encode("utf-8"))
        except Exception as e:
            print(f"Error occurred while sending msg: {e}")
    
    def stop(self):
        self.running = False
        self.stop_event.set()
        if self.chatbox:
            self.chatbox.quit()  # Ensure the mainloop is exited
            self.chatbox.destroy()
        self._client.close()
        exit(0)

if __name__ == "__main__":
    NewClient = Client(SERVER_HOST, SERVER_PORT)
