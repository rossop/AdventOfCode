"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

from collections import deque
import os
import sys
from typing import Any, Deque, Dict, List, Set, Tuple

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
            int(c) for c in line
        ] for line in raw_data.splitlines()
    ]


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        return None

    rows: int = len(data)
    cols: int = len(data[0])
    end: Tuple[int, int] = (rows-1, cols-1)

    # Queue entries: (heat_loss, row, col, dir_index, steps, path)
    q: List = [(0, 0, 0, -1, 0, [(0, 0)])]

    # Track (row, col, dir_index, steps)
    seen: Set[Tuple[int, int, int, int]] = set()

    directions: List[Tuple[int, int]] = [
        (0, 1), (1, 0), (0, -1), (-1, 0)]  # R,D,L,U
    min_heat: int = float('inf')
    best_path: List = []

    while q:
        q.sort(key=lambda x: x[0])
        heat, r, c, prev_dir, straight, path = q.pop(0)

        if (r, c) == end:
            if heat < min_heat:
                min_heat = heat
                best_path = path
            continue

        state: Tuple[int, int, int, int] = (r, c, prev_dir, straight)
        if state in seen:
            continue
        seen.add(state)

        for i, (dr, dc) in enumerate(directions):
            # Can't reverse direction
            if prev_dir != -1 and abs(prev_dir - i) == 2:
                continue

            # Can't go more than 3 straight
            if i == prev_dir and straight == 3:
                continue

            nr: int = r + dr
            nc: int = c + dc

            if 0 <= nr < rows and 0 <= nc < cols:
                new_heat: int = heat + data[nr][nc]
                new_straight: int = straight + 1 if i == prev_dir else 1
                new_path: List = path + [(nr, nc)]
                q.append((new_heat, nr, nc, i, new_straight, new_path))

    # Print the path for debugging
    if best_path:
        grid: List[List[str]] = [
            ['.' for _ in range(cols)] for _ in range(rows)]
        for i in range(len(best_path)-1):
            curr_r, curr_c = best_path[i]
            next_r, next_c = best_path[i+1]
            if next_c > curr_c:
                grid[curr_r][curr_c] = '>'
            elif next_c < curr_c:
                grid[curr_r][curr_c] = '<'
            elif next_r > curr_r:
                grid[curr_r][curr_c] = 'v'
            else:
                grid[curr_r][curr_c] = '^'
        grid[end[0]][end[1]] = 'E'

        # print("\nPath:")
        # for row in grid:
        #     print(''.join(row))

    return min_heat


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
