#!/usr/bin/env python3

#
"""Task parallelism using Pipeline processing pattern"""
import time
from queue import Queue
from threading import Thread


class Washer(Thread):
    """ A thread representing a Washing Machine. """

    def __init__(self, in_queue: Queue, out_queue: Queue):
        super().__init__()
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self) -> None:
        while True:
            # get the wash  load from the previous stage.
            wash_load = self.in_queue.get()
            print(f"Washing {wash_load}")
            time.sleep(1)
            # send the wash load to the next stage
            self.out_queue.put(f'{wash_load}')
            self.in_queue.task_done()


class Dryer(Thread):
    """ A thread representing a Dryer. """

    def __init__(self, in_queue: Queue, out_queue: Queue):
        super().__init__()
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self) -> None:
        while True:
            # get the wash load from the previous stage.
            wash_load = self.in_queue.get()
            # dry the wash_load
            print(f"\tDrying {wash_load}")
            time.sleep(2)
            # send the wash load to next stage
            self.out_queue.put(f'{wash_load}')
            self.in_queue.task_done()


class Folder(Thread):
    """ A thread representing the folding action. """

    def __init__(self, in_queue: Queue):
        super().__init__()
        self.in_queue = in_queue

    def run(self) -> None:
        while True:
            # get the wash load from the previous stage.
            wash_load = self.in_queue.get()
            # fold the wash_load
            print(f"\t\tFolding {wash_load}")
            time.sleep(1)
            print(f"\t\t\t{wash_load} done")
            self.in_queue.task_done()


class Pipeline:
    """ Represents a washer, dryer and folder linked by queues. """

    def assemble_laundry_for_washing(self):
        wash_load_count = 8
        wash_loads_in = Queue(wash_load_count)
        for wash_load_num in range(wash_load_count):
            wash_loads_in.put(f'wash_load no {wash_load_num}')
        return wash_loads_in

    def run_parallel(self) -> None:
        # set up the queues in the pipeline
        to_be_washed = self.assemble_laundry_for_washing()
        to_be_dried = Queue()
        to_be_folded = Queue()

        # start the threads linked by the queues
        Washer(to_be_washed, to_be_dried).start()
        Dryer(to_be_dried, to_be_folded).start()
        Folder(to_be_folded).start()

        # wait for washing to finish
        to_be_washed.join()
        to_be_dried.join()
        to_be_folded.join()
        print('All done!')


if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run_parallel()
