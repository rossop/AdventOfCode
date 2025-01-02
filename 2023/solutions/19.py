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
    workflows_section, parts_section = raw_data.strip().split("\n\n")

    workflows: Dict[str, List] = {}
    for line in workflows_section.splitlines():
        name, rules_raw = line.split("{", 1)
        name = name.strip()
        rules_raw = rules_raw.rstrip('}')

        # Parse rules and fallback
        rules = []
        for rule in rules_raw.split(','):
            if ":" in rule:
                condition, destination = rule.split(":")
                key = condition[0]
                cmp = condition[1]
                n = int(condition[2:])
                rules.append((key, cmp, n, destination.strip()))
            else:
                fallback = rule.strip()
                workflows[name] = (rules, fallback)

    parts = []
    for line in parts_section.splitlines():
        part_data = {}
        for segment in line.strip("{}").split(","):
            key, value = segment.split("=")
            part_data[key.strip()] = int(value)
        parts.append(part_data)

    return workflows, parts



def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        return None

    workflows, parts = data

    ops = {
        ">" : int.__gt__,
        "<" : int.__lt__
    }

    def accept(item, name: str = "in") -> bool:
        """Recursive function to determine if a part is accepted
        """
        if name == "R":
            return False
        if name == "A":
            return True

        rules, fallback = workflows[name]
        for key, cmp, n, taget in rules:
            if ops[cmp](item[key], n):
                return accept(item, taget)
        return accept(item, fallback)

    total: int = 0
    for item in parts:
        if accept(item):
            total += sum(item.values())

    return total


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.
    """
    workflows, _ = data  # We only need workflows for part two

    def count(ranges, name="in"):
        if name == "R":
            return 0
        if name == "A":
            product = 1
            for lo, hi in ranges.values():
                product *= hi - lo + 1
            return product

        rules, fallback = workflows[name]
        total = 0

        for key, cmp, n, target in rules:
            lo, hi = ranges[key]
            if cmp == "<":
                T = (lo, min(n - 1, hi))
                F = (max(n, lo), hi)
            else:
                T = (max(n + 1, lo), hi)
                F = (lo, min(n, hi))

            # Process "True" range
            if T[0] <= T[1]:
                copy = dict(ranges)
                copy[key] = T
                total += count(copy, target)

            # Update "False" range
            if F[0] <= F[1]:
                ranges = dict(ranges)
                ranges[key] = F
            else:
                break
        else:
            total += count(ranges, fallback)

        return total

    # Initialize ranges and start counting
    ranges = {key: (1, 4000) for key in "xmas"}
    return count(ranges)


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
