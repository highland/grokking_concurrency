#!/usr/bin/env python3

"""Simple single threaded event loop implementation"""

from collections import deque
from threading import Thread, Lock
from time import sleep


class Event:
    def __init__(self, name: str, action: callable, next_event=None):
        self.name = name
        self._action = action
        self.next_event = next_event

    def execute_action(self):
        self._action(self)


class EventLoop(Thread):
    """ Maintains a deque of Events and executes them. """
    

    def __init__(self):
        super().__init__()
        # internal event queue
        self._events: deque[Event] = deque()
        # manage concurrent access to event queue
        self._mutex = Lock()


    def register_event(self, event: Event):
        with self._mutex:
            self._events.append(event)

    def run(self):
        print(f'Queue running with {len(self._events)} events')
        self._run_forever()

    def _run_forever(self):
        while True:   # busy-waiting
            # execute the action of the next event
            with self._mutex:
                try:
                    event = self._events.popleft()
                except IndexError:
                    continue
            event.execute_action()


def knock(event: Event):
    """ A callback which does an action and adds another Event to the deque. """
    print(event.name)
    sleep(1)
    # adding a next event into the event loop event queue
    event_loop.register_event(event.next_event)


def who(event: Event):
    """ A callback which simply does an action. """
    print(event.name)
    sleep(2)


if __name__ == "__main__":
    event_loop = EventLoop()
    replying = Event("Who's there?", who)
    knocking = Event("Knock-knock", knock, replying)
    event_loop.register_event(knocking)
    event_loop.register_event(replying)
    # adding several _events
    for _ in range(2):
        event_loop.register_event(knocking)
    event_loop.start()
