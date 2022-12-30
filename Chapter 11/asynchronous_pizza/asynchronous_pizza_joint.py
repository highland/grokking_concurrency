#!/usr/bin/env python3

"""Multithreaded echo server implementation"""

import time
from socket import socket, create_server
from concurrent.futures import ThreadPoolExecutor

# the maximum amount of data to be received at once
BUFFER_SIZE = 1024
ADDRESS = ("127.0.0.1", 12345)   # address and port of the host machine


class Kitchen:
    @staticmethod
    async def cook_pizza(n: int) -> None:
        print(f"Started cooking {n} pizzas")
        time.sleep(n)
        print(f"Fresh {n} pizzas are ready!")


class Server:
    def __init__(self) -> None:
        self.pool = ThreadPoolExecutor()
        try:
            print(f"Starting up at: {ADDRESS}")
            self.server_socket = create_server(ADDRESS)
            print("Listening for incoming connections")
            # on server side let's start listening mode for this socket
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
                self.pool.submit(self.serve, conn)
        finally:
            self.server_socket.close()
            print("\nServer stopped.")

    def serve(self, conn: socket) -> None:   # This runs in a separate thread managed by the pool
        try:
            data = conn.recv(BUFFER_SIZE)
            while data:
                try:
                    order = int(data.decode())
                    response = f"Thank you for ordering {order} pizzas\n"
                    print(f"Sending message to {conn.getpeername()}")
                    conn.send(response.encode())
                    Kitchen.cook_pizza(order)
                    print(f"Sending message to {conn.getpeername()}")
                    conn.send(
                        f"Your order for {order} pizzas is ready!\n".encode())
                except ValueError:
                    response = "Wrong number of orders, please try again\n"
                    print(f"Sending message to {conn.getpeername()}")
                    conn.send(response.encode())
                data = conn.recv(BUFFER_SIZE)
            print(f"Connection with {conn.getpeername()} has been closed")
            conn.close()
        except Exception:
            self.server_socket.close()
            print("\nServer stopped.")


if __name__ == "__main__":
    server = Server()
    server.start()
