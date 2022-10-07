#!/usr/bin/env python3

#
"""Task parallelism using Pipeline processing pattern"""
import time
from queue import Queue
from threading import Thread

Washload = str


class Washer(Thread):
    """ A thread representing a Washing Machine. """

    def __init__(self, in_queue: Queue[Washload], out_queue: Queue[Washload]):
        super().__init__()
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self) -> None:
        while True:
            # get the wash  load from the previous stage.
            Washload = self.in_queue.get()
            print(f"Washing {Washload}")
            time.sleep(1)
            # send the wash load to the next stage
            self.out_queue.put(f'{Washload}')
            self.in_queue.task_done()


class Dryer(Thread):
    """ A thread representing a Dryer. """

    def __init__(self, in_queue: Queue[Washload], out_queue: Queue[Washload]):
        super().__init__()
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self) -> None:
        while True:
            # get the wash load from the previous stage.
            Washload = self.in_queue.get()
            # dry the Washload
            print(f"\tDrying {Washload}")
            time.sleep(2)
            # send the wash load to next stage
            self.out_queue.put(f'{Washload}')
            self.in_queue.task_done()


class Folder(Thread):
    """ A thread representing the folding action. """

    def __init__(self, in_queue: Queue[Washload]):
        super().__init__()
        self.in_queue = in_queue

    def run(self) -> None:
        while True:
            # get the wash load from the previous stage.
            Washload = self.in_queue.get()
            # fold the Washload
            print(f"\t\tFolding {Washload}")
            time.sleep(1)
            print(f"\t\t\t{Washload} done")
            self.in_queue.task_done()


class Pipeline:
    """ Represents a washer, dryer and folder linked by queues. """

    def assemble_laundry_for_washing(self) -> Queue[Washload]:
        Washload_count = 8
        Washloads_in: Queue[Washload] = Queue(Washload_count)
        for Washload_num in range(Washload_count):
            Washloads_in.put(f'Washload no {Washload_num}')
        return Washloads_in

    def run_parallel(self) -> None:
        # set up the queues in the pipeline
        to_be_washed = self.assemble_laundry_for_washing()
        to_be_dried: Queue[Washload] = Queue()
        to_be_folded: Queue[Washload] = Queue()

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
