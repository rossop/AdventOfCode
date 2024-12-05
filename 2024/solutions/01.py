"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
from typing import List, Any, Dict
from collections import Counter


def read_input(file_name: str) -> Any:
    """Reads the input from a specified file.

    Args:
        file_name (str): The name of the input file.

    Returns:
        Any: Processed data.
    """
    file_path = os.path.join('2024/in', file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        data: List[str] = file.read().strip().splitlines()
        split_data: List[List[int]] = [
            list(map(int, line.split())) for line in data]
        column_a: List[int] = [line[0] for line in split_data]
        column_b: List[int] = [line[1] for line in split_data]
        return sorted(column_a), sorted(column_b)


def solve_part_one(data: List[str]) -> Any:
    """Solves part one of the challenge.

    Args:
        data (List[str]): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """
    sorted_column_a, sorted_column_b = data

    return sum(
        map(
            lambda x: abs(x[0] - x[1]),
            zip(sorted_column_a, sorted_column_b)
        )
    )


def solve_part_two(data: List[str]) -> Any:
    """Solves part two of the challenge.

    Args:
        data (List[str]): The input data for the challenge.

    Returns:
        Any: The result of the solution for part two.
    """
    column_a, column_b = data

    freq_b: Dict[int, int] = Counter(column_b)
    ANS: int = 0

    for num in column_a:
        if num in freq_b:
            ANS += freq_b[num] * num

    return ANS


if __name__ == "__main__":
    input_data = read_input('1.in')
    result_part_one = solve_part_one(input_data)
    print(f"Part One: {result_part_one}")
    result_part_two = solve_part_two(input_data)
    print(f"Part Two: {result_part_two}")
