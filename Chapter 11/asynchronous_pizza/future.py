"""The best known way to see the future is to wait"""

from typing import Coroutine, Generator, Awaitable, Any, NewType
import event_loop


class Future(Awaitable[Any]):
    def __init__(self, loop: event_loop.EventLoop) -> None:
        self.loop = loop
        self.done = False

    def set_coroutine(self, co: Coroutine[Any, Any, Any]) -> None:
        self.co = co

    def set_result(self, result: Any) -> None:
        self.done = True
        self.result = result

        if self.co:
            self.loop.add_coroutine(self.co)

    def __await__(self) -> Generator[Any, None, Any]:  # This 'Magic Method' is what makes Future a future
        if not self.done:
            yield self
        return self.result
