#!/usr/bin/env python3

"""Non-blocking single threaded echo server implementation"""

from socket import socket, create_server
from typing import Set

# the maximum amount of data to be received at once
BUFFER_SIZE = 1024
ADDRESS = ("127.0.0.1", 12345)   # address and port of the host machine


class Server:
    clients: Set[socket] = set()

    def __init__(self) -> None:
        # AF_UNIX and SOCK_STREAM are constants represent the protocol and socket type respectively
        # here we create a TCP/IP socket
        try:
            print(f"Starting up at: {ADDRESS}")
            self.server_socket: socket = create_server(ADDRESS)
            # set socket to non-blocking mode
            self.server_socket.setblocking(False)
            print("Listen for incoming connections")
            # on server side let's start listening mode for this socket
            self.server_socket.listen()
            print("Waiting for a connection")
        except OSError:
            self.server_socket.close()
            print("\nServer stopped.")

    def accept(self) -> None:
        try:
            # accepting the incoming connection, non-blocking
            # conn = is a new socket object usable to send and receive data on the connection
            # client_address = is the address bound to the socket on the other end of connection
            # Saves the socket og the incoming connection to the set of clients
            conn, client_address = self.server_socket.accept()
            # making this connection non-blocking
            conn.setblocking(False)
            self.clients.add(conn)
            print(f"Connected to {client_address}")
        except BlockingIOError:
            # [Errno 35] Resource temporarily unavailable
            # indicates that "accept" returned without results
            pass

    def serve(self, conn: socket) -> None:
        try:
            data = conn.recv(BUFFER_SIZE)
            if not data:   # client not sending
                self.clients.remove(conn)
                print(f"Connection with {conn.getpeername()} has been closed")
                conn.close()
            else:
                try:
                    order = int(data.decode())
                    response = f"Thank you for ordering {order} pizzas\n"
                except ValueError:
                    response = "Wrong number of orders, please try again\n"
                print(f"Sending message to {conn.getpeername()}")
                # send a response
                conn.send(response.encode())
                # Note: recommended way is to use .sendall(),
                # but we will stick with send to keep reader's mental model
        except BlockingIOError:
            # recv/send returns without data
            pass

    def start(self) -> None:
        try:
            while True:
                self.accept()
                for conn in self.clients.copy():  # poll the set of clients
                    self.serve(conn)
        finally:
            self.server_socket.close()
            print("\nServer stopped.")


if __name__ == "__main__":
    server = Server()
    server.start()
