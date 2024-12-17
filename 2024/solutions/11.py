"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
import sys
from typing import Any, Dict, List


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
    return list(
        map(
            int,
            raw_data.split()
        )
    )


def process_stone(stone: int) -> List[int]:
    """Process a single stone"""
    if stone == 0:
        yield 1
    stone_str: str = str(stone)
    if len(str(stone)) % 2 == 0:  # Even number of digits
        mid: int = len(str(stone)) // 2
        yield int(stone_str[:mid])
        yield int(stone_str[mid:])
    yield stone * 2024


def blink(stones):
    """A single step in the blinking process"""
    return [item for sublist in map(process_stone, stones) for item in sublist]


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.

    Args:
        data (Any): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """
    current_stone = data.copy()
    for _ in range(25):
        current_stone = blink(current_stone)
    return len(current_stone)


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'

    unprocessed_data = read_input(infile)
    data = process(unprocessed_data['data'])

    DP = {}
    def solve(x, t):
        """If we put [x] through [t] steps, how long is the resulting list?"""
        num_str = str(x)
        if (x,t) in DP:
            return DP[(x, t)]
        if t == 0:
            ret = 1
        elif x == 0:
            ret = solve(1, t-1)
        elif len(num_str) % 2 == 0 and len(num_str) > 1:
            num_str = str(x)
            mid: int = len(num_str) // 2
            num_left = int(num_str[:mid])
            num_right = int(num_str[mid:])
            ret = solve(num_left, t-1) + solve(num_right, t-1)
        else:
            ret = solve(x * 2024, t - 1)
        DP[(x,t)] = ret
        return ret

    def solve_all(t):
        return sum(solve(x,t) for x in data)

    result_part_one: int = solve_all(25)
    result_part_two: int = solve_all(75)

    if result_part_one is not None:
        print(f"Part One: {result_part_one}")
    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")

