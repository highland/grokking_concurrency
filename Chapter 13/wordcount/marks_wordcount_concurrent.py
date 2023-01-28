# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 14:23:22 2023

@author: Mark
"""
import asyncio
from collections import Counter
from pathlib import Path
import aiofiles


async def count_words_by_line(filename: str) -> Counter:
    """ async generator to count words in a line in a file """
    print(f"Running map for {filename}")
    async with aiofiles.open(filename, encoding="ISO-8859-1") as file:
        async for line in file:
            yield Counter(line.lower().split())


async def count_words_in_file(filename: str) -> Counter:
    """ async generator to count words in a file """
    file_count = Counter()
    async for count in count_words_by_line(filename):
        file_count.update(count)
    yield file_count


async def count_words() -> Counter:
    """ Count words in text files concurrently """
    total_count = Counter()
    for filename in Path.cwd().glob('./input_files/*.txt'):
        async for count in count_words_in_file(filename):
            total_count.update(count)
    return total_count

if __name__ == "__main__":
    word_count = asyncio.run(count_words())
    print(f"Found {len(word_count)} words")
    print(f"10 most common were {word_count.most_common(10)}")
