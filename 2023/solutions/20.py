"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

import os
import sys
from collections import deque
from typing import Any, Dict, Deque, Tuple, List

from pathlib import Path
import math
import copy
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
    modules: Dict[str, Dict] = {}
    broadcast_targets: List[str] = []

    for line in raw_data.splitlines():
        left, right = line.strip().split(" -> ")
        outputs = right.split(", ")

        if left == "broadcaster":
            broadcast_targets = outputs
        else:
            type_char = left[0]
            name = left[1:]
            modules[name] = {
                "name": name,
                "type": type_char,
                "outputs": outputs,
                "memory": "off" if type_char == "%" else {}
            }

    # Initialize conjunction module memories
    for name, module in modules.items():
        for output in module["outputs"]:
            if output in modules and modules[output]["type"] == "&":
                modules[output]["memory"][name] = "lo"

    return modules, broadcast_targets


def traverse_modules(data: Tuple[Dict, List[str]]) -> Dict[str, int]:
    """Simulate one button press and count pulses.
    """
    modules, broadcast_targets = data
    pulse_queue: Deque[Tuple[str, str, str]] = deque(
        [("broadcaster", dest, "lo") for dest in broadcast_targets]
    )
    pulse_counts = {"lo": 1, "hi": 0}  # Start with 1 lo for button press

    while pulse_queue:
        origin, target, pulse = pulse_queue.popleft()
        pulse_counts[pulse] += 1

        if target not in modules:
            continue

        module = modules[target]

        if module["type"] == "%":
            if pulse == "lo":
                module["memory"] = "on" if module["memory"] == "off" else "off"
                new_pulse = "hi" if module["memory"] == "on" else "lo"
                for dest in module["outputs"]:
                    pulse_queue.append((target, dest, new_pulse))

        elif module["type"] == "&":
            module["memory"][origin] = pulse
            new_pulse = "lo" if all(
                x == "hi" for x in module["memory"].values()) else "hi"
            for dest in module["outputs"]:
                pulse_queue.append((target, dest, new_pulse))

    return pulse_counts


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge."""
    if data is None:
        return None

    total_pulse_counts: Dict[str, int] = {"low": 0, "high": 0}

    for _ in range(1000):  # Simulate pushing the button 1000 times
        currents: Dict[str, int] = traverse_modules(data)
        total_pulse_counts['low'] += currents['lo']
        total_pulse_counts['high'] += currents['hi']

    return total_pulse_counts['high'] * total_pulse_counts['low']


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.
    """
    if data is None:
        return None

    modules, broadcast_targets = data

    # Find the module that feeds into rx
    (feed,) = [name for name, module in modules.items()
               if "rx" in module["outputs"]]

    cycle_lengths: Dict[str, int] = {}
    seen: Dict[str, int] = {name: 0 for name, module in modules.items()
                            if feed in module["outputs"]}

    press_count: int = 0

    while True:
        press_count += 1
        pulse_queue = deque([("broadcaster", x, "lo")
                             for x in broadcast_targets])

        while pulse_queue:
            origin, target, pulse = pulse_queue.popleft()

            if target not in modules:
                continue

            module = modules[target]

            if target == feed and pulse == "hi":
                seen[origin] += 1

                if origin not in cycle_lengths:
                    cycle_lengths[origin] = press_count
                else:
                    if press_count != seen[origin] * cycle_lengths[origin]:
                        raise AssertionError(
                            f"Cycle verification failed for {origin}"
                        )

                if all(seen.values()):
                    result: int = 1
                    for cycle_length in cycle_lengths.values():
                        result = (
                            result * cycle_length
                        ) // math.gcd(result, cycle_length)
                    return result

            if module["type"] == "%":
                if pulse == "lo":
                    module["memory"] = "on" if module["memory"] == "off" else "off"
                    new_pulse = "hi" if module["memory"] == "on" else "lo"
                    for dest in module["outputs"]:
                        pulse_queue.append((target, dest, new_pulse))
            else:
                module["memory"][origin] = pulse
                new_pulse = "lo" if all(
                    x == "hi" for x in module["memory"].values()) else "hi"
                for dest in module["outputs"]:
                    pulse_queue.append((target, dest, new_pulse))


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'

    file_path: str = os.path.join(input_directory, infile)
    unprocessed_data = utils.read_input(file_path)
    input_data = process(unprocessed_data['data'])


    result_part_one = solve_part_one(copy.deepcopy(input_data))
    if result_part_one is not None:
        print(f"Part One: {result_part_one}")
    result_part_two = solve_part_two(copy.deepcopy(input_data))
    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")
