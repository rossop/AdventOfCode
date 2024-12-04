"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
import sys
from typing import List, Any, Dict
from collections import Counter, defaultdict
import re

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
            # Find the data section between Example data marker and answer section
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
                    result['answer_a'] = int(ans) if ans != '-' else None
                elif line.startswith('answer_b:'):
                    ans: str = line.split(':')[1].strip()
                    result['answer_b'] = int(ans) if ans != '-' else None

        # Handle regular .in files
        else:
            result['data'] = content.strip()

    return result


def process(raw_data: str) -> Any:
    """Processes the input data.
    """
    # TODO: Implement the processing for the input data
    return None


def find_mul_patterns(data: List[str], pattern: str) -> List[str]:
    """Finds all occurrences of the pattern 'mul($1,$2)' in the input data.

    Args:
        data (List[str]): The input data for the challenge.

    Returns:
        List[str]: A list of matched patterns.
    """

    matches: List[str] = []

    found: List[str] = re.findall(pattern, data)
    matches.extend(found)

    return matches


def solve_part_one(data: List[str]) -> Any:
    """Solves part one of the challenge.

    Args:
        data (List[str]): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """

    pattern: str = r'mul\((\d+),(\d+)\)'
    mul_patterns: List[str] = find_mul_patterns(data, pattern)

    return sum(int(a) * int(b) for a, b in mul_patterns)


def solve_part_two(data: List[str]) -> Any:
    """Solves part two of the challenge.

    Args:
        data (List[str]): The input data for the challenge.

    Returns:
        Any: The result of the solution for part two.
    """
    pattern: str = r'(mul)\((\d*)(?:,(\d+))?\)|(do|don\'t)\(\)'
    mul_patterns: List[str] = find_mul_patterns(data, pattern)

    ans: int = 0
    allowed_to_mul: bool = True

    for mul_pattern in mul_patterns:
        if mul_pattern[0] == 'mul' and allowed_to_mul:
            ans += int(mul_pattern[1]) * int(mul_pattern[2])
        elif mul_pattern[3] == 'do':
            allowed_to_mul = True
        elif mul_pattern[3] == "don't":
            allowed_to_mul = False

    return ans


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'

    raw_data = read_input(infile)

    result_part_one = solve_part_one(raw_data['data'])
    if result_part_one is not None:
        print(f"Part One: {result_part_one}")
    result_part_two = solve_part_two(raw_data['data'])
    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")
