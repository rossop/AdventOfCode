"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

import os
import sys
from typing import Any, List

from pathlib import Path

# Add the parent directory of 'utils' to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import utils  # noqa: E402


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
        [
            line.split()[0], list(
                map(
                    int,
                    line.split()[1].split(',')
                )
            )
        ] for line in raw_data.splitlines()
    ]


def count_arrangements(cfg: str, nums: tuple, cache: dict = None) -> int:
    """Recursively counts valid arrangements of springs with memoization.
    """
    if cache is None:
        cache = {}

    key: tuple = (cfg, nums)
    if key in cache:
        return cache[key]

    if cfg == "":
        return 1 if nums == () else 0

    if nums == ():
        return 0 if "#" in cfg else 1

    result: int = 0

    if cfg[0] in ".?":
        result += count_arrangements(cfg[1:], nums, cache)

    if cfg[0] in "#?":
        if (nums[0] <= len(cfg) and
            "." not in cfg[:nums[0]] and
                (nums[0] == len(cfg) or cfg[nums[0]] != "#")):
            if nums[0] == len(cfg):
                result += count_arrangements("", nums[1:], cache)
            else:
                result += count_arrangements(cfg[nums[0] + 1:],
                                             nums[1:], cache)

    cache[key] = result
    return result


def solve_part_one(data: List[List[Any]]) -> int:
    """Solves part one of the challenge.
    """
    if data is None:
        error_msg: str = "Data not properly loaded"
        raise ValueError(error_msg)

    total: int = 0
    for cfg, nums in data:
        nums_tuple: tuple = tuple(nums)  # Convert list to tuple for recursion
        total += count_arrangements(cfg, nums_tuple)

    return total


def solve_part_two(data: List[List[Any]]) -> int:
    """Solves part two of the challenge by unfolding the spring patterns.
    """
    if data is None:
        error_msg: str = "Data not properly loaded"
        raise ValueError(error_msg)

    # Add memoization cache
    cache: dict = {}
    total: int = 0

    for cfg, nums in data:
        # Unfold the pattern 5 times
        unfolded_cfg: str = "?".join([cfg] * 5)  # Join with ? between copies
        unfolded_nums: tuple = tuple(nums) * 5    # Repeat the numbers 5 times
        total += count_arrangements(unfolded_cfg, unfolded_nums, cache)

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
