"""Event loop implementation with futures and coroutines"""

from selectors import DefaultSelector
from collections import deque
from future import Future
from typing import Deque, Coroutine, Any, NoReturn, Callable
from socket import socket

Data = bytes
Action = Callable[[socket, Any], None]

BUFFER_SIZE = 1024
Mask = int # selectors constants EVENT_READ & EVENT_WRITE


class EventLoop:
    def __init__(self) -> None:
        self.event_notifier = DefaultSelector()
        self.tasks: Deque[Coroutine[Any, Any, Any]] = deque()

    def create_future(self) -> Future:
        return Future(loop=self)

    def create_future_for_events(self, sock: socket, events: Mask) -> Future:
        future = self.create_future()

        def handler(sock: socket, result: Any) -> None:
            self.unregister_event(sock)
            future.set_result(result)

        self.register_event(sock, events, handler)
        return future

    def register_event(self, source: socket, event: int, action: Action) -> None:
        try:
            self.event_notifier.register(source, event, action)
        except KeyError:  # already exists so modify
            self.event_notifier.modify(source, event, action)

    def unregister_event(self, source: socket) -> None:
        self.event_notifier.unregister(source)

    def add_coroutine(self, co: Coroutine[Any, Any, Any]) -> None:
        self.tasks.append(co)

    def run_coroutine(self, co: Coroutine[Any, Any, Any]) -> None:
        try:
            future = co.send(None)
            future.set_coroutine(co)
        except StopIteration:
            pass

    def run_forever(self) -> NoReturn:
        while True:
            while not self.tasks:
                try:
                    events = self.event_notifier.select()
                    for (source, _, _, action), _ in events:
                        action(source, events)
                except OSError:
                    pass

            while self.tasks:
                self.run_coroutine(co=self.tasks.popleft())
