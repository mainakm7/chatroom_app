# TCP Socket-Based Chatroom App

This is a simple chatroom application built using Python's `socket` module. The application consists of a server and two types of clients—a console-based client and a GUI-based client—allowing users to communicate with each other over a TCP socket connection.

## Features

- **Server-Side**: Handles multiple client connections and broadcasts messages to all connected clients.
- **Console Client**: A command-line interface for connecting to the server and sending/receiving messages.
- **GUI Client**: A graphical interface for a more user-friendly chat experience.

## Installation

To get started with the chatroom app, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/mainakm7/chatroom_app.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd chatroom_app/TCP_socket
    ```

3. **No additional dependencies are required for this application.**

## Usage

### Running the Server

1. Open a terminal and navigate to the project directory.
2. Run the server script:

    ```bash
    python server.py
    ```
   Make sure to properly update the HOST IP and PORT
   The server will start and listen for incoming connections on the specified port.

### Console Client

1. Enter the server's IP address and port in the client script.
2. Open a terminal.
3. Run the console client script:

    ```bash
    python client.py
    ```
4. Start chatting! Messages typed in the terminal will be sent to all connected clients.

### GUI Client

1. Enter the server's IP address and port in the client script.
2. Run the GUI client script:

    ```bash
    python client_gui.py
    ```
3. Use the GUI to send and receive messages in a user-friendly interface.

## Configuration

- **Server Port**: The default port used by the server is `12345`. You can change this in the `server.py` file.
- **Server IP Address**: By default, the server listens on `localhost`. You can update the IP address if you want to allow remote connections.

## Code Structure

- `server.py`: The main server script that handles incoming client connections and broadcasts messages.
- `client.py`: The console client script that connects to the server and allows users to send and receive messages via the command line.
- `client_gui.py`: The GUI client script that connects to the server and provides a graphical interface for chatting.



