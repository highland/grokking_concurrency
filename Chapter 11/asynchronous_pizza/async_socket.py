"""Asynchronous socket implementation - same functionality but with asynchronous flavour!"""
from __future__ import annotations  # allows forward references in type hints

import selectors


from typing import Tuple, Any
from socket import socket
from event_loop_with_pool import EventLoop

Address = int  # IPAddress


class AsyncSocket:
    def __init__(self, sock: socket, loop: EventLoop) -> None:
        sock.setblocking(False)
        self._sock = sock
        self._loop = loop

    async def accept(self) -> Tuple[AsyncSocket, Address]:
        while True:
            try:
                client_sock, client_addr = self._sock.accept()
                return AsyncSocket(client_sock, self._loop), client_addr
            except BlockingIOError:
                future = self._loop.create_future_for_events(
                    self._sock, selectors.EVENT_READ)
                await future

    async def recv(self, bufsize: int) -> bytes:
        while True:
            try:
                return self._sock.recv(bufsize)
            except BlockingIOError:
                future = self._loop.create_future_for_events(
                    self._sock, selectors.EVENT_READ)
                await future

    async def send(self, data: bytes) -> int:
        while True:
            try:
                return self._sock.send(data)
            except BlockingIOError:
                future = self._loop.create_future_for_events(
                    self._sock, selectors.EVENT_WRITE)
                await future

    def __getattr__(self, name: str) -> Any:
        return getattr(self._sock, name)
