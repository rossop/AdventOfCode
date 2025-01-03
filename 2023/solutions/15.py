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
    return raw_data.split(',')


def hash(instructions: str):
    """Process and hash a string
    """
    curr: int = 0
    for c in instructions:
        curr += ord(c)
        curr *= 17
        curr %= 256
    return curr


def solve(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        return None

    boxes = [[] for _ in range(256)]
    focal_lengths = {}

    part_one_answer: int = 0
    for instructions in data:
        part_one_answer += hash(instructions)

        if '-' in instructions:
            label = instructions[:-1]
            index = hash(label)
            if label in boxes[index]:
                boxes[index].remove(label)
        elif '=' in instructions:
            label, length = instructions.split('=')
            length: int = int(length)

            index: int = hash(label)
            if label not in boxes[index]:
                boxes[index].append(label)

            focal_lengths[label] = length

    part_two_answer: int = 0

    for box_number, box in enumerate(boxes, 1):
        for lens_slot, label in enumerate(box, 1):
            part_two_answer += box_number * lens_slot * focal_lengths[label]

    return part_one_answer, part_two_answer


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
