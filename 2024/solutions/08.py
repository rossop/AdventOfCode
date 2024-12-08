"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
import sys
from typing import Any, Dict, List
from typing import NewType, Tuple
from collections import (
    defaultdict
)
from itertools import combinations

import math

Coordinate = NewType('Coordinate', Tuple[int, int])

input_directory: str = os.path.join(
    os.path.dirname(
        os.path.abspath(
            os.path.dirname(__file__)
        )
    ), 'in'
)


def read_input(file_name: str) -> Dict[str, Any]:
    """Reads input from a specified file and separates metadata for test files.

    Args:
        file_name (str): Name of the input file (.in or .test)

    Returns:
        Dict[str, Any]: Dictionary containing:
            - 'data': Raw string of input data
            - 'answer_a': Expected answer for part 1 (None for .in files)
            - 'answer_b': Expected answer for part 2 (None for .in files)
    """
    file_path: str = os.path.join(input_directory, file_name)
    result: Dict[str, Any] = {
        'data': None,
        'answer_a': None,
        'answer_b': None
    }

    with open(file_path, 'r', encoding='utf-8') as file:
        content: str = file.read()

        # Handle .test files with metadata
        if file_name.endswith('.test'):
            # Find the data section between Example data marker and answer
            # section
            data_start: int = content.find('Example data')
            if data_start != -1:
                data_start = content.find('\n', data_start) + 1
                data_end: int = content.find('\n-----------------', data_start)
                if data_end != -1:
                    result['data'] = content[data_start:data_end].strip()

            # Extract answers if present
            answer_section: str = content[data_end:] if data_end != -1 else ''
            for line in answer_section.splitlines():
                if line.startswith('answer_a:'):
                    ans: str = line.split(':')[1].strip()
                    result['answer_a'] = ans if ans != '-' else None
                elif line.startswith('answer_b:'):
                    ans: str = line.split(':')[1].strip()
                    result['answer_b'] = ans if ans != '-' else None

        # Handle regular .in files
        else:
            result['data'] = content.strip()

    return result


def process(raw_data: str) -> Any:
    """Processes the input data.
    """
    processed_data: List[List[str]] = [
        list(line) for line in raw_data.splitlines()
    ]

    return processed_data


def find_antennas_position(data: Any) -> Dict[str, List[Coordinate]]:
    """Find position of antennas
    """
    antenna_positions: Dict[str, List[Coordinate]] = defaultdict(list)

    for r, line in enumerate(data):
        for c, char in enumerate(line):
            if is_antenna(char):
                antenna_positions[char].append((r, c))
    return antenna_positions


def diff(
    a: Coordinate,
    b: Coordinate
) -> Coordinate:
    """Returns the difference between two Coordinates"""
    assert len(a) == len(b), "Coordinate must have same dimensions"
    return tuple(a[i] - b[i] for i in range(len(a)))


def summ(
    a: Coordinate,
    b: Coordinate
) -> Coordinate:
    """Returns the sum between two Coordinates"""
    assert len(a) == len(b), "Coordinate must have same dimensions"
    return tuple(a[i] + b[i] for i in range(len(a)))


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.

    Args:
        data (Any): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """
    antenna_positions: Dict[str, List[Coordinate]
                            ] = find_antennas_position(data)
    rows: int = len(data)
    cols: int = len(data[0])

    occupied_positions: List[Coordinate] = []
    list_of_antinodes: List[Coordinate] = []

    # Collect all antenna positions
    for vals in antenna_positions.values():
        occupied_positions.extend(vals)

    # For each frequency group
    for vals in antenna_positions.values():
        if len(vals) < 2:
            continue

        # Check each pair of antennas
        for ant1, ant2 in combinations(vals, 2):
            # Calculate vector between antennas
            diff_vector: Coordinate = diff(ant2, ant1)

            # Calculate antinodes (one at distance beyond each antenna)
            antinode1: Coordinate = (
                ant1[0] - diff_vector[0],
                ant1[1] - diff_vector[1]
            )
            antinode2: Coordinate = (
                ant2[0] + diff_vector[0],
                ant2[1] + diff_vector[1]
            )

            # Add valid antinodes
            for antinode in [antinode1, antinode2]:
                if (0 <= antinode[0] < rows and 0 <= antinode[1] < cols and
                        antinode not in list_of_antinodes):
                    # and antinode not in occupied_positions):
                    list_of_antinodes.append(antinode)

    return len(list_of_antinodes)


def is_antenna(char: str) -> bool:
    """Finds characters that satisfy antenna definition"""
    return char.isalnum()


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.

    Args:
        data (List[str]): The input data for the challenge.

    Returns:
        Any: The result of the solution for part two.
    """
    antenna_positions: Dict[str, List[Coordinate]] = \
        find_antennas_position(data)
    rows: int = len(data)
    cols: int = len(data[0])
    list_of_antinodes: List[Coordinate] = []

    # For each frequency group
    for vals in antenna_positions.values():
        if len(vals) < 2:
            continue

        # Check each pair of antennas
        for ant1, ant2 in combinations(vals, 2):
            # Calculate vector between antennas
            diff_vector: Coordinate = diff(ant2, ant1)

            # Get the GCD of the vector components to find the minimum step
            gcd: int = abs(math.gcd(diff_vector[0], diff_vector[1])) if \
                diff_vector[0] and diff_vector[1] else \
                max(abs(diff_vector[0]), abs(diff_vector[1]))
            step_vector: Coordinate = (
                diff_vector[0] // gcd,
                diff_vector[1] // gcd
            )

            # Check all points along the line (including antennas)
            current: Coordinate = ant1
            while True:
                if (0 <= current[0] < rows and 0 <= current[1] < cols and
                        current not in list_of_antinodes):
                    list_of_antinodes.append(current)

                if current == ant2:
                    break

                current = summ(current, step_vector)

            # Continue the line in both directions
            # Backward from ant1
            current = summ(ant1, (-step_vector[0], -step_vector[1]))
            while 0 <= current[0] < rows and 0 <= current[1] < cols:
                if current not in list_of_antinodes:
                    list_of_antinodes.append(current)
                current = summ(current, (-step_vector[0], -step_vector[1]))

            # Forward from ant2
            current = summ(ant2, step_vector)
            while 0 <= current[0] < rows and 0 <= current[1] < cols:
                if current not in list_of_antinodes:
                    list_of_antinodes.append(current)
                current = summ(current, step_vector)

    return len(list_of_antinodes)


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'
    # infile: str = "08.test"
    unprocessed_data = read_input(infile)
    input_data = process(unprocessed_data['data'])

    result_part_one = solve_part_one(input_data)
    if result_part_one is not None:
        print(f"Part One: {result_part_one}")
    result_part_two = solve_part_two(input_data)
    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")
