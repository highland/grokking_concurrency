#!/usr/bin/env python3

"""Multithreaded echo server implementation"""

import socket
from threading import Thread

# the maximum amount of data to be received at once
BUFFER_SIZE = 1024
ADDRESS = ("127.0.0.1", 12345)   # address and port of the host machine


class Handler(Thread):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn

    def run(self) -> None:
        print(f"Connected to {self.conn.getpeername()}")
        try:
            while (data := self.conn.recv(BUFFER_SIZE)) != b'\n':
                try:
                    order = int(data.decode())
                    response = f"Thank you for ordering {order} pizzas\n"
                except ValueError:
                    response = f"Unrecognisable order, '{data}' - please try again\n"
                print(f"Sending message to {self.conn.getpeername()}")
                # send a response
                self.conn.send(response.encode())
        finally:
            # server expects the client to close its side of the connection when it’s done.
            # In a real application, we should use timeout for clients if they don’t send
            # a request after a certain amount of time.
            print(f"Connection with {self.conn.getpeername()} has been closed")
            self.conn.close()


class Server:
    def __init__(self):
        try:
            print(f"Starting up at: {ADDRESS}")
            self.server_socket = socket.create_server(ADDRESS)
            print("Listen for incoming connections")
            # on server side let's start listening mode for this socket
            self.server_socket.listen()
            print("Waiting for a connection")
        except OSError:
            self.server_socket.close()
            print("\nServer stopped.")

    def accept(self):
        # accepting the incoming connection, blocking
        # conn = is a new socket object usable to send and receive data on the connection
        # addr = is the address bound to the socket on the other end of connection
        conn, address = self.server_socket.accept()
        return conn

    def start(self):
        try:
            while True:
                conn = self.accept(1)
                thread = Handler(conn)
                thread.start()
        except KeyboardInterrupt:
            print('Server Closing') 
        finally:
            self.server_socket.close()
            print("\nServer stopped.")


if __name__ == "__main__":
    server = Server()
    server.start()
