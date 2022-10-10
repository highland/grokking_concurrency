from __future__ import annotations  # allows forward references in type hints

from random import randint
from collections.abc import Coroutine
from typing import Any, Generator


Result = Any
Burger = Result  # our Burger is a string!


class Future:
    def __init__(self) -> None:
        self.done = False

    def set_coroutine(self, coroutine: Coroutine[Any, Any, Result]) -> None:
        self.coroutine = coroutine

    def set_result(self, result: Result) -> None:
        self.done = True
        self.result = result

    def __await__(self) -> Generator[Future, None, Result]:
        if not self.done:
            yield self
        return self.result


async def cook() -> Burger:
    f = Future()

    def on_callback() -> None:   # Locally defined functiom
        burger: str = f"Burger #{randint(1, 10)}"
        print(f"{burger} is cooked!")
        f.set_result(burger)

    on_callback()
    c = await f
    return c


async def cashier(burger: Burger) -> Burger:
    f = Future()

    def on_callback() -> None:
        print("Burger is ready for pick up!")
        f.set_result(burger)

    on_callback()
    c = await f
    return c


async def order_burger() -> Burger:
    burger = await cook()
    burger = await cashier(burger)
    return burger


def run_coroutine(coroutine: Coroutine[Any, Any, Result]) -> None:
    try:
        future = coroutine.send(None)
        future.set_coroutine(coroutine)
    except StopIteration as e:
        print(f"{e.value}? That's me! Mmmmmm!")


if __name__ == "__main__":
    run_coroutine(order_burger())
