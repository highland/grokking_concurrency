#!/usr/bin/env python3
"""Bank account without synchronization cause race condition """

from threading import Lock


class SyncedBankAccount:
    """Bank account with synchronization strategy, thread-safe"""

    balance: float

    def __init__(self, balance: float = 0):
        self.balance: float = balance
        self.mutex = Lock()

    def deposit(self, amount: float) -> None:
        # acquiring a lock on the shared resource
        with self.mutex:
            if amount > 0:
                self.balance += amount
            else:
                raise ValueError("You can't deposit negative amount of money")


    def withdraw(self, amount: float) -> None:
        with self.mutex:
            if 0 < amount <= self.balance:
                self.balance -= amount
            else:
                raise ValueError("Account does not contain sufficient funds")