#!/usr/bin/env python3

""" Using pipes for IPC """

from threading import Thread, current_thread
from multiprocessing import Pipe
from multiprocessing.connection import Connection


class Writer(Thread):
    """Writer thread will write messages into the pipe"""
    def __init__(self, conn: Connection):
        super().__init__()
        self.conn = conn
        self.name = 'Writer'

    def run(self) -> None:
        print(f"{current_thread().name}: Sending rubber duck...")
        self.conn.send("Rubber duck")

class Reader(Thread):
    """Writer thread will write messages into the pipe"""
    def __init__(self, conn: Connection):
        super().__init__()
        self.conn = conn
        self.name = 'Reader'

    def run(self) -> None:
        print(f"{current_thread().name}: Reading...")
        msg = self.conn.recv()
        print(f"{current_thread().name}: Received: {msg}")


def main() -> None:
    # Connections for reading and writing
    reader_conn, writer_conn = Pipe()
    reader = Reader(reader_conn)
    writer = Writer(writer_conn)

    threads = [
        writer,
        reader
    ]
    # start threads
    for thread in threads:
        thread.start()

    # block the main thread until the child threads has finished
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
