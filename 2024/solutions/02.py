"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
from typing import List, Any, Dict
from collections import Counter

import sys
from collections import defaultdict, Counter

input_directory: str = os.path.join(
    os.path.dirname(
        os.path.abspath(
            os.path.dirname(__file__)
        )
    ), 'in'
)


def read_input(file_name: str) -> Any:
    """Reads the input from a specified file.

    Args:
        file_name (str): The name of the input file.

    Returns:
        Any: Processed data.
    """
    file_path = os.path.join(input_directory, file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        rows: List[str] = file.read().strip().splitlines()
        data: List[List[int]] = [
            list(
                map(int, row.split())
            ) for row in rows
        ]
        return data


def is_good(xs):
    """Check if a sequence is good."""
    inc_or_dec = (xs == sorted(xs) or xs == sorted(xs, reverse=True))
    ok = True
    for i in range(len(xs)-1):
        diff = abs(xs[i]-xs[i+1])
        if not 1 <= diff <= 3:
            ok = False
    return inc_or_dec and ok


if __name__ == "__main__":
    input_data = read_input('02.in')

    p1 = 0
    p2 = 0
    for line in input_data:
        if is_good(line):
            p1 += 1

        good = False
        for j in range(len(line)):
            subline = line[:j] + line[j+1:]
            if is_good(subline):
                good = True
        if good:
            p2 += 1

    print(f"Part One: {p1}")
    print(f"Part Two: {p2}")
