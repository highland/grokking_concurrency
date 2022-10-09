import asyncio
from collections import deque
from collections.abc import Coroutine
from typing import Deque, Any

AsyncTask = Coroutine[Any, Any, Any]


class EventLoop:
    """ Holds *awaitable* tasks in an queue.

        When the loop is run, tasks are taken from the queue and executed
        Tasks may be added to the queue at any time
        The loop continues until the queue is empty
    """

    def __init__(self) -> None:
        self.tasks: Deque[AsyncTask] = deque()

    def add_coroutine(self, task: AsyncTask) -> None:
        """ Add a task to the queue. """
        self.tasks.append(task)

    def _run_coroutine(self, task: AsyncTask) -> None:
        try:
            task.send(None)
            self.add_coroutine(task)
        except StopIteration:
            pass

    def run(self) -> None:
        """ Run the loop until no mare tasks exist in the queue. """
        while self.tasks:
            print("Event loop cycle.")
            self._run_coroutine(task=self.tasks.popleft())


async def fibonacci(n: int) -> None:   # note *async* keyword
    """ Generating fibonacci sequence as a non-recursive awaitable task """
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
        print(f"Fibonacci({i}): {a}")
        # returns control to the event loop
        await asyncio.sleep(0)  # note *await* keyword (one of 35 in python)


if __name__ == "__main__":
    el = EventLoop()
    el.add_coroutine(fibonacci(5))
    el.run()
