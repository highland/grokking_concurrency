import time


class Stopwatch:
    """Stopwatch to measure elapsed time"""
    
    def start(self) -> None:
        self.start_time = time.perf_counter()

    @property
    def elapsed_time(self) -> time:
        try:
            return time.perf_counter() - self.start_time
        except AttributeError:
            self.start_time = time.perf_counter()
            return 0
