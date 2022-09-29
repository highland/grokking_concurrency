# -*- coding: utf-8 -*-
"""
Simple Pizza Client
"""

import socket

BUFFER_SIZE = 1024
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 12345  # The port used by the server

with socket.socket() as s:
    s.connect((HOST, PORT))
    while order := input('How many pizzas do you want? '):
        s.send(order.encode())
        response = s.recv(BUFFER_SIZE)
        print(f'Server replied {response.decode()}')

