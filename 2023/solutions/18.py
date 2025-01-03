"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

import os
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
        (
            parts[0],
            int(parts[1]),
            parts[2].strip('()')
        ) for comm in raw_data.splitlines()
        if (parts := comm.split(" "))
        # for parts in [comm.split(" ")]
    ]


def dynamic_range(start: int, d: int, num: int) -> List[int]:
    """" Generate the range
    """
    if d == 0:
        return []
    return [start + delta for delta in range(0, d * num, d) if d != 0]


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        return None

    # Track vertices of the polygon (not every single edge point)
    points: List[Tuple[int, int]] = [(0, 0)]

    # Track total boundary points
    boundary_length: int = 0

    directions: Dict[str, Tuple[int, int]] = {
        'R': (0, 1),
        'D': (1, 0),
        'L': (0, -1),
        'U': (-1, 0)
    }

    # Build vertices and count boundary points
    for dirr, steps, _ in data:
        dr, dc = directions[dirr]
        boundary_length += steps
        r, c = points[-1]
        # Only store the endpoint of each instruction
        points.append((r + dr * steps, c + dc * steps))

    # Shoelace formula to calculate area
    area = abs(sum(
        points[i][0] * (points[i-1][1] - points[(i+1) % len(points)][1])
        for i in range(len(points))
    )) // 2

    # Pick's theorem: A = i + b/2 - 1
    # Rearranging to solve for i (interior points)
    interior_points = area - boundary_length//2 + 1

    # Total points = interior + boundary
    return interior_points + boundary_length


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.
    """
    if data is None:
        return None

    # Track vertices of the polygon (not every single edge point)
    points: List[Tuple[int, int]] = [(0, 0)]

    # Track total boundary points
    boundary_length: int = 0

    # Map hex digit to direction
    directions: Dict[str, Tuple[int, int]] = {
        '0': (0, 1),   # R
        '1': (1, 0),   # D
        '2': (0, -1),  # L
        '3': (-1, 0)   # U
    }

    # Build vertices and count boundary points
    for _, _, hex_string in data:
        # Extract distance and direction from hex
        steps = int(hex_string[1:6], 16)  # First 5 digits are distance
        dir_code = hex_string[6]          # Last digit is direction

        dr, dc = directions[dir_code]
        boundary_length += steps
        r, c = points[-1]
        # Only store the endpoint of each instruction
        points.append((r + dr * steps, c + dc * steps))

    # Shoelace formula to calculate area
    area = abs(sum(
        points[i][0] * (points[i-1][1] - points[(i+1) % len(points)][1])
        for i in range(len(points))
    )) // 2

    interior_points = area - boundary_length//2 + 1
    return interior_points + boundary_length


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
