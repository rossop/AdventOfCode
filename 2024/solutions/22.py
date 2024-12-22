"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides secret_num structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

import os
import sys
from typing import Any, List, Optional, Tuple

from pathlib import Path

# Add the parent directory of 'utils' to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import utils  # noqa: E402, F401

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
    return list(
        map(
            int,
            raw_data.splitlines()
        )
    )


def solve(data: Any) -> Any:
    """Solves part one and part two of the challenge.
    """
    if data is None:
        return None

    def mix(secret_num: int, new_num: int) -> int:
        """Mix two number using XOR
        """
        return secret_num ^ new_num

    def prune(secret_num: int, pruning_num: int = 16777216) -> int:
        """Prune new number out of secret_num
        """
        return secret_num % pruning_num

    part_one_ans: int = 0
    # Pattern -> List of prices (one per buyer)
    pattern_scores: dict[tuple[int, ...], list[int]] = {}

    for start_num in data:
        # Generate sequence
        nums: list[int] = [start_num]
        current_num: int = start_num

        for i in range(2000):
            # Process 1: First multiply by 64 and mix
            current_num = prune(mix(current_num * 64, current_num))
            # Process 2: Then divide by 32 and mix
            current_num = prune(mix(current_num // 32, current_num))
            # Process 3: Finally multiply by 2048 and mix
            current_num = prune(mix(current_num * 2048, current_num))
            nums.append(current_num)

        part_one_ans += current_num
        prices: List[int] = [n % 10 for n in nums]
        changes: List[int] = [prices[i+1] - prices[i]
                              for i in range(len(prices)-1)]

        # Record FIRST occurrence of each pattern for this buyer
        seen_patterns: set[tuple[int, ...]] = set()
        for i in range(len(changes)-3):
            pattern = tuple(changes[i:i+4])
            if pattern not in seen_patterns:  # Only record first occurrence
                seen_patterns.add(pattern)
                if pattern not in pattern_scores:
                    pattern_scores[pattern] = [prices[i+4]]  # Start new list
                else:
                    pattern_scores[pattern].append(
                        prices[i+4])  # Add to existing list

    pattern_sums = {pattern: sum(prices)
                    for pattern, prices in pattern_scores.items()}

    part_two_ans: int = max(pattern_sums.values())
    return part_one_ans, part_two_ans


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'

    file_path: str = os.path.join(input_directory, infile)
    unprocessed_data = utils.read_input(file_path)
    input_data = process(unprocessed_data['data'])

    result_part_one, result_part_two = solve(input_data)
    if result_part_one is not None:
        print(f"Part One: {result_part_one}")
    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")
