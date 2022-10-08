#!/usr/bin/env python3
"""Three philosophers, thinking and eating sushi - but some has been starving"""
import time
from threading import Thread

from deadlock.lock_with_name import LockWithName         # type: ignore

dumplings = 1000
THREAD_DELAY = 1e-16


class Philosopher(Thread):
    def __init__(self, name: str, left_chopstick: LockWithName, right_chopstick: LockWithName):
        super().__init__()
        self.name = name
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick

    def run(self) -> None:
        # using globally shared variable
        global dumplings

        dumplings_eaten = 0
        while dumplings > 0:
            with self.left_chopstick:
                with self.right_chopstick:
                    if dumplings > 0:
                        dumplings -= 1
                        dumplings_eaten += 1
                        time.sleep(THREAD_DELAY)
        print(f"{self.name} ate {dumplings_eaten} pieces")


if __name__ == "__main__":
    chopstick_a = LockWithName("chopstick_a")
    chopstick_b = LockWithName("chopstick_b")

    threads = []
    for i in range(10):
        threads.append(Philosopher(f"Philosopher #{i}", chopstick_a, chopstick_b))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
