"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

import os
import re
import sys
from typing import Any, Dict, List, Set, Tuple

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
    return [
        [
            c for c in line
        ] for line in raw_data.splitlines()
    ]


def split_keep_delimiter(s: str, delimiter: str):
    """Split string and keep delimiter in final list.
    """
    escaped_delimiter = re.escape(delimiter)
    return re.split(f"({escaped_delimiter})", s)


def simulate_board(grid: List[List[str]]) -> List[List[str]]:
    """Slide board, where O represent movable rocks and # are fixed rocks.
    """
    rows: int = len(grid)
    cols: int = len(grid[0])

    for col in range(cols):
        column = [
            grid[row][col] for row in range(rows)
        ]
        column_str: str = "".join(column)
        parts = split_keep_delimiter(column_str, "#")
        s: List[str] = list(
                map(
                    lambda x: "".join(
                        sorted(
                            [
                                c for c in x
                            ],
                            reverse=True
                        )
                    ),
                    parts
                )
        )
        sorted_column: str = "".join(s)
        for row in range(rows):
            grid[row][col] = sorted_column[row]

    return grid


def simulate(grid: List[List[str]]) -> List[List[str]]:
    """ Slide Board
    """
    grid = list(
        map(
            "".join,
            zip(*grid)
            )
    )
    grid = [
        "#".join(  # Join groups with "#"
            [
                "".join(  # Join characters within each group
                    sorted(  # Sort the characters in descending order
                        list(group),
                        reverse=True
                    )
                ) for group in row.split("#")  # Split the row by "#"
            ]
        ) for row in grid  # Iterate through each row in the grid
    ]
    grid = list(
        map(
            "".join,
            zip(*grid)
            )
    )
    return grid


def calculate_load(grid: List[List[str]]) -> int:
    """Calculate teh load on the north beam.
    """
    rows: int = len(grid)
    load: int = 0

    for r, row in enumerate(grid):
        rocks_count: int = sum(
            [
                1 if val == 'O' else 0 for val in row
            ]
        )
        load += (rows - r) * rocks_count

    return load


def calc_load(grid: List[List[str]]) -> int:
    """Calculate teh load on the north beam for roated grid.
    """
    return sum(
        row.count('O') * (len(grid) - r) for r, row in enumerate(grid)
    )


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        error_msg: str = "Data not properly loaded"
        raise ValueError(error_msg)

    tilted_grid: List[List[str]] = simulate_board(data)

    return calc_load(tilted_grid)


def solve_part_two(input_data: Any) -> Any:
    """Solves part two of the challenge."""

    # Validate input
    if input_data is None:
        raise ValueError("Input data is not properly loaded.")

    # Parse the input into an initial immutable grid
    initial_grid: Tuple[str, ...] = tuple("".join(line) for line in input_data)

    def transform_grid(grid: Tuple[str, ...]) -> Tuple[str, ...]:
        """
        Performs one full transformation cycle on the grid:
        1. Transpose the grid.
        2. Sort and process rows based on `#` delimiters.
        3. Reverse each row.
        """
        for _ in range(4):
            # Rotate grid 90 degrees clockwise
            grid = tuple(map("".join, zip(*grid)))

            # Sort each row's groups of rocks
            grid = tuple(
                "#".join(
                    "".join(sorted(group, reverse=True)) for group in row.split("#")
                )
                for row in grid
            )

            # Reverse each row
            grid = tuple(row[::-1] for row in grid)

        return grid

    # Initialize variables for cycle detection
    seen_grids: Set[Tuple[str, ...]] = set()
    seen_grids.add(initial_grid)

    grid_history: List[Tuple[str, ...]] = [initial_grid]
    current_grid = initial_grid

    # Detect cycles in grid transformations
    iteration = 0
    while True:
        iteration += 1
        current_grid = transform_grid(current_grid)
        if current_grid in seen_grids:
            # Cycle detected
            break

        seen_grids.add(current_grid)
        grid_history.append(current_grid)

    # Determine cycle properties
    start_of_cycle = grid_history.index(current_grid)
    cycle_length = iteration - start_of_cycle

    # Calculate the target iteration within the cycle
    target_iteration = (
        1_000_000_000 - start_of_cycle
    ) % cycle_length + start_of_cycle
    target_grid = grid_history[target_iteration]

    # Convert target grid for calc_load (if required by its implementation)
    formatted_target_grid: List[List[str]] = [
        [
            c for c in line
        ] for line in target_grid
    ]

    # Calculate and return the load for the target grid
    return calc_load(formatted_target_grid)


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
