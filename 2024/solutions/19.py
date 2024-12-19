"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
import sys
from typing import Any, Dict, List, Set


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
    split_data: List[str] = raw_data.split('\n\n')
    data={
        "patterns": split_data[0].split(', '),
        "designs": split_data[1].splitlines()
    }
    return data


def can_form_design(
    patterns: List[str],
    design: str
) -> bool:
    """Check if design can be composed by available patterns
    """
    pattern_set: Set[str] = set(patterns)

    # Initialise DP table
    dp: List[bool] = [False] * (len(design) + 1)
    # Base case:
    dp[0] = True

    for i in range(1, len(design) + 1):
        for j in range(i):
            if dp[j] and design[j:i] in pattern_set:
                dp[i] = True
                break
    return dp[len(design)]


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        return None
    patterns: List[str] = data['patterns']
    designs: List[str] = data['designs']

    ans: int = 0
    for design in designs:
        if can_form_design(patterns, design):
            ans += 1

    return ans


def count_formations(
    patterns: List[str],
    design: str
) -> int:
    """Check how many design can be composed by available patterns
    """
    pattern_set: Set[str] = set(patterns)
    n: int = len(design)
    dp = [0] * (n + 1)
    dp[0] = 1 # one way to form an empty design

    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] > 0 and design[j:i] in pattern_set:
                dp[i] += dp[j]
    return dp[n]


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.
    """
    if data is None:
        return None
    patterns: List[str] = data['patterns']
    designs: List[str] = data['designs']

    ans: int = 0
    for design in designs:
        if can_form_design(patterns, design):
            ans += count_formations(patterns, design)

    return ans


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'

    unprocessed_data = read_input(infile)
    input_data = process(unprocessed_data['data'])

    result_part_one = solve_part_one(input_data)
    if result_part_one is not None:
        print(f"Part One: {result_part_one}")
    result_part_two = solve_part_two(input_data)
    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")
