"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

import os
import sys
from typing import Any, Dict, List, Tuple

from pathlib import Path
import re
from math import gcd

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
    info: List[str] = raw_data.split('\n\n')
    instructions: str = info[0]

    pattern: str = r'([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)' # Part 1
    # pattern: str = r'([A-Z0-9]+) = \(([A-Z0-9]+), ([A-Z0-9]+)\)'
    matches = re.findall(pattern, info[1])
    network: Dict[str, Tuple[str, str]] = dict(
        map(
            lambda x: (x[0], ( x[1], x[2])),
            matches
        )
    )
    return instructions, network


def lcm(a: int, b: int) -> int:
    """Helper function to calculate the LCM of two numbers."""
    return a * b // gcd(a, b)


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        return None

    instr, network = data
    start: str = 'AAA'
    end: str = 'ZZZ'
    if start not in network:
        return None
    # translation_table: Dict[str, int] = str.maketrans({'R': 1, 'L': 0})

    index_instr: List[int] = [1 if char == 'R' else 0 for char in instr]
    curr: str = start
    counter: int = 0
    while curr != end:  # If current network node gets to end, stop
        possible_steps: Tuple[str, str] = network[curr]
        index: int = index_instr[counter % len(index_instr)]  # L or R
        curr = possible_steps[index]
        counter += 1

    return counter


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.
    """
    if data is None:
        return None

    instr, network = data

    start_strings: List[str] = [
        node for node in network.keys() if node.endswith('A')
    ]

    index_instr: List[int] = [1 if char == 'R' else 0 for char in instr]

    # Simulate each starting node to determine its cycle
    cycles: List[int] = []
    for start in start_strings:
        current = start
        steps = 0
        visited = {}  # Track visited nodes and the step count at the visit
        first_z = None
        cycle_length = 0

        while True:
            if current.endswith('Z'):
                if first_z is None:  # Record the first time we hit a Z node
                    first_z = current
                    cycle_length = steps
                elif current == first_z:  # If we loop back to the same Z node, stop
                    break

            # If we revisit a node at the same step count, we're in a loop
            if (current, steps % len(index_instr)) in visited:
                cycle_length = steps - visited[(current, steps % len(index_instr))]
                break

            # Mark this node as visited
            visited[(current, steps % len(index_instr))] = steps

            # Follow the current instruction
            steps += 1
            instruction_index = index_instr[steps % len(index_instr)]
            current = network[current][instruction_index]

        # Append the cycle length for this starting node
        cycles.append(cycle_length)

    # Calculate the LCM of all cycle lengths
    result = cycles.pop(0)
    for cycle in cycles:
        result = lcm(result, cycle)

    return result


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
