#!/usr/bin/env python3

"""Multithreaded echo server implementation"""

from socket import socket, create_server
from concurrent.futures import ThreadPoolExecutor

# the maximum amount of data to be received at once
BUFFER_SIZE = 1024
ADDRESS = ("127.0.0.1", 12345)   # address and port of the host machine


def handle_request(conn: socket) -> None:
    print(f"Connected to {conn.getpeername()}")
    try:
        while (data := conn.recv(BUFFER_SIZE)):
            try:
                order = int(data.decode())
                response = f"Thank you for ordering {order} pizzas\n"
            except ValueError:
                response = f"Unrecognisable order, '{data!r}' - please try again\n"
            print(f"Sending message to {conn.getpeername()}")
            # send a response
            conn.send(response.encode())
    finally:
        # server expects the client to close its side of the connection when it’s done.
        # In a real application, we should use timeout for clients if they don’t send
        # a request after a certain amount of time.
        print(f"Connection with {conn.getpeername()} has been closed")
        conn.close()


class Server:
    def __init__(self) -> None:
        self.pool = ThreadPoolExecutor()
        try:
            print(f"Starting up at: {ADDRESS}")
            self.server_socket = create_server(ADDRESS)
            print("Listening for incoming connections")
            # on server side let's start listening mode for this socket
            self.server_socket.settimeout(60)  # Don't wait forever
            self.server_socket.listen()
            print("Waiting for a connection")
        except OSError:
            self.server_socket.close()
            print("\nServer stopped.")

    def start(self) -> None:
        try:
            while True:
                conn, address = self.server_socket.accept()
                print(f"Client connection request from {address}")
                self.pool.submit(handle_request, conn)
        finally:
            self.server_socket.close()
            print("\nServer stopped.")


if __name__ == "__main__":
    server = Server()
    server.start()
