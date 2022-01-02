# Bind Keylogger
### A simple keylogger application utilising socket connections within python to send keylog data retreived from clients to a centralised server.

#### The server side has been stripped down with the CLI being removed, requiring less interaction.

## **Client**
Makes a connection to the server and sends keylogger data over the socket connection when a key is pressed. 

To run the client without building an executeable the `start.bat` script can be used. This will require a virtual environment to be created and all necessary dependencies installed.

*A virtual environment can also be used to run the client on systems that may not have python installed*

#### 1. Setup and activate virtual environment
```console
python -m venv env
./env/Scripts/activate
```
#### 2. Install the required packages within the virtual environment
```console
pip install -r requirements.txt
```

To build an executeable the `build.bat` script can be used. The required dependencies must be installed beforehand.

## **Server**
The server provides the interface the "attacker" will use to receive keylogging data. Clients will make a connection to this server on the IP and Port specified when the listener is started.


### ***Running the server within Docker***

#### 1. Build the Docker image
```console
docker build -t keylogger-server .
```

#### 2. Creating and running the Docker container
```console
docker run -d -v "$PWD":/usr/src/app --name <name> keylogger-server:latest
```



##  **THIS REPOSITORY EXISTS PURELY FOR DEMONSTRATION/EDUCATIONAL PURPOSES**
