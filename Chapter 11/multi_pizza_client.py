# -*- coding: utf-8 -*-
"""
Simulate multiple concurrent pizza clients
Created on Thu Nov 24 16:11:39 2022

@author: Mark
"""

from socket import create_connection
from time import sleep
from threading import Thread
from typing import List

BUFFER_SIZE = 1024
ADDRESS = ("127.0.0.1", 12345)   # address and port of the host machine

CLIENT_ORDERS: List[List[str]] = [["22"], ["33","2"], ["2","1","3"],[]]


def make_client_requests(client: int, orders: List[str]) -> None:
    with create_connection(ADDRESS) as conn:
        for order in orders:
            conn.send(order.encode())
            print(f'Client number {client} sent an order for {order} pizzas')
            response = conn.recv(BUFFER_SIZE)
            print(f'Client number {client} recieved reply "{response.decode().rstrip()}"')
            sleep(1)
        conn.send(b"")
        print(f'Client number {client} closing')

for client_number, client_order in enumerate(CLIENT_ORDERS):
    Thread(target = make_client_requests, args = (client_number, client_order)).start()
    