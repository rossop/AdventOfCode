"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
import sys
from typing import List, Any, Dict


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
    data: List[str] = list(map(str.strip, raw_data.splitlines()))
    return data


def solve_part_one(data: List[str]) -> Any:
    """Solves part one of the challenge.

    Args:
        data (List[str]): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """
    answer: int = 0
    for line in data:
        p1: int = 0
        p2: int = len(line) - 1
        p1_found: bool = False
        p2_found: bool = False

        while p1 <= p2 and not (p1_found and p2_found):
            # Only move p1 if we haven't found a digit yet
            if not p1_found:
                if line[p1].isdigit():
                    p1_found = True
                else:
                    p1 += 1

            # Only move p2 if we haven't found a digit yet
            if not p2_found:
                if line[p2].isdigit():
                    p2_found = True
                else:
                    p2 -= 1

        if p1_found and p2_found:
            answer += int(line[p1] + line[p2])

    return answer


def solve_part_two(data: List[str]) -> Any:
    """Solves part two of the challenge.

    Args:
        data (List[str]): The input data for the challenge.

    Returns:
        Any: The result of the solution for part two.
    """
    # Map both spelled-out digits and numeric digits to their values
    digit_map: Dict[str, str] = {
        'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
        'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
        '1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
        '6': '6', '7': '7', '8': '8', '9': '9'
    }

    answer: int = 0

    for line in data:
        first_digit: str = ''
        last_digit: str = ''
        first_pos: int = float('inf')
        last_pos: int = -1

        # Find all possible digits (spelled out or numeric) and their positions
        for digit in digit_map.values():
            # Find leftmost occurrence
            pos = line.find(digit)
            if pos != -1 and pos < first_pos:
                first_pos = pos
                first_digit = digit_map[digit]

            # Find rightmost occurrence
            pos = line.rfind(digit)
            if pos != -1 and pos > last_pos:
                last_pos = pos
                last_digit = digit_map[digit]

        if first_digit and last_digit:
            answer += int(first_digit + last_digit)

    return answer


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'

    raw_data = read_input(infile)
    input_data = process(raw_data['data'])

    result_part_one = solve_part_one(input_data)
    if result_part_one is not None:
        print(f"Part One: {result_part_one}")

    result_part_two = solve_part_two(input_data)
    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")
