"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

import os
import sys
import math
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
    def parse_line(line: str):
        info: List[str] = list(
            map(
                lambda x: x.strip(':'),
                line.split()
            )
        )
        return info[0], list(map(int, info[1:]))

    return dict(map(parse_line, raw_data.splitlines()))


def simulate_race(
    time: int,
    distance: int):
    """
    """
    count: int = 0
    for speed in range(time):
        session_time: int = time - speed
        if distance < speed * session_time:
            count += 1

    return count


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        return None
    times: List[int] = data['Time']
    distances: List[int] = data['Distance']

    return math.prod(map(simulate_race,times, distances))


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.
    """
    if data is None:
        return None
    time: int = int("".join(map(str, data['Time'])))
    distance: int = int("".join(map(str, data['Distance'])))

    return simulate_race(time, distance)


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
