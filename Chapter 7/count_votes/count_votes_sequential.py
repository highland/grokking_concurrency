#!/usr/bin/env python3

"""Counting votes sequentially"""

import typing as T
import random
from collections import Counter


def process_votes(votes: T.List[int]) -> T.Dict[int, int]:
    counts = Counter(votes)
    return counts


if __name__ == "__main__":
    num_candidates = 3
    num_voters = 100000
    # generating a huge list of votes
    # each vote is an integer represents the selected candidate
    votes = [random.randint(1, num_candidates) for _ in range(num_voters)]
    counts = process_votes(votes)
    print(counts)
