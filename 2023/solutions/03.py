"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
import sys
from typing import Any, Dict, List, Tuple
from collections import defaultdict

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
        [char for char in line] for line in raw_data.splitlines()
    ]
    return processed_data


def solve(data: Any) -> Any:
    """Solves part one of the challenge.

    Args:
        data (Any): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """
    rows: int = len(data)
    cols: int = len(data[0])
    ans_pt1: int = 0
    ans_pt2: int = 0

    def is_symbol(char: str) -> bool:
        """Checks if a character is a symbol (not a digit or period)."""
        return not char.isdigit() and char != '.'

    def has_adjacent_symbol(r: int, c: int) -> bool:
        """Checks if position has an adjacent symbol."""
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == dc == 0:
                    continue
                rr, cc = r + dr, c + dc
                if 0 <= rr < rows and 0 <= cc < cols:
                    if is_symbol(data[rr][cc]):
                        return True
        return False

    def has_adjacent_gear(r: int, c: int) -> Tuple[bool, int, int]:
        """Checks if position has an adjacent gear."""
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == dc == 0:
                    continue
                rr, cc = r + dr, c + dc
                if 0 <= rr < rows and 0 <= cc < cols:
                    if data[rr][cc] == "*":
                        return True, rr, cc
        return False, None, None

    gear_neighbours = defaultdict(list)

    r: int = 0
    while r < rows:
        c: int = 0
        while c < cols:
            if data[r][c].isdigit():
                # Found start of a number
                num_str: str = ''
                valid: bool = False
                gear_neighbour: bool = False
                gr, gc = None, None

                # Get full number and check for adjacent symbols
                while c < cols and data[r][c].isdigit():
                    num_str += data[r][c]
                    if not valid:
                        valid = has_adjacent_symbol(r, c)
                    if not gear_neighbour:
                        gear_neighbour, gr, gc = has_adjacent_gear(r, c)
                    c += 1

                if valid:
                    ans_pt1 += int(num_str)

                if gear_neighbour and (gr is not None) and (gc is not None):
                    gear_neighbours[(gr, gc)].append(int(num_str))
            else:
                c += 1
        r += 1

    for _, vals in gear_neighbours.items():
        if len(vals) > 1:
            prod: int = 1
            for v in vals:
                prod *= v
            ans_pt2 += prod

    return ans_pt1, ans_pt2


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'
    # infile: str = '03.test'
    unprocessed_data = read_input(infile)
    input_data = process(unprocessed_data['data'])

    result_part_one, result_part_two = solve(input_data)
    if result_part_one is not None:
        print(f"Part One: {result_part_one}")
    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")
