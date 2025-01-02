"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

from collections import defaultdict, deque
import os
from pprint import pprint
from re import A
import sys
from typing import Any, Deque, Dict, List, Optional, Set

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
    modules: Dict = {}
    for line in raw_data.splitlines():
        parts = line.split("->")
        name = parts[0].strip()
        destinations = (
            [dest.strip() for dest in parts[1].split(",")]
            if len(parts) > 1 else []
        )
        module_type: Optional[str] = None
        if name.startswith('%'):  # flip-flop
            module_type = '%'
            name = name.lstrip(module_type)
        elif name.startswith('&'):  # conjunction module
            module_type = '&'
            name = name.lstrip(module_type)
        elif name == "broadcaster":
            module_type = 'broadcaster'

        modules[name] = {
            "type": module_type,
            "destinations": destinations,
            "state": "low" if module_type in ('%', None) else None,
            "memory": defaultdict(lambda: "low")
            if module_type == '&' else None  # Memory for conjunctions
        }

    return modules


def traverse_modules(modules):
    """Simulate current traversing modules"""
    pulse_queue: Deque = deque([("broadcaster", "low")])
    pulse_counts = {"low": 0, "high": 0}

    while pulse_queue:
        current, pulse_level = pulse_queue.popleft()
        pulse_counts[pulse_level] += 1

        if current not in modules:  # Handle unknown modules
            continue

        module = modules[current]

        if module["type"] == "%":
            if pulse_level == "low":
                # Update the state and send new pulse
                module["state"] = "high" if module["state"] == "low" else "low"
                new_pulse = "high" if module["state"] == "high" else "low"
                pulse_queue.extend(
                    (dest, new_pulse) for dest in module["destinations"]
                )

        elif module["type"] == "&":
            module["memory"][current] = pulse_level
            if all(value == "high" for value in module["memory"].values()):
                new_level: str = "low"
            else:
                new_level: str = "high"

            pulse_queue.extend(
                (dest, new_level) for dest in module["destinations"]
            )

        elif module["type"] == "broadcaster":
            pulse_queue.extend(
                (dest, pulse_level) for dest in module["destinations"]
            )

    return pulse_counts


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        return None

    total_pulse_counts: Dict[str, int] = {"low": 0, "high": 0}

    for _ in range(1000):  # Simulate pushing the button 1000 times
        currents: Dict[str, int] = traverse_modules(data)
        total_pulse_counts['low'] += currents['low']
        total_pulse_counts['high'] += currents['high']

    return total_pulse_counts['high'] * total_pulse_counts['low']


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.
    """
    # TODO: Implement the solution for part two
    return None


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
