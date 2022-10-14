# -*- coding: utf-8 -*-
"""
Asynchronous Pizza Server

Author: Mark Thomas
"""

from asyncio import StreamReader, StreamWriter, start_server, run


BUFFER_SIZE = 1024
SERVER_PORT = 12345
LOCAL_HOST = "127.0.0.1"


async def _on_client_connected(client_reader: StreamReader, client_writer: StreamWriter) -> None:
    """ Callback function invoked by the Server when accepting a client connection. """
    client_address = client_writer.get_extra_info('peername')
    print(f"Connected to {client_address!r}")
    try:
        while (data := await client_reader.read(BUFFER_SIZE)) != b'\n':
            try:
                order = int(data.decode())
                response = f"Thank you for ordering {order} pizzas\n"
            except ValueError:
                response = f"Unrecognisable order, '{data!r}' - please try again\n"
            client_writer.write(response.encode())
            await client_writer.drain()
    finally:
        print(f"Connection with {client_address} has been closed")
        client_writer.close()


async def main():
    """ Starts the Pizza Server and waits for connections. """
    print(f"Starting up at: {LOCAL_HOST}:{SERVER_PORT}")
    pizza_server = await start_server(
        _on_client_connected, host=LOCAL_HOST, port=SERVER_PORT)
    async with pizza_server:
        await pizza_server.serve_forever()

run(main())
