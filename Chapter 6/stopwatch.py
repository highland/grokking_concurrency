import time

Seconds = float


class Stopwatch:
    """Stopwatch to measure elapsed time"""

    def start(self) -> None:
        self.start_time = time.perf_counter()

    @property
    def elapsed_time(self) -> Seconds:
        try:
            return time.perf_counter() - self.start_time
        except AttributeError:
            self.start_time = time.perf_counter()
            return 0

    def __enter__(self):
        print('Stopwatch started')
        self.start()

    def __exit__(self, type, value, traceback):
        print(f'Stopwatch stopped at {self.elapsed_time} secs')


if __name__ == '__main__':
    with Stopwatch():
        print('Doing timed operation')
        time.sleep(2)
