#!/usr/bin/env python3

"""Implementing parking garage using semaphore for control critical section"""

import time
import random
import threading
import typing as T

TOTAL_SPOTS = 3


class Garage:
    cars: T.List[str]  # list of parked cars

    def __init__(self):
        self.semaphore = threading.Semaphore(TOTAL_SPOTS)
        self.cars_lock = threading.Lock()
        self.cars = []

    def count_parked_cars(self):
        return len(self.cars)

    def enter(self, car_name: str) -> None:
        """Enter the garage"""
        self.semaphore.acquire()
        with self.cars_lock:
            self.cars.append(car_name)
            print(f"{car_name} car parked")

    def exit(self, car_name: str) -> None:
        """Car exits the garage"""
        with self.cars_lock:
            self.cars.remove(car_name)
            print(f"{car_name} leaving")
        self.semaphore.release()


def park_car(garage: Garage, car_name: str) -> None:
    """Emulate parked car behavior"""
    garage.enter(car_name)
    time.sleep(random.uniform(1, 2))
    garage.exit(car_name)


def test_garage(garage: Garage, number_of_cars: int = 10):
    threads = []
    for car_num in range(number_of_cars):
        t = threading.Thread(target=park_car, args=(garage, f"car-{car_num}"))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    number_of_cars = 10
    garage = Garage()
    # test garage by concurrently arriving cars
    test_garage(garage, number_of_cars=number_of_cars)

    print("Number of parked car after a busy day:")
    print(f"Actual: {garage.count_parked_cars()}\nExpected: 0")
