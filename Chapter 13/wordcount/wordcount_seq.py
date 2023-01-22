#!/usr/bin/env python3


import os
import glob

from typing import List, Dict

Pathname = str
Word = str
from collections import Counter


def wordcount(filenames: List[Pathname]) -> Dict[Word, int]:
    """ Return a dictionary where the keys are words found within the files
        supplied, and the values are the counts of occurences of eack word.
        """
    word_counts: Dict[Word, int] = {}
    for filename in filenames:
        print(f"Calculating {filename}")
        with open(filename, encoding="UTF-8") as f:
            for line in f:
                words = line.lower().split()
                for word in words:
                    word_counts[word] = 1 + word_counts.get(word, 0)
    return word_counts

def wordcount_1(filenames: List[str]) -> Counter[Word]:
    """ Alternative to wordcount using python Counter
        """
    count = Counter()
    for filename in filenames:
        print(f"Calculating {filename}")
        with open(filename, encoding="UTF-8") as f:
            for line in f:
                words = [word.lower() for word in line.split()]
                count.update(words)
    return count

if __name__ == "__main__":
    data = list(
        glob.glob(f"{os.path.abspath(os.getcwd())}/input_files/*.txt"))
    result = wordcount_1(data)
    print(result)
