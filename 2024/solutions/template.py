"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
from typing import List, Any


def read_input(file_name: str) -> List[str]:
    """Reads the input from a specified file.

    Args:
        file_name (str): The name of the input file.

    Returns:
        List[str]: A list of strings representing the lines in the file.
    """
    file_path = os.path.join('2024/in', file_name)
    with open(file_path, 'r') as file:
        return file.read().strip().splitlines()


def solve_part_one(data: List[str]) -> Any:
    """Solves part one of the challenge.

    Args:
        data (List[str]): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """
    # TODO: Implement the solution for part one
    pass


def solve_part_two(data: List[str]) -> Any:
    """Solves part two of the challenge.

    Args:
        data (List[str]): The input data for the challenge.

    Returns:
        Any: The result of the solution for part two.
    """
    # TODO: Implement the solution for part two
    pass


if __name__ == "__main__":
    input_data = read_input('input.txt')
    result_part_one = solve_part_one(input_data)
    print(f"Part One: {result_part_one}")
    result_part_two = solve_part_two(input_data)
    print(f"Part Two: {result_part_two}")
