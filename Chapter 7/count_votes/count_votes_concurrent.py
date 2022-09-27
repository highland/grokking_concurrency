#!/usr/bin/env python3

"""Counting votes using Fork/Join pattern"""

import typing as T
import random
from threading import Thread
from collections import Counter


class StaffMember(Thread):
    def __init__(self, votes: T.List[int]):
        super().__init__()
        self.votes = votes
        
    def run(self):
        self.counts = Counter(self.votes)
    
    def join(self) -> T.Dict[int, int]:
        super().join()
        return self.counts


def process_votes(votes: T.List[int]) -> None:
    jobs = []
    vote_count = len(votes)
    member_count = 4
    vote_per_pile = vote_count // member_count

    # ---- Fork step ----
    for i in range(member_count):
        pile = votes[i * vote_per_pile:i * vote_per_pile + vote_per_pile]
        p = StaffMember(pile)
        jobs.append(p)
    
    for j in jobs:
        j.start()
    # ---- End Fork step ----
    # ---- Join step ----
    votes_summaries = []
    for j in jobs:
        votes_summaries.append(j.join())

    total_summary = Counter()
    for vote_summary in votes_summaries:
        total_summary.update(vote_summary)
    print(f"Total number of votes: {total_summary}")
    # ---- End Join step ----


if __name__ == "__main__":
    num_candidates = 3
    num_voters = 100000
    # generating a huge list of votes
    # each vote is an integer represents the selected candidate
    votes = [random.randint(1, num_candidates) for _ in range(num_voters)]
    process_votes(votes)
