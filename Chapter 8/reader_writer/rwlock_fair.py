"""Reader-writer lock: fair lock"""

from threading import Lock


class RWLockFair:
    def __init__(self):
        self.readers = 0
        # To achieve fairness and prevent starvation, we can use another mutex named that
        # will materialize the order of arrived events (read or write). This semaphore will be taken
        # by any entity that requests access to the resource, and released as soon as this entity
        # gains access to the resource
        self.order_lock = Lock()
        self.read_lock = Lock()
        self.write_lock = Lock()

    def acquire_read(self):
        with self.order_lock:
            with self.read_lock:
                self.readers += 1
                if self.readers == 1:
                    self.write_lock.acquire()

    def release_read(self):
        assert self.readers >= 1
        with self.read_lock:
            self.readers -= 1
            if self.readers == 0:
                self.write_lock.release()

    def acquire_write(self):
        with self.order_lock:
            self.write_lock.acquire()

    def release_write(self):
        self.write_lock.release()
