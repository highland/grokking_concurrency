#!/usr/bin/env python3

"""Counting votes using Fork/Join pattern"""

from typing import List, Mapping
import random
from threading import Thread
from collections import Counter


Candidate = int
Vote = Candidate
Count = int
CountedVotes = Mapping[Candidate, Count]

class StaffMember:
    """ One of a number of people tasked with counting votes.
            Each is given a list of votes to count.
            A vote references one of the candidates.
    """
    def __init__(self, votes: List[Vote]):
        super().__init__()
        self.votes = votes
        self.thread = Thread() 

    def start(self) -> None:
        self.thread.start()
        self.counts: CountedVotes = Counter(self.votes)

    def join(self) -> CountedVotes:
        self.thread.join()
        return self.counts


def process_votes(votes: List[Vote]) -> None:
    jobs: List[StaffMember] = []
    vote_count = len(votes)
    member_count = 4
    vote_per_pile = vote_count // member_count

    # ---- Fork step ----
    for i in range(member_count):
        pile: List[Vote] = votes[i * vote_per_pile:i * vote_per_pile + vote_per_pile]
        p = StaffMember(pile)
        jobs.append(p)

    for j in jobs:
        j.start()
    # ---- End Fork step ----
    # ---- Join step ----
    votes_summaries: List[CountedVotes] = []
    for j in jobs:
        votes_summaries.append(j.join())

    total_summary: CountedVotes = Counter()
    for vote_summary in votes_summaries:
        total_summary.update(vote_summary)
    print(f"Total number of votes: {total_summary}")
    # ---- End Join step ----


if __name__ == "__main__":
    candidate = int
    num_candidates = 3
    num_voters = 100000
    # generating a huge list of votes
    # each vote is an integer represents the selected candidate
    votes: List[Vote] = [random.randint(1, num_candidates) for _ in range(num_voters)]
    process_votes(votes)
