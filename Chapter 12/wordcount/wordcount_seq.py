#!/usr/bin/env python3
""" A version of the author's original without unnecessary use of re module,
    type hints included,
    and improved variable names'
"""

import os
import glob

from typing import List, Dict

Pathname = str
Word = str


def wordcount(filenames: List[Pathname]) -> Dict[Word, int]:
    word_counts: Dict[Word, int] = {}
    for filename in filenames:
        print(f"Calculating {filename}")
        with open(filename) as f:
            for line in f:
                words = line.lower().split()
                for word in words:
                    word_counts[word] = 1 + word_counts.get(word, 0)
    return word_counts


if __name__ == "__main__":
    data = list(
        glob.glob(f"{os.path.abspath(os.getcwd())}/input_files/*.txt"))
    result = wordcount(data)
    print(result)

"""
Alternative to the above using Python Standard Library:
    
    from collections import Counter
    
    def wordcount(filenames: List[Pathname]) -> Dict[Word, int]:
        word_counts: Counter[Word] = Counter()
        for filename in filenames:
            print(f"Calculating {filename}")
            with open(filename) as f:
                for line in f:
                    words = line.lower().split()
                    word_counts.update(words)
        return word_counts
"""