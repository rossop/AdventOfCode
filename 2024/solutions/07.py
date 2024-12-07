"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
import sys
import copy
from typing import List, Any, Dict, Union


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
    processed_data: List[List[Union[List[int], int]]] = []
    for line in raw_data.splitlines():
        separated_line = line.split(": ")
        num = int(separated_line[0])
        vals = list(
            map(
                int,
                separated_line[1].split()
            )
        )
        processed_data.append(
            [
                num,
                vals
            ]
        )

    return processed_data


def is_valid(
        target: int,
        list_of_nums: List[int],
        part_2: bool = False) -> bool:
    """Find Valid sum"""
    if len(list_of_nums) == 1:
        return list_of_nums[0] == target
    n0: int = list_of_nums.pop(0)
    n1: int = list_of_nums.pop(0)

    if is_valid(target, [n0 + n1] + list_of_nums, part_2):
        return True
    if is_valid(target, [n0 * n1] + list_of_nums, part_2):
        return True

    if part_2:
        concat_num: int = int(
            str(n0) + str(n1)
        )
        # print(n0, n1, concat_num)
        if is_valid(target, [concat_num] + list_of_nums, part_2):
            return True

    return False


def solve_part_one(data: List[str]) -> Any:
    """Solves part one of the challenge.

    Args:
        data (List[str]): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """
    ans: int = 0
    for target, list_of_nums in data:
        if is_valid(target, list_of_nums):
            ans += target
    return ans


def solve_part_two(data: List[str]) -> Any:
    """Solves part two of the challenge.

    Args:
        data (List[str]): The input data for the challenge.

    Returns:
        Any: The result of the solution for part two.
    """
    ans: int = 0
    for target, list_of_nums in data:
        if is_valid(target, list_of_nums, part_2=True):
            ans += target
    return ans


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'

    raw_data = read_input(infile)

    input_data = process(raw_data['data'])
    data_part_one = copy.deepcopy(input_data)
    data_part_two = copy.deepcopy(input_data)

    result_part_one = solve_part_one(data_part_one)
    if result_part_one is not None:
        print(f"Part One: {result_part_one}")

    result_part_two = solve_part_two(data_part_two)
    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")
