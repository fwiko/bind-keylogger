# bind-keylogger (WIP)
 
The server accepts connections from keylogger clients who then send keylogger data over the connection. The server then allows interaction with keylogger data and clients.

## Client
Makes a connection to the server and sends keylogger data over the socket connection when keys are pressed.

message displayed on server when a client makes a connection
```
Server:> 
[NEW] > Connection from 127.0.0.1:1069
```

#

## Server
Listens for connections from clients and receives keylogger data which can then be interacted with (viewed and/or saved) from the built in command-line interface.

help command - displays the list of available commands
```
Server:> help
          sessions | List all active sessions.
 logs <session_id> | Display the logs of specified session.
 save <session_id> | Save the logs of specified session to a file    
              help | Display this list.
              exit | Shutdown listener server and close all sessions.
```
sessions command - session_id | client_address:client_port | log_length
```
Server:> sessions
 1 | 127.0.0.1:8464 | 10
 2 | 127.0.0.1:9283 | 152
```
logs command - displays the logs of specified session
```
Server:> logs 1

Keyboard logs from - Session 1 (127.0.0.1:8464)
--------------------------------

hello awpiudhbaw9dghaw-09d87gbaw-uda
```
save command - saves the logs of specified session to a file
```
Server:> save 1
[SUCCESS] > Logs written to file log-127.0.0.1_08-24-2021_15-31-11.txt
```
exit command - closes the listener server
```
Server:> exit
[EXIT] > Server Stopped
```
#

Project still a WIP and can most likely be optimised further.

(educational innit)