#!/usr/bin/env python3

"""Program for cracking the password consisting of only numbers using multi cores in parallel"""

import os
import math
import time
import typing as T
import hashlib
from multiprocessing import Pool, Manager

Flag = T.TypeVar('multiprocessing.Event')


def get_combinations(*, length: int, min_number: int = 0, max_number: int = None) -> T.List[str]:
    """Generate all possible password combinations"""
    if not max_number:
        # calculating maximum number based on the length
        max_number = int(math.pow(10, length) - 1)
    # go through all possible combinations in a given range and convert to strings of given length
    return [f'{i:0>{length}}' for i in range(min_number, max_number + 1)]


def get_crypto_hash(password: str) -> str:
    """"Calculating cryptographic hash of the password"""
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(expected_crypto_hash: str, possible_password: str) -> bool:
    actual_crypto_hash = get_crypto_hash(possible_password)
    # compare the resulted cryptographic hash with the one stored on the system
    return expected_crypto_hash == actual_crypto_hash


def get_ranges(num_ranges: int, length: int) -> T.List[T.Tuple[int, int]]:
    """Splitting the passwords into batches using break points"""
    max_number = int(math.pow(10, length) - 1)
    start_points = [int(max_number / num_ranges * i) for i in range(num_ranges)]
    end_points = [start_point - 1 for start_point in start_points[1:]] + \
        [max_number]    # creating a range of numbers for each process
    return zip(start_points, end_points)


def crack_batch(crypto_hash: str, length: int, start: int, end: int,
                flag: Flag, result: list) -> str:
    """Brute force the password combinations"""
    print(f'checking {start} to {end}')
    combinations = get_combinations(
        length=length, min_number=start, max_number=end)
    for combination in combinations:
        if flag.is_set():   #  some other process found it
            return
        if check_password(crypto_hash, combination):   # found it
            result.append(combination)
            flag.set()
            return
    return   # not found


def crack_password_parallel(crypto_hash: str, length: int) -> None:
    """Orchestrate cracking the password between different processes"""
    # getting number of available processors
    num_cores = os.cpu_count()

    print("Processing number combinations concurrently")
    start_time = time.perf_counter()

    # set up inter-process communication
    shared = Manager()
    flag = shared.Event()
    result = shared.list()

    # processing each batch in a separate process concurrently
    with Pool() as pool:
        for start_point, end_point in get_ranges(num_cores, length):
            pool.apply_async(
                crack_batch, (crypto_hash, length, start_point, end_point, flag, result))
            print(f"Batch submitted checking {start_point} to {end_point}")
        print("Waiting for batches to finish")
        pool.close()
        pool.join()

    print(f'Found password {result[0]}')

    process_time = time.perf_counter() - start_time
    print(f"PROCESS TIME: {process_time}")


if __name__ == "__main__":
    crypto_hash = "e24df920078c3dd4e7e8d2442f00e5c9ab2a231bb3918d65cc50906e49ecaef4"
    length = 8
    crack_password_parallel(crypto_hash, length)
