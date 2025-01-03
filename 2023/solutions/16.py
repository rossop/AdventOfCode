"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

import os
import sys
from typing import Any, Deque, Dict, List, Optional, Set, Tuple

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


def calc(data: Any, start: Tuple[int, int], dir: int) -> int:
    """Calculates the number of energized tiles from a given starting position and direction.

    Args:
        data: The grid data
        start: Starting position tuple (row, col)
        dir: Initial direction (0=right, 1=down, 2=left, 3=up)

    Returns:
        int: Number of energized tiles
    """
    q: Deque = Deque([
        (start[0], start[1], dir)  # (row, col, direction)
    ])

    energized: Set[Tuple[int, int]] = set()
    visited: Set[Tuple[int, int, int]] = set()

    rows: int = len(data)
    cols: int = len(data[0])
    directions: List[Tuple[int, int]] = [
        (0, 1), (1, 0), (0, -1), (-1, 0)]  # R,D,L,U

    while q:
        r, c, dir = q.popleft()

        # Add current cell to energized set
        energized.add((r, c))

        if (r, c, dir) in visited:
            continue
        visited.add((r, c, dir))

        dr, dc = directions[dir]
        nr, nc = r + dr, c + dc

        if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
            continue

        if data[nr][nc] == '.':
            q.append((nr, nc, dir))
        elif data[nr][nc] == '\\':
            new_dir = dir ^ 1  # Smart way to flip between 0<->1 and 2<->3
            q.append((nr, nc, new_dir))
        elif data[nr][nc] == '/':
            new_dir = 3 - dir  # Smart way to flip between 0<->3 and 1<->2
            q.append((nr, nc, new_dir))
        elif data[nr][nc] == '|':
            if dir in (0, 2):  # Horizontal beam
                q.append((nr, nc, 1))  # Split down
                q.append((nr, nc, 3))  # Split up
            else:  # Vertical beam
                q.append((nr, nc, dir))
        elif data[nr][nc] == '-':
            if dir in (1, 3):  # Vertical beam
                q.append((nr, nc, 0))  # Split right
                q.append((nr, nc, 2))  # Split left
            else:  # Horizontal beam
                q.append((nr, nc, dir))

    return len(energized) - 1


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        return None

    return calc(data, (0, -1), 0)


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.
    """
    if data is None:
        return None
    max_val: int = 0

    # Fixed the calc() calls and grid reference
    for r in range(len(data)):
        max_val = max(max_val, calc(data, (r, -1), 0))
        max_val = max(max_val, calc(data, (r, len(data[0])), 2))

    for c in range(len(data[0])):
        max_val = max(max_val, calc(data, (-1, c), 1))
        max_val = max(max_val, calc(data, (len(data), c), 3))

    return max_val


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
