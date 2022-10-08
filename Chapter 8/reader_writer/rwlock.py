"""Reader-writer lock: readers have priority"""

from threading import Lock


class RWLock:
    def __init__(self) -> None:
        self.readers = 0
        self.read_lock = Lock()
        self.write_lock = Lock()

    def acquire_read(self) -> None:
        with self.read_lock:
            self.readers += 1
            if self.readers == 1:
                self.write_lock.acquire()

    def release_read(self) -> None:
        assert self.readers >= 1
        with self.read_lock:
            self.readers -= 1
            if self.readers == 0:
                self.write_lock.release()
 
    def acquire_write(self) -> None:
        self.write_lock.acquire()

    def release_write(self) -> None:
        self.write_lock.release()
