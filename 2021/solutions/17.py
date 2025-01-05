"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# Add the parent directory of 'utils' to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import utils

input_directory: str = os.path.join(
    os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "in"
)


def process(raw_data: str) -> Any:
    """Processes the input data."""
    pattern: str = r"-?\d+"
    return list(map(int, re.findall(pattern, raw_data)))


def steps_for_dy(dy, miny, maxy):
    """move step vertically"""
    y: int = 0
    steps: int = 0
    valid: List[int] = []
    while y >= miny:
        if miny <= y <= maxy:
            valid.append(steps)
        y += dy
        dy -= 1
        steps += 1
    return valid


def can_land_dx(step: int, minx: int, maxx: int) -> bool:
    """Check if it cal land on platform"""
    for dx in range(1, maxx):
        x: int = 0
        for _ in range(step):
            x += dx
            if dx > 0:
                dx -= 1
        if minx <= x <= maxx:
            return True
    return False


def count_can_land_dx(step: int, minx: int, maxx: int) -> Set[int]:
    """"""
    total = set()
    for dx in range(0, maxx + 1):
        x = 0
        odx = dx
        for _ in range(step):
            x += dx
            if dx > 0:
                dx -= 1
        if minx <= x <= maxx:
            total.add(odx)
    return total


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge."""
    if data is None:
        return None
    minx: int
    maxx: int
    miny: int
    maxy: int
    minx, maxx, miny, maxy = data

    dy: int = -miny

    answer_part_one: Optional[int] = None
    while True:
        if any(can_land_dx(step, minx, maxx) for step in steps_for_dy(dy, miny, maxy)):
            answer_part_one = sum(range(1, dy + 1))
            break
        dy -= 1
    return answer_part_one


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge."""
    minx: int
    maxx: int
    miny: int
    maxy: int
    minx, maxx, miny, maxy = data

    total = 0

    for dy in range(miny - 1, -miny + 1):
        iter = set()
        for step in steps_for_dy(dy, miny, maxy):
            iter |= count_can_land_dx(step, minx, maxx)
        total += len(iter)
    return total


if __name__ == "__main__":
    day: str = __file__.rsplit("/", maxsplit=1)[-1].replace(".py", "")
    infile = sys.argv[1] if len(sys.argv) >= 2 else f"{day}.in"

    file_path: str = os.path.join(input_directory, infile)
    unprocessed_data = utils.read_input(file_path)
    input_data = process(unprocessed_data["data"])

    result_part_one = solve_part_one(input_data)
    if result_part_one is not None:
        print(f"Part One: {result_part_one}")
    result_part_two = solve_part_two(input_data)
    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")
