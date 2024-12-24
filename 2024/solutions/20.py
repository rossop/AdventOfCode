"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

from collections import deque
import copy
import os
import sys
from typing import Any, Callable, Deque, List, Optional, Set, Tuple

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
) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Find start and end point in the 2D maze
    """
    start: Optional[Tuple[int, int]] = None
    end: Optional[Tuple[int, int]] = None

    point_counter: int = 0  # counts relevant points found

    # Find start and end
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == 'S':
                start = (r, c)
                point_counter += 1
                if point_counter == 2:
                    break
            elif val == 'E':
                end = (r, c)
                point_counter += 1
                if point_counter == 2:
                    break

    if start is None or end is None:
        error_str: str = "Grid is missing either start or end position."
        raise ValueError(error_str)
    return start, end


def bfs_with_constraints(
    grid: List[List[str]],
) -> Optional[List[List[Tuple[int, int]]]]:
    """Perform BFS on a grid to find all shortest paths from start to end.
    Allow to step across one wall tile at any point
    """
    if grid is None or len(grid) < 1 or len(grid[0]) < 1:
        return None

    rows: int = len(grid)
    cols: int = len(grid[0])

    directions: List[Tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    start, end = find_start_end(grid)

    # Queue format: (row, col, cheat_count, in_cheat_mode, path)
    queue: Deque = deque([(start[0], start[1], 0, False, [start])])
    visited: Set = set()
    valid_paths: List[List[Tuple[int, int]]] = []

    while queue:
        x, y, cheat_count, in_cheat_mode, path = queue.popleft()

        if (x, y) == end:
            valid_paths.append(path)
            continue

        state = (x, y, cheat_count, in_cheat_mode)
        if state in visited:
            continue
        visited.add(state)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                new_path = path + [(nx, ny)]

                if grid[nx][ny] in '.SE':
                    # Normal move on path
                    queue.append((nx, ny, cheat_count, False, new_path))
                elif grid[nx][ny] == '#':
                    # Start or continue cheating if allowed
                    if not in_cheat_mode and cheat_count == 0:
                        # Start new cheat sequence
                        queue.append((nx, ny, 1, True, new_path))
                    elif in_cheat_mode and cheat_count < 20:
                        # Continue existing cheat sequence
                        queue.append((nx, ny, cheat_count + 1, True, new_path))

    return valid_paths


def bfs(
    grid: List[List[str]],
    start: Tuple[int, int],
    end_condition: Callable[[int, int], bool]
) -> List[List[Tuple[int, int]]]:
    """
    Perform BFS on a grid and return paths or distances based on the given
    end_condition.

    :param grid: 2D grid representation.
    :param start: Starting point as (row, col).
    :param end_condition: A callable that determines when to stop BFS (e.g.,
        reaching 'E').
    :return: List of all paths or distances depending on the end_condition.
    """
    if grid is None or len(grid) < 1 or len(grid[0]) < 1:
        error_str: str = "Invalid grid size."
        raise ValueError(error_str)

    rows: int = len(grid)
    cols: int = len(grid[0])

    directions: List[Tuple[int, int]] = [
        (0, 1),   # Right
        (0, -1),  # Left
        (1, 0),   # Down
        (-1, 0)   # Up
    ]
    queue: Deque[Any] = deque(
        [
            (start[0], start[1], [start])
        ]
    )
    result: List[Any] = []

    while queue:
        x, y, path = queue.popleft()

        if end_condition(x, y):
            result.append(path)
            continue

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < rows and
                0 <= ny < cols and
                grid[nx][ny] in '.SE'
            ):
                if (nx, ny) not in path:
                    queue.append((nx, ny, path + [(nx, ny)]))
    return result


def bfs_with_paths(
    grid: List[List[str]],
) -> List[List[Tuple[int, int]]]:
    """ Perform BFS to find all paths from 'S' to 'E'.
    """
    start, end = find_start_end(grid)
    return bfs(grid, start, lambda x, y: (x, y) == end)


def evaluate_shortcut(
    paths: List[List[Tuple[int, int]]],
    shortcut: Tuple[Tuple[int, int], Tuple[int, int]]
) -> int:
    """
    Evaluate the benefit of applying a shortcut betweeen two points.
    Shortcut: (entry_point, exit_point).
    """
    entry_point, exit_point = shortcut
    for path in paths:
        if entry_point in path and exit_point in path:  # Both on same path
            entry_idx: int = path.index(entry_point)
            exit_idx: int = path.index(exit_point)
            if entry_idx < exit_idx:  # ensure valid order
                shortcut_length: int = exit_idx - entry_idx - 2
                return shortcut_length
    return 0  # No valid shortcut found


def find_shortcuts(
    grid: List[List[str]],
    paths: List[List[Tuple[int, int]]]
) -> List[Tuple[Tuple[int, int], Tuple[int, int], int]]:
    """
    Find and evaluate all potential shortcuts in the grid, optimized using
    precomputed paths.
    """
    shortcuts: List = []

    rows: int = len(grid)
    cols: int = len(grid[0])

    directions: List[Tuple[int, int]] = [
        (0, 1),   # Right
        (0, -1),  # Left
        (1, 0),   # Down
        (-1, 0)   # Up
    ]

    path_points = set()
    for path in paths:
        path_points.update(path)

    for path in paths:
        for (r, c) in path:
            # Check adjacent walls and their opposite sides
            for dr, dc in directions:
                wall_r, wall_c = r + dr, c + dc
                opp_r, opp_c = wall_r + dr, wall_c + dc
                if (
                    0 <= wall_r < rows and
                    0 <= wall_c < cols and
                    grid[wall_r][wall_c] == '#' and
                    0 <= opp_r < rows and
                    0 <= opp_c < cols and
                    (opp_r, opp_c) in path_points
                ):  # Find entry and exit points
                    shortcut = ((r, c), (opp_r, opp_c))
                    benefit = evaluate_shortcut(paths, shortcut)
                    if benefit > 0:
                        shortcuts.append((shortcut[0], shortcut[1], benefit))
    return shortcuts


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        return None

    grid = copy.deepcopy(data)
    # Compute all paths
    paths = bfs_with_paths(grid)

    # Find and evaluate shortcuts
    shortcuts = find_shortcuts(grid, paths)

    # Print results
    for entry_point, exit_point, benefit in shortcuts:
        msg: str = (
            f"Shortcut from {entry_point} to "
            f"{exit_point} saves {benefit} steps."
        )
        # print(msg)

    # Define a benefit threshold
    threshold = 100  # Adjust this value to your desired benefit threshold

    # Use filter to get shortcuts meeting the threshold
    filtered_shortcuts = list(
        filter(
            lambda s: s[2] >= threshold,
            shortcuts
        )
    )

    # Print the filtered results
    for entry_point, exit_point, benefit in filtered_shortcuts:
        msg: str = (
            f"Shortcut from {entry_point} to "
            f"{exit_point} saves {benefit} steps."
        )
        # print(msg)

    return len(filtered_shortcuts)


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.
    """
    if data is None:
        return None

    grid = copy.deepcopy(data)
    rows: int = len(grid)
    cols: int = len(grid[0])

    # Find start position
    start_r: int = 0
    start_c: int = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start_r = r
                start_c = c
                break
        else:
            continue
        break

    # Calculate distances from start using BFS
    dists: List[List[int]] = [[-1] * cols for _ in range(rows)]
    dists[start_r][start_c] = 0

    r, c = start_r, start_c
    while grid[r][c] != 'E':
        for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
            if nr < 0 or nc < 0 or nr >= rows or nc >= cols:
                continue
            if grid[nr][nc] == '#':
                continue
            if dists[nr][nc] != -1:
                continue
            dists[nr][nc] = dists[r][c] + 1
            r, c = nr, nc

    # Count shortcuts that save >= 100 steps
    count: int = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '#':
                continue
            # Check all possible cheat lengths (2 to 20)
            for radius in range(2, 21):
                for dr in range(radius + 1):
                    dc: int = radius - dr
                    # Check all four diagonal directions
                    for nr, nc in {
                        (r + dr, c + dc),
                        (r + dr, c - dc),
                        (r - dr, c + dc),
                        (r - dr, c - dc)
                    }:
                        if nr < 0 or nc < 0 or nr >= rows or nc >= cols:
                            continue
                        if grid[nr][nc] == '#':
                            continue
                        # Check if shortcut saves at least 100 + radius steps
                        if dists[r][c] - dists[nr][nc] >= 100 + radius:
                            count += 1

    return count


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
