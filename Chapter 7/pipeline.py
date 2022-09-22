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
            # get the item from the previous stage.
            item = self.in_queue.get()
            print(f"Washing {item}")
            time.sleep(1)
            # send the message to the next stage
            self.out_queue.put(f'{item}')
            self.in_queue.task_done()


class Dryer(Thread):
    """ A thread representing a Dryer. """

    def __init__(self, in_queue: Queue, out_queue: Queue):
        super().__init__()
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self) -> None:
        while True:
            # get the item from the previous stage.
            item = self.in_queue.get()
            # dry the item
            print(f"\tDrying {item}")
            time.sleep(2)
            # send the item to next stage
            self.out_queue.put(f'{item}')
            self.in_queue.task_done()


class Folder(Thread):
    """ A thread representing the folding action. """

    def __init__(self, in_queue: Queue):
        super().__init__()
        self.in_queue = in_queue

    def run(self) -> None:
        while True:
            # get the item from the previous stage.
            item = self.in_queue.get()
            # fold the item
            print(f"\t\tFolding {item}")
            time.sleep(1)
            print(f"\t\t\t{item} done")
            self.in_queue.task_done()


class Pipeline:
    """ Represents a washer, dryer and folder linked by queues. """

    def assemble_laundry_for_washing(self):
        item_count = 8
        items_in = Queue(item_count)
        for item_num in range(item_count):
            items_in.put(f'item no {item_num}')
        return items_in

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
