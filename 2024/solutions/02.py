"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
from typing import List, Any, Dict
from collections import Counter

import sys
from collections import defaultdict, Counter

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

    Args:
        file_name (str): The name of the input file.

    Returns:
        Any: Processed data.
    """
    rows: List[str] = raw_data.strip().splitlines()
    data: List[List[int]] = [
        list(
            map(int, row.split())
        ) for row in rows
    ]
    return data


def is_good(xs):
    """Check if a sequence is good."""
    inc_or_dec = (xs == sorted(xs) or xs == sorted(xs, reverse=True))
    ok = True
    for i in range(len(xs)-1):
        diff = abs(xs[i]-xs[i+1])
        if not 1 <= diff <= 3:
            ok = False
    return inc_or_dec and ok


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'

    raw_data = read_input(infile)
    input_data = process(raw_data['data'])

    p1 = 0
    p2 = 0
    for row in input_data:
        if is_good(row):
            p1 += 1

        good = False
        for j in range(len(row)):
            subline = row[:j] + row[j+1:]
            if is_good(subline):
                good = True
        if good:
            p2 += 1

    print(f"Part One: {p1}")
    print(f"Part Two: {p2}")
