"""Don"t mind it - just upgrading a mutex
     with additional attribute
     to make examples more explicit."""

from threading import Lock


class LockWithName:
    """ A standard python lock but with name attribute added. """

    def __init__(self, name: str):
        self.name = name
        self._lock = Lock()

    def acquire(self):
        self._lock.acquire()

    def release(self):
        self._lock.release()

    def __enter__(self):
        """ Allows this to be used with context management. """
        self.acquire()

    def __exit__(self, exc_type, exc_value, exc_tb):
        """ Allows this to be used with context management. """
        self.release()
