
# Server
The server provides the interface the "attacker" will use to receive keylogging data. Clients will make a connection to this server on the IP and Port specified when the listener is started.

**message displayed on server when a client makes a connection**
```
bind-logger:> 

[CONNECTION] > Connection from 127.0.0.1:1069

```

## Commands

**help command** - displays the list of available commands
```
bind-logger:> help

               sessions | List all active sessions.
      logs <session_id> | Display the logs of specified session.
      save <session_id> | Save the logs of specified session to a file.
 set <variable> <value> | Change the value of one of the available options.
                   help | Display this list.
                options | Display a list of variable options.
                  start | Run the keylogger connection listener
                   kill | Stop a specified session/client connection.      
                   exit | Shutdown listener server and close all sessions. 

```

**options command** - displays current state of variable options
```
bind-logger:> options

   LHOST | 127.0.0.1
   LPORT | 6666

```

**set command** - assigns specified value to specified variable
```
bind-logger:> set LPORT 9821

[SUCCESS] > Set LPORT to 9821

```

**start command** - start the keylogger client connection listener
```
bind-logger:> start

[LISTENER] > Listening on 127.0.0.1:6666

```

**sessions command** - list active sessions session_id | client_address:client_port | log_length
```
bind-logger:> sessions
 1 | 127.0.0.1:8464 | 10
 2 | 127.0.0.1:9283 | 152

```

**kill command** - terminate a specified client connection
```
bind-logger:> kill 1

[DISCONNECT] > Session 1 (127.0.0.1:1093) - Logs Saved

```

**logs command** - displays the logs of specified session
```
bind-logger:> logs 1

Keyboard logs from - Session 1 (127.0.0.1:8464)
--------------------------------

hello awpiudhbaw9dghaw-09d87gbaw-uda

```

**save command** - saves the logs of specified session to a file
```
bind-logger:> save 1
[SUCCESS] > Logs written to file log-127.0.0.1_08-24-2021_15-31-11.txt
```

**exit command** - closes all sessions and exits application
```
bind-logger:> exit

[EXIT] > Stopped.

```