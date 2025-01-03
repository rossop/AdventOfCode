"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

from collections import deque
import os
import sys
from typing import Any, Deque, Dict, List, Optional, Set, Tuple

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


def find_start(grid: List[List[str]]) -> Optional[Tuple[int, int]]:
    """Find starting point in grid"""
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val == 'S':
                return (i, j)


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        return None

    # find start
    start: Optional[Tuple[int, int]] = find_start(data)
    if start is None:
        error_message: str = "Grid has no starting value."
        raise ValueError(error_message)

    # simulate movement
    rows: int = len(data)
    cols: int = len(data[0])
    directions: Dict[str, List[Tuple[int, int]]] = {
        "|" : [(1, 0), (-1,0)],
        "-" : [(0, 1), (0,-1)],
        "L" : [(0, 1), (-1,0)],
        "J" : [(0, -1), (-1,0)],
        "7" : [(0, -1), (1,0)],
        "F" : [(0, 1), (1,0)],
        "S" : [(1, 0), (-1, 0), (0, 1), (0, -1)],
        "." : []
    }

    visited: Set[Tuple[int, int]] = set()
    q: Deque[Tuple[int, int, int]] = deque([(start[0], start[1], 0)])
    visited.add(start)
    furthest: Tuple[int, int] = start
    max_distance: int = 0

    while q:
        r, c, dist = q.popleft()

        if dist > max_distance:
            max_distance = dist
            furthest = (r, c)

        curr_connection: str = data[r][c]

        for dr, dc in directions[curr_connection]:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):  # Ensure within bounds
                continue

            if data[nr][nc] == '.':  # Ignore empty spaces
                continue

            new_connection: str = data[nr][nc]

            # Check if this pipe connects back to the current pipe
            if (-dr, -dc) in directions[new_connection]:  # Reverse direction
                if (nr, nc) not in visited:  # Avoid revisiting
                    visited.add((nr, nc))
                    q.append((nr, nc, dist + 1))


    return max_distance, visited


def solve_part_two_archive(grid, loop_set):
    """Solves part two of the challenge.

    ISSUE: misses some of the outside "trapped" cells.
    """
    if grid is None:
        raise ValueError("Grid not valid.")

    rows, cols = len(grid), len(grid[0])

    def in_bounds(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def flood_fill_outside():
        visited = [[False for _ in range(cols)] for _ in range(rows)]
        stack = []

        # Start from all edges of the grid
        for r in range(rows):
            for c in (0, cols - 1):  # Left and right edges
                if (r, c) not in loop_set:
                    stack.append((r, c))
        for c in range(cols):
            for r in (0, rows - 1):  # Top and bottom edges
                if (r, c) not in loop_set:
                    stack.append((r, c))

        # Perform flood fill
        while stack:
            x, y = stack.pop()
            if in_bounds(x, y) and not visited[x][y] and (x, y) not in loop_set:
                visited[x][y] = True
                stack.extend([(x + dx, y + dy) for dx, dy in directions])

        return visited

    # Directions for 4-connected neighbors
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Flood fill from the outside
    outside_visited = flood_fill_outside()

    # Debug: visualize the flood fill result

    # Create a visualization grid
    visualization = [["." for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if (r, c) in loop_set:
                visualization[r][c] = "#"  # Loop cells
            elif outside_visited[r][c]:
                visualization[r][c] = "O"  # Outside cells
            else:
                visualization[r][c] = "I"  # Inside cells

    # Print the visualization
    print("Visualization (O: Outside, #: Loop, I: Inside):")
    for row in visualization:
        print("".join(row))

    # Count enclosed area
    enclosed_area = 0
    for r in range(rows):
        for c in range(cols):
            if not outside_visited[r][c] and (r, c) not in loop_set:
                enclosed_area += 1

    # Debug: print results
    print("Total grid cells:", rows * cols)
    print("Outside cells:", sum(sum(row) for row in outside_visited))
    print("Loop cells:", len(loop_set))
    print("Enclosed area:", enclosed_area)

    return enclosed_area


def solve_part_two(data: Any, loop_set: Set[Tuple[int, int]]) -> Any:
    """Solves part two of the challenge."""
    rows: int = len(data)
    cols: int = len(data[0])

    # find start
    start: Optional[Tuple[int, int]] = find_start(data)
    if start is None:
        error_message: str = "Grid has no starting value."
        raise ValueError(error_message)

    start_row, start_col = start

    loop = {(start_row, start_col)}
    q = deque([(start_row, start_col)])

    maybe_s = {"|", "-", "J", "L", "7", "F"}

    while q:
        r, c = q.popleft()
        ch = data[r][c]

        if r > 0 and ch in "S|JL" and data[r - 1][c] in "|7F" and (r - 1, c) not in loop:
            loop.add((r - 1, c))
            q.append((r - 1, c))
            if ch == "S":
                maybe_s &= {"|", "J", "L"}

        if r < rows - 1 and ch in "S|7F" and data[r + 1][c] in "|JL" and (r + 1, c) not in loop:
            loop.add((r + 1, c))
            q.append((r + 1, c))
            if ch == "S":
                maybe_s &= {"|", "7", "F"}

        if c > 0 and ch in "S-J7" and data[r][c - 1] in "-LF" and (r, c - 1) not in loop:
            loop.add((r, c - 1))
            q.append((r, c - 1))
            if ch == "S":
                maybe_s &= {"-", "J", "7"}

        if c < cols - 1 and ch in "S-LF" and data[r][c + 1] in "-J7" and (r, c + 1) not in loop:
            loop.add((r, c + 1))
            q.append((r, c + 1))
            if ch == "S":
                maybe_s &= {"-", "L", "F"}

    assert len(maybe_s) == 1
    start_type: str = next(iter(maybe_s))

    # Replace 'S' with its determined type
    new_data: List[List[str]] = []
    for row in data:
        new_row: List[str] = [start_type if c == 'S' else c for c in row]
        new_data.append(new_row)
    data = new_data

    # Create a cleaned grid with only loop pipes
    cleaned_grid: List[List[str]] = []
    for r, row in enumerate(data):
        new_row: List[str] = [
            data[r][c] if (r, c) in loop else '.'
            for c in range(cols)
        ]
        cleaned_grid.append(new_row)
    data = cleaned_grid

    # Mark outside and loop cells
    outside = set()

    for r, row in enumerate(data):
        within = False
        up = None
        for c, ch in enumerate(row):
            if ch == "|":
                assert up is None
                within = not within
            elif ch == "-":
                assert up is not None
            elif ch in "LF":
                assert up is None
                up = ch == "L"
            elif ch in "7J":
                assert up is not None
                if ch != ("J" if up else "7"):
                    within = not within
                up = None
            elif ch == ".":
                pass
            else:
                raise RuntimeError(f"unexpected character (horizontal): {ch}")
            if not within:
                outside.add((r, c))

    total_cells = rows * cols
    return total_cells - len(outside | loop)


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'

    file_path: str = os.path.join(input_directory, infile)
    unprocessed_data = utils.read_input(file_path)
    input_data = process(unprocessed_data['data'])

    result_part_one, loop_set = solve_part_one(input_data)
    if result_part_one is not None:
        print(f"Part One: {result_part_one}")
    result_part_two = solve_part_two(input_data, loop_set)
    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")
