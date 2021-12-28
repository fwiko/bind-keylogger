# Bind Keylogger
## 🖥️ Connection handler that accepts connections and data from a client and then handles whatever data is sent over the connection allowing the user to view/interact with said data.

#

## **Client**
Makes a connection to the server and sends keylogger data over the socket connection when a key is pressed. 

To run the client without building an executeable the `start.bat` script can be used. This will require a virtual environment to be created and all necessary dependencies installed.

```console
python -m venv env
./env/Scripts/activate
pip install -r requirements.txt
```

To build an executeable the `build.bat` script can be used. The required dependencies must be installed beforehand.

## **Server**
The server provides the interface the "attacker" will use to receive keylogging data. Clients will make a connection to this server on the IP and Port specified when the listener is started.


### ***Hosting the server using Docker***

Build the Docker image
```console
docker build -t keylogger-server .
```

Creating and running the Docker container
```console
docker run -d -v "$PWD":/usr/src/app --name <name> keylogger-server:latest
```



##  **THIS REPOSITORY EXISTS PURELY FOR DEMONSTRATION/EDUCATIONAL PURPOSES**
