"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

from collections import defaultdict
import os
from pprint import pprint
import sys
from typing import Any, Dict, List, Set, Tuple

from pathlib import Path
from itertools import product
import copy


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
            char for char in line
        ] for line in raw_data.splitlines()
    ]


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        msg: str = 'Invalid `data` entry'
        raise ValueError(msg)

    rows: int = len(data)
    cols: int = len(data[0])

    empty_rows: List = []
    for r, row in enumerate(data):
        if all([val == '.' for val in row]):
            empty_rows.append(r)

    empty_cols = []
    for c in range(cols):  # Iterate over columns
        if all(row[c] == '.' for row in data):  # Check if all rows have '.' in column c
            empty_cols.append(c)  # Add column index to the list

    def increase_columns(
        row: List[str],
        empty_cols: List[int]
    ) -> List[str]:
        new_row: List[str] = []
        for r, val in enumerate(row):
            new_row.append(val)
            if r in empty_cols:
                new_row.append(val)
        return new_row

    new_grid: List[List[str]] = []
    for r, row in enumerate(data):
        # Expand Cols
        expanded_row = increase_columns(row, empty_cols)
        new_grid.append(expanded_row)
        if r in empty_rows:
            new_grid.append(expanded_row)


    num: int = 1
    locations: Dict[int,Tuple[int, int]] = dict()
    for r, row in enumerate(new_grid):
        for c, val in enumerate(row):
            if val == '#':
                new_grid[r][c] = str(num)
                locations[num] = (r, c)
                num += 1


    ans: int = 0
    calculated: Set[Tuple[int, ...]] = set()
    for (key1, coord1), (key2, coord2) in product(locations.items(), repeat=2):
        pair: Tuple[int, ...] = tuple(sorted([key1, key2]))
        if pair in calculated:
            continue

        calculated.add(pair)
        dist: int = calc_dist(coord1, coord2)

        ans += dist

    return ans


def calc_dist(
    coord1: Tuple[int, int],
    coord2: Tuple[int, int],
) -> int:
    """ Calcualte distance between two galaxies
    """
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])


def calc_expanded_dist(
    coord1: Tuple[int, int],
    coord2: Tuple[int, int],
    empty_rows: List[int],
    empty_cols: List[int],
    magnification: int = 2
) -> int:
    """Calculate galaxy distance accounting for magnification
    """
    x1, y1 = coord1
    x2, y2 = coord2
    relevant_expanding_cols: int = len(
            [
                num for num in empty_cols if (
                    x1 < num < x2 or
                    x2 < num < x2
                )
            ]
    )
    relevant_expanding_rows: int = len(
            [
                num for num in empty_rows if (
                    y1 < num < y2 or
                    y2 < num < y2
                )
            ]
    )
    adjusted_x2: int = x2 + (magnification - 0) * (relevant_expanding_cols - 1)
    adjusted_y2: int = y2 + (magnification - 0) * (relevant_expanding_rows - 1)

    return abs(adjusted_x2- x1) + abs(adjusted_y2 - y1)


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.
    """
    if data is None:
        msg: str = 'Invalid `data` entry'
        raise ValueError(msg)

    rows: int = len(data)
    cols: int = len(data[0])

    new_grid = copy.deepcopy(data)

    empty_rows: List = []
    for r, row in enumerate(new_grid):
        if all([val == '.' for val in row]):
            empty_rows.append(r)

    empty_cols = []
    for c in range(cols):  # Iterate over columns
        if all(row[c] == '.' for row in new_grid):  # Check if all rows have '.' in column c
            empty_cols.append(c)  # Add column index to the list

    num: int = 1
    locations: Dict[int,Tuple[int, int]] = dict()
    points: List[Tuple[int, int]] = []
    for r, row in enumerate(new_grid):
        for c, val in enumerate(row):
            if val == '#':
                new_grid[r][c] = str(num)
                locations[num] = (r, c)
                points.append((r, c))
                num += 1

    ans: int = 0
    scale: int = 1000000
    for i, (r1, c1) in enumerate(points):
        for (r2, c2) in points[:i]:
            for r in range(min(r1, r2), max(r1, r2)):
                ans += scale if r in empty_rows else 1
            for c in range(min(c1, c2), max(c1, c2)):
                ans += scale if c in empty_cols else 1


    return ans


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
