"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

import copy
import os
import sys
from collections import deque
from typing import Any, List, Tuple, Deque, Optional

from pathlib import Path

# Add the parent directory of 'utils' to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import utils  # noqa: E402


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


def count_reachable_plots(
    data: Any,
    steps: int = 64
) -> int:
    """Solves part one of the challenge.
    """
    if data is None:
        return None

    grid: List[List[str]] = copy.deepcopy(data)
    new_grid: List[List[str]] = copy.deepcopy(data)

    rows: int = len(grid)
    cols: int = len(grid[0])

    directions: List[Tuple[int, int]] = [
        (0, 1), (1, 0), (0, -1), (-1, 0)
    ]  # R,D,L,U

    for i in range(64):
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                if val == 'O' or (i == 0 and val == 'S'):
                    new_grid[r][c] = '.'
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if (
                            0 <= nr < rows and
                            0 <= nc < cols and
                            grid[nr][nc] != '#'
                        ):
                            new_grid[nr][nc] = 'O'

        grid = copy.deepcopy(new_grid)

    count: int = sum(row.count('O') for row in grid)
    return count


def count_reachable_plots_bfs(
    data: List[List[str]],
    steps: int = 64
) -> int:
    """Count reachable plots using Breadth-First Search.
    """
    # Find starting position
    rows: int = len(data)
    cols: int = len(data[0])
    start_pos: Tuple[int, int] = next(
        (r, c) for r, row in enumerate(data)
        for c, ch in enumerate(row) if ch == 'S'
    )

    ans: set = set()
    seen: set = {start_pos}
    q: Deque[Tuple[int, int, int]] = deque(
        [(start_pos[0], start_pos[1], steps)]
    )

    while q:
        r, c, s = q.popleft()

        if s % 2 == 0:
            ans.add((r, c))
        if s == 0:
            continue

        for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
            if (nr < 0 or nr >= rows or nc < 0 or nc >= cols or
                    data[nr][nc] == '#' or (nr, nc) in seen):
                continue
            seen.add((nr, nc))
            q.append((nr, nc, s - 1))

    return len(ans)


def count_reachable_plots_infinite(
    data: List[List[str]],
    steps: int,
    start_pos: Optional[Tuple[int, int]] = None
) -> int:
    """Count reachable plots in infinite grid.
    """
    size: int = len(data)
    if not start_pos:
        start_pos = next((r, c) for r, row in enumerate(data)
                         for c, ch in enumerate(row) if ch == 'S')

    plots: set = set()
    seen: set = set()
    q: deque = deque([(start_pos[0], start_pos[1], steps)])

    while q:
        r, c, s = q.popleft()

        pos_key: Tuple[int, int, int] = (r, c, s)
        if pos_key in seen:
            continue
        seen.add(pos_key)

        if s % 2 == 0:
            plots.add((r, c))
        if s == 0:
            continue

        for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
            grid_r, grid_c = nr % size, nc % size
            if data[grid_r][grid_c] != '#':
                q.append((nr, nc, s - 1))

    return len(plots)


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        return None

    return count_reachable_plots(data)


def solve_part_two(data: List[List[str]]) -> int:
    """Solves part two of the challenge.
    """
    size: int = len(data)
    steps: int = 26501365

    # The pattern repeats every size steps after the initial offset
    offset: int = steps % size

    # Calculate three points to fit quadratic formula
    y: List[int] = []
    for n in range(3):
        steps_n: int = offset + n * size
        y.append(count_reachable_plots_infinite(data, steps_n))

    # Calculate coefficients for quadratic formula: ax² + bx + c
    n: int = steps // size
    a: int = (y[2] + y[0] - 2 * y[1]) // 2
    b: int = y[1] - y[0] - a
    c: int = y[0]

    return a * n * n + b * n + c


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
