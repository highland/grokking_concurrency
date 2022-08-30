#!/usr/bin/env python3

""" Using sockets for IPC """

import socket
import time
from threading import Thread, current_thread

BUFFER_SIZE = 1024
host = 'localhost'
port = 1812

class Sender(Thread):
    def run(self) -> None:
        self.name = 'Sender'
        client = socket.socket()
        client.connect((host, port))
        
        messages = ["Hello", " ", "world!"]
        for msg in messages:
            print(f"{current_thread().name}: Sent: '{msg}'")
            client.sendall(str.encode(msg))

        client.close()


class Receiver(Thread):
    def run(self) -> None:
        self.name = 'Receiver'
        server = socket.socket()
        # bind socket to the file
        server.bind((host, port))
        # let's start listening mode for this socket
        server.listen()

        print(f"{current_thread().name}: Listening for incoming messages...")
        # accept a connection
        conn, addr = server.accept()

        # receive data from socket
        while data := conn.recv(BUFFER_SIZE):
            message = data.decode()   # bytes to string
            print(f"{current_thread().name}: Received: '{message}'")

        server.close()


def main() -> None:
    # receiver will create a socket
    receiver = Receiver()
    receiver.start()
    # waiting till the socket has been created
    time.sleep(1)
    sender = Sender()
    sender.start()

    # block the main thread until the child threads has finished
    for thread in [receiver, sender]:
        thread.join()


if __name__ == "__main__":
    main()
