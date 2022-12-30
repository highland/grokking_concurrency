#!/usr/bin/env python3

"""Non-blocking single threaded echo server implementation using asyncio
library"""

import asyncio
from socket import create_server
from asynchronous_pizza_joint import Kitchen
from socket import socket
# the maximum amount of data to be received at once
BUFFER_SIZE = 1024
ADDRESS = ("127.0.0.1", 12345)   # address and port of the host machine


class Server:
    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop
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

    async def start(self) -> None:
        try:
            while True:
                conn, addr = await self.loop.sock_accept(self.server_socket)
                self.loop.create_task(self.serve(conn))
        except Exception:
            self.server_socket.close()
            print("\nServer stopped.")

    async def serve(self, conn: socket) -> None:
        try:
            data = await self.loop.sock_recv(conn, BUFFER_SIZE)
            while data:
                order = int(data.decode())
                response = f"Thank you for ordering {order} pizzas\n"
                print(f"Sending message to {conn.getpeername()}")
                await self.loop.sock_sendall(conn, f"{response}\n".encode())
                await self.loop.run_in_executor(None, Kitchen.cook_pizza, order)
                await self.loop.sock_sendall(conn, f"{order} pizzas are ready\n".encode())
                data = await self.loop.sock_recv(conn, BUFFER_SIZE)
        except Exception:
            print(f"Connection with {conn.getpeername()} has been closed")
            conn.close()
            self.server_socket.close()
            print("\nServer stopped.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    server = Server(loop)
    loop.create_task(server.start())
    loop.run_forever()
    
    
