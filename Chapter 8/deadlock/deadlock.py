#!/usr/bin/env python3

"""Three philosophers thinking and eating dumplings - deadlock happens"""

import time
from threading import Thread

from lock_with_name import LockWithName

THREAD_DELAY = 0.1
dumplings = 20


class Philosopher(Thread):
    def __init__(self, name: str, left_chopstick: LockWithName, right_chopstick: LockWithName):
        super().__init__()
        self.name = name
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick

    def run(self) -> None:
        # using globally shared variable
        global dumplings

        while dumplings > 0:
            with self.left_chopstick:
                print(
                    f"{self.left_chopstick.name} grabbed by {self.name} now needs {self.right_chopstick.name}")

                with self.right_chopstick:
                    print(f"{self.right_chopstick.name} grabbed by {self.name}")

                    dumplings -= 1
                    print(
                        f"{self.name} eats a dumpling. Dumplings left: {dumplings}")

                print(f"{self.right_chopstick.name} released by {self.name}")
            print(f"{self.left_chopstick.name} released by {self.name}")
            time.sleep(THREAD_DELAY)


if __name__ == "__main__":
    chopstick_a = LockWithName("chopstick_a")
    chopstick_b = LockWithName("chopstick_b")

    philosopher_1 = Philosopher("Philosopher #1", chopstick_a, chopstick_b)
    philosopher_2 = Philosopher("Philosopher #2", chopstick_b, chopstick_a)

    philosopher_1.start()
    philosopher_2.start()
