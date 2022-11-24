"""Simple one connection TCP/IP socket server"""
import socket
from typing import NoReturn
from async_socket import AsyncSocket
from event_loop import EventLoop

# the maximum amount of data to be received at once
BUFFER_SIZE = 1024
HOST = "127.0.0.1"  # address of the host machine
PORT = 12345  # port to listen on (non-privileged ports are > 1023)


class Server:
    def __init__(self) -> None:
        self._loop = EventLoop()
        self._server_socket = AsyncSocket(
            sock=socket.socket(), loop=self._loop)
        # allows multiple sockets to be bound to an identical socket address
        self._server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            print(f"Starting up on: {HOST}:{PORT}")
            # bind a socket to a specific network interface and port number
            self._server_socket.bind((HOST, PORT))
            print("Listen for incoming connections")
            # on server side let"s start listening mode for this socket
            self._server_socket.listen()
            print("Waiting for a connection")
            self._server_socket.setblocking(False)
        except OSError:
            self._server_socket.close()
            print("\nServer stopped.")
        self._loop.add_coroutine(self.serve_forever())
        self._loop.run_forever()
        print("Event Loop started")

    async def serve(self, conn: AsyncSocket) -> None:
        try:
            while (data := await conn.recv(BUFFER_SIZE)):
                try:
                    order = int(data.decode())
                    response = f"Thank you for ordering {order} pizzas\n"
                except ValueError:
                    response = f"Unrecognisable order, '{data!r}' - please try again\n"
                print(f"Sending message to {conn.getpeername()}")
                # send a response
                await conn.send(response.encode())
        finally:
            # server expects the client to close its side of the connection when it’s done.
            # In a real application, we should use timeout for clients if they don’t send
            # a request after a certain amount of time.
            print(f"Connection with {conn.getpeername()} has been closed")
            conn.close()

    async def serve_forever(self) -> NoReturn:
        try:
            while True:
                conn, client_address = await self._server_socket.accept()
                print(f"Connected to {client_address}")
                self._loop.add_coroutine(self.serve(conn))
        finally:
            self._server_socket.close()
            print("\nServer stopped.")


if __name__ == "__main__":
    server = Server()
