"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

import os
from pprint import pprint
import sys
from typing import Any, Callable, Dict, List, Set, Tuple

from pathlib import Path

# Add the parent directory of 'utils' to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import utils

input_directory: str = os.path.join(
    os.path.dirname(
        os.path.abspath(
            os.path.dirname(__file__)
        )
    ), 'in'
)


def process(raw_data: str) -> Any:
    """Processes the input data.
    """
    info: List[str] = raw_data.split('\n\n')
    processed_data: Dict = {}
    processed_data['inputs'] = {}
    processed_data['operations'] = []

    processed_data['inputs'].update(
            map(
                lambda line: (
                    line.split(': ')[0],
                    int(line.split(': ')[1])
                ),
                info[0].splitlines()
            )
    )


    processed_data['operations'].extend(
            map(
                lambda line: (
                    line.split(' ')[0],
                    line.split(' ')[1],
                    line.split(' ')[2],
                    line.split(' ')[4],
                ),
                info[1].splitlines()
            )
    )
    # pprint(processed_data)
    return processed_data


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        error_str: str = "Invalid input data"
        raise ValueError(error_str)

    inputs: Dict[str, int] = data['inputs']
    operations: List[Tuple[str, str, str, str]] = data['operations']

    operation_map: Dict[str, Callable[[int, int], int]] = {
        "AND": lambda x, y: x and y,  # Logical AND
        "OR": lambda x, y: x or y,   # Logical OR
        "XOR": lambda x, y: x ^ y,   # Logical XOR
    }

    while True:
        filtered_tuples = list(
            filter(
                lambda t: (
                    t[3] not in inputs and  # Already processed
                    t[0] in inputs and      # First input present
                    t[2] in inputs          # Second input present
                ),
                operations
            ),
        )
        if len(filtered_tuples) < 1:
            break

        for ft in filtered_tuples:
            bin1: int = inputs[ft[0]]
            op: str = ft[1]
            bin2: int = inputs[ft[2]]
            inputs[ft[3]] = operation_map[op](bin1, bin2)

    binary_value: str = "".join(
        str(inputs[key]) for key in sorted(
            inputs,
            reverse= True
        ) if key.startswith('z')
    )
    print('Binary Value: ', binary_value)
    integer_value: int = int(binary_value, 2)

    return integer_value


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.
    """
    # TODO: Implement the solution for part two
    return None


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'

    file_path: str = os.path.join(input_directory, infile)
    unprocessed_data = utils.read_input(file_path)
    input_data = process(unprocessed_data['data'])

    result_part_one = solve_part_one(input_data)
    if result_part_one is not None:
        print(f"Part One: {result_part_one}")
    result_part_two = solve_part_two(input_data)
    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")

