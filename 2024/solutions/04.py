"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
import sys
from typing import List, Any, Dict, Tuple
from collections import Counter, defaultdict


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
    processed_data: List[List[str]] = []
    for line in raw_data.splitlines():
        row: List[str] = [char for char in line]
        processed_data.append(row)

    return processed_data


def find_xmas(data: List[List[str]], R: int, C: int) -> int:
    rows: int = len(data)
    cols: int = len(data[0])
    words: List[str] = ['X'] * 8
    ans: int = 0

    for d in range(1, 4):
        if 0 <= R + d < rows and 0 <= C < cols:
            words[0] += data[R + d][C]
        if 0 <= R + d < rows and 0 <= C + d < cols:
            words[1] += data[R + d][C + d]
        if 0 <= R < rows and 0 <= C + d < cols:
            words[2] += data[R][C + d]
        if 0 <= R - d < rows and 0 <= C + d < cols:
            words[3] += data[R - d][C + d]
        if 0 <= R - d < rows and 0 <= C < cols:
            words[4] += data[R - d][C]
        if 0 <= R - d < rows and 0 <= C - d < cols:
            words[5] += data[R - d][C - d]
        if 0 <= R < rows and 0 <= C - d < cols:
            words[6] += data[R][C - d]
        if 0 <= R + d < rows and 0 <= C - d < cols:
            words[7] += data[R + d][C - d]

    for word in words:
        if word == 'XMAS':
            ans += 1

    return ans


def solve_part_one(data: List[str]) -> Any:
    """Solves part one of the challenge.

    Args:
        data (List[str]): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """
    rows: int = len(data)
    cols: int = len(data[0])
    ans: int = 0
    for R in range(rows):
        for C in range(cols):
            if data[R][C] == 'X':
                ans += find_xmas(data, R, C)

    return ans


def find_x_shaped_mas(data: List[List[str]], R: int, C: int) -> int:
    rows: int = len(data)
    cols: int = len(data[0])

    dr1, dr2 = R - 1, R + 2
    dc1, dc2 = C - 1, C + 2
    if 0 <= dr1 < rows and dr2 <= rows and 0 <= dc1 < cols and dc2 <= cols:
        pattern = [row[dc1:dc2] for row in data[dr1:dr2]]

        top_right = pattern[0][2]
        top_left = pattern[0][0]
        bottom_left = pattern[2][0]
        bottom_right = pattern[2][2]

        if top_right in ['M', 'S'] and \
                top_left in ['M', 'S'] and \
                bottom_left in ['M', 'S'] and \
                bottom_right in ['M', 'S']:
            if top_right == top_left and \
                    top_right != bottom_left and \
                    top_right != bottom_right and \
                    bottom_left == bottom_right:
                return 1
            if top_right == bottom_right and \
                    top_right != top_left and \
                    bottom_right != bottom_left and \
                    top_left == bottom_left:
                return 1

    return 0


def solve_part_two(data: List[str]) -> Any:
    """Solves part two of the challenge.

    Args:
        data (List[str]): The input data for the challenge.

    Returns:
        Any: The result of the solution for part two.
    """
    rows: int = len(data)
    cols: int = len(data[0])
    ans: int = 0
    for R in range(rows):
        for C in range(cols):
            if data[R][C] == 'A':
                ans += find_x_shaped_mas(data, R, C)

    return ans


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
