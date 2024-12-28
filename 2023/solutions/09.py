"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

import os
import sys
from typing import Any, Dict, List, Optional, Set
from pprint import pprint

from pathlib import Path

# Add the parent directory of 'utils' to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import utils

input_directory: str = os.path.join(
    os.path.dirname(
        os.path.abspath(
            os.path.dirname(__file__)
        )
    ), 'in'
)


def process(raw_data: str) -> Any:
    """Processes the input data.
    """
    return [
        list(
            map(
                int,
                line.split()
            )
        ) for line in raw_data.splitlines()
    ]


def find_next_value(values: List[int]):
    """Given a list of integers find the next value in the sequence
    """
    layers: List[List[int]] = [values]

    while any(x != 0 for x in layers[-1]):
        lst: List[int] = layers[-1]
        diffs = [b - a for a, b in zip(lst, lst[1:])]
        layers.append(diffs)

    new_val: int = 0
    for layer in layers[::-1]:
        new_val = layer[-1] + new_val
    return new_val


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        return None

    ans: int = 0
    for line in data:
        ans += find_next_value(line)

    return ans


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.
    """
    if data is None:
        return None

    ans: int = 0
    for line in data:
        ans += find_next_value(line[::-1])

    return ans


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'

    file_path: str = os.path.join(input_directory, infile)
    unprocessed_data = utils.read_input(file_path)
    input_data = process(unprocessed_data['data'])

    result_part_one = solve_part_one(input_data)
    if result_part_one is not None:
        print(f"Part One: {result_part_one}")
    result_part_two = solve_part_two(input_data)
    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")
