"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

from collections import deque
import copy
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
    return [list(line) for line in raw_data.splitlines()]


def find_start_end(
    grid: List[List[str]]
) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """Find start and end point in the 2D maze
    """
    rows: int = len(grid)
    cols: int = len(grid[0])

    if rows < 1 and cols < 1:
        return None

    start: Optional[Tuple[int, int]] = None
    end: Optional[Tuple[int, int]] = None

    point_counter: int = 0  # counts relevant points found

    # Find start and end
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start = (r, c)
                point_counter += 1
                if point_counter == 2:
                    break
            elif grid[r][c] == 'E':
                end = (r, c)
                point_counter += 1
                if point_counter == 2:
                    break

    if start is None or end is None:
        return None
    return start, end


def bfs_with_constraints(
    grid: List[List[str]],
    min_save_time: int = 100
) -> List[Tuple]:
    """Perform BFS on a grid with constraints to find valid cheating paths.
    """
    rows: int = len(grid)
    cols: int = len(grid[0])

    directions: List[Tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    start, end = find_start_end(grid)
    print(start, end)
    for line in grid:
        print("".join(line))

    if not start or not end:
        raise ValueError("Grid must contain both 'S' (start) and 'E' (end).")

    # Queue format: (row, col, time, cheat_moves_used, cheat_start)
    queue: Deque = deque([(start[0], start[1], 0, 0, None)])
    # visited format: (row, col, cheat_moves_left)
    visited: Set = set()
    cheats: List[Tuple] = []

    while queue:
        x, y, time, cheat_moves, cheat_start = queue.popleft()
        state = (x, y, cheat_moves)

        if state in visited:
            continue
        visited.add(state)

        # If we reach the end and were cheating, record the cheat
        if (x, y) == end and cheat_start:
            normal_dist = abs(cheat_start[0] - x) + abs(cheat_start[1] - y)
            saved_time = normal_dist - 2
            if saved_time >= min_save_time:
                cheats.append((cheat_start, (x, y), saved_time))
            continue

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if not (0 <= nx < rows and 0 <= ny < cols):
                continue

            cell = grid[nx][ny]

            # Normal move (no walls)
            if cell in '.SE':
                queue.append((nx, ny, time + 1, cheat_moves, cheat_start))

            # Start cheating
            elif cell == '#' and cheat_moves == 0 and not cheat_start:
                queue.append((nx, ny, time + 1, 1, (x, y)))

            # Continue cheating
            elif cell == '#' and cheat_moves == 1:
                queue.append((nx, ny, time + 1, 2, cheat_start))

            # End cheating
            elif cell in '.SE' and cheat_moves == 2:
                queue.append((nx, ny, time + 1, 0, None))

    return cheats


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        return None

    grid: List[List[str]] = copy.deepcopy(data)
    valid_cheats: List[Tuple] = bfs_with_constraints(grid, min_save_time=100)

    return len(valid_cheats)


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
