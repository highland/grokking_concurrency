#!/usr/bin/env python3

"""Counting votes sequentially"""

from typing import List, Mapping
import random
from collections import Counter

Candidate = int
Vote = Candidate
Count = int
CountedVotes = Mapping[Candidate, Count]


def process_votes(votes: List[int]) -> CountedVotes:
    counts: CountedVotes = Counter(votes)
    return counts


if __name__ == "__main__":
    num_candidates = 3
    num_voters = 100000
    # generating a huge list of votes
    # each vote is an integer represents the selected candidate
    votes: List[Vote] = [random.randint(
        1, num_candidates) for _ in range(num_voters)]
    counts = process_votes(votes)
    print(counts)
