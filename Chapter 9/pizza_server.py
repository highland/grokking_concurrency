#!/usr/bin/env python3

"""Simple one connection TCP/IP socket server"""
from socket import socket, create_server

# the maximum amount of data to be received at once
BUFFER_SIZE = 1024
ADDRESS = ("127.0.0.1", 12345)   # address and port of the host machine


class Server:
    def __init__(self) -> None:
        try:
            print(f"Starting up at: {ADDRESS}")
            self.server_socket: socket = create_server(ADDRESS)
            print("Listen for incoming connections")
            # on server side let's start listening mode for this socket
            self.server_socket.listen()
            print("Waiting for a connection")
        except OSError:
            self.server_socket.close()
            print("\nServer stopped.")

    def accept(self) -> socket:
        # accepting the incoming connection, blocking
        # conn = is a new socket object usable to send and receive data on the connection
        # client_address = is the address bound to the socket on the other end of connection
        conn, client_address = self.server_socket.accept()
        print(f"Connected to {client_address}")
        return conn

    def serve(self, conn: socket) -> None:
        try:
            while (data := conn.recv(BUFFER_SIZE)) != b'\n':
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

    def start(self) -> None:
        try:
            while True:
                conn = self.accept()
                self.serve(conn)
        finally:
            self.server_socket.close()
            print("\nServer stopped.")


if __name__ == "__main__":
    server = Server()
    server.start()
