"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
Input can be read from local files (##.in or ##.test) or fetched via AOCD.
When fetching from AOCD, data is automatically saved to local files.
"""

import os
from typing import List, Any
from aocd import get_data


def get_input(day: int, year: int, test: bool = False) -> List[str]:
    """Reads the input from either a local file or fetches it via AOCD.

    When fetching from AOCD, automatically saves the data to a local file.

    Args:
        day (int): The day of the challenge.
        year (int): The year of the challenge.
        test (bool, optional): Whether to use test input file. Defaults to
            False.

    Returns:
        List[str]: A list of strings representing the input data.

    Raises:
        FileNotFoundError: If test file is requested but doesn't exist.
    """
    day_str: str = f"{day:02d}"

    if test:
        file_path = f"{day_str}.test"
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip().splitlines()
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Test file {file_path} not found"
            ) from e

    # Try local file first
    file_path = f"{day_str}.in"
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip().splitlines()
    except FileNotFoundError:
        # Fetch from AOCD and save locally
        data: str = get_data(day=day, year=year)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(data)
        return data.splitlines()


def solve_part_one(data: List[str]) -> Any:
    """Solves part one of the challenge.

    Args:
        data (List[str]): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """
    # TODO: Implement the solution for part one
    return None


def solve_part_two(data: List[str]) -> Any:
    """Solves part two of the challenge.

    Args:
        data (List[str]): The input data for the challenge.

    Returns:
        Any: The result of the solution for part two.
    """
    # TODO: Implement the solution for part two
    return None


if __name__ == "__main__":
    # Configure these values for each challenge
    DAY: int = 1
    YEAR: int = 2024
    USE_LOCAL: bool = False

    input_data = get_input(DAY, YEAR, USE_LOCAL)

    result_part_one = solve_part_one(input_data)
    if result_part_one is not None:
        print(f"Part One: {result_part_one}")
    result_part_two = solve_part_two(input_data)
    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")
