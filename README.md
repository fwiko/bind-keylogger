# Bind Keylogger

A simple keylogger application utilising socket connections within python to send keylog data retreived from clients to a centralised server. Code from this project has been used in a university project of mine in which i implemented a remote-access tool with additional features.

## **Client**

Makes a connection to the server and sends keylogger data over the socket connection when a key is pressed.

**To run the client without building an executeable.**

#### 1. Install the required packages

```console
pip install -r requirements.txt
```

#### 2. Start the client

```console
python client.py
```

**To build a Windows executeable file.**

#### 1. Use pyinstaller to build the client.

```console
pyinstaller.exe --onefile client.py
```

## **Server**

The server provides the interface the "attacker" will use to receive keylogging data. Clients will make a connection to this server on the IP and Port specified when the listener is started.

### **_Running the server within a Docker container_**

#### 1. Build the Docker image

```console
docker build -t keylogger-server .
```

#### 2. Creating and running the Docker container

```console
docker run -d -v "$PWD":/usr/src/app -p <hostPort>:<containerPort> --name <name> keylogger-server:latest
```

