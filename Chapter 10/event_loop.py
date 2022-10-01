#!/usr/bin/env python3

"""Simple single threaded event loop implementation"""

import time
from collections import deque
from threading import Thread


class Event:
    def __init__(self, name: str, callback: callable, next_event = None):
        self.name = name
        self.callback = callback
        self.next_event = next_event
        
    def execute(self):
        self.callback(self)
        
    
class EventLoop(Thread):
    def __init__(self):
        super().__init__()
        # internal task queue
        self.events: deque[Event] = deque()

    def register_event(self, event: Event):
        self.events.append(event)

    def run(self):
        self._run_forever()

    def _run_forever(self):
        while True:
            # execute the ready tasks
            while self.events:
                event = self.events.popleft()
                event.execute()


def knock(event: Event):
    print(event.name)
    time.sleep(1)
    # adding a next task into the event loop task queue
    event_loop.events.append(event.next_event)


def who(event: Event):
    print(event.name)
    time.sleep(2)


if __name__ == "__main__":
    event_loop = EventLoop()
    replying = Event("Who's there?", who)
    knocking = Event("Knock-knock", knock, replying)
    event_loop.register_event(knocking)
    event_loop.register_event(replying)
    # adding several events
    for _ in range(2):
        event_loop.events.append(knocking)
    event_loop.start()
