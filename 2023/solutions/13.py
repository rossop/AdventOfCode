"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

import os
import sys
from typing import Any, Dict, List, Set

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
    print(raw_data)
    return [
        [
            [
                c for c in line
            ] for line in grid.splitlines()
        ] for grid in raw_data.split('\n\n')
    ]


def find_reflection(grid: List[List[str]]) -> int:
    """Finds coordinates of the refelctions axis.
    """
    for r in range(1, len(grid)):
        above: List[List[str]] = grid[:r][::-1]
        below: List[List[str]] = grid[r:]

        above = above[:len(below)]
        below = below[:len(above)]

        if above == below:
            return r

    return 0


def find_potential_reflection(grid: List[List[str]]) -> int:
    """Finds coordinates of the refelctions axis.
    """
    for r in range(1, len(grid)):
        above: List[List[str]] = grid[:r][::-1]
        below: List[List[str]] = grid[r:]

        condition: bool = (
            sum(
                sum(
                    # pair up possible eqiivalent values
                    0 if a == b else 1 for a, b in zip(x, y)
                # pair up possible symmetric lines
                ) for x, y in zip(above, below)
            ) == 1  # if there is a single mistmatch
        )
        if condition:
            return r

    return 0


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        error_msg: str = "Data not properly loaded"
        raise ValueError(error_msg)

    total: int = 0
    for grid in data:
        row = find_reflection(grid)
        total += row * 100

        col = find_reflection(list(zip(*grid)))
        total += col


    return total


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.
    """
    if data is None:
        error_msg: str = "Data not properly loaded"
        raise ValueError(error_msg)

    total: int = 0
    for grid in data:
        row = find_potential_reflection(grid)
        total += row * 100

        col = find_potential_reflection(list(zip(*grid)))
        total += col


    return total


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
