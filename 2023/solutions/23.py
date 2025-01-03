"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

from collections import deque
import os
import sys
from typing import Any, Deque, Dict, List, Set, Tuple
import copy

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


def find_path(data: Any):
    """Shared path finding algorithm"""
    start: Tuple[int, int] = (0, "".join(data[0]).index("."))
    end: Tuple[int, int] = (len(data) - 1, "".join(data[-1]).index("."))

    points: List[Tuple[int, int]] = [start, end]

    for r, row in enumerate(data):
        for c, ch in enumerate(row):
            if ch == "#":
                continue
            neighbors = 0
            for nr, nc in [
                (r - 1, c),
                (r + 1, c),
                (r, c - 1),
                (r, c + 1)
            ]:
                if (
                    0 <= nr < len(data) and
                    0 <= nc < len(data[0]) and
                    data[nr][nc] != "#"
                ):
                    neighbors += 1
            if neighbors >= 3:
                points.append((r, c))

    # Initialize graph dictionary for all points
    graph: Dict[Tuple[int, int], Dict[Tuple[int, int], int]] = {
        pt: {} for pt in points
    }

    dirs: Dict[str, List[Tuple[int, int]]] = {
        "^": [(-1, 0)],
        "v": [(1, 0)],
        "<": [(0, -1)],
        ">": [(0, 1)],
        ".": [(-1, 0), (1, 0), (0, -1), (0, 1)],
    }

    # Build graph of connections between points
    for sr, sc in points:
        stack: List[Tuple[int, int, int]] = [(0, sr, sc)]
        seen: Set[Tuple[int, int]] = {(sr, sc)}

        while stack:
            n, r, c = stack.pop()

            if n != 0 and (r, c) in points:
                graph[(sr, sc)][(r, c)] = n
                continue

            for dr, dc in dirs[data[r][c]]:
                nr: int = r + dr
                nc: int = c + dc
                if (0 <= nr < len(data) and
                    0 <= nc < len(data[0]) and
                    data[nr][nc] != "#" and
                        (nr, nc) not in seen):
                    stack.append((n + 1, nr, nc))
                    seen.add((nr, nc))

    seen: Set[Tuple[int, int]] = set()

    def dfs(pt: Tuple[int, int]) -> int:
        """Performs depth-first search to find longest path.

        Args:
            pt: Current point in the graph

        Returns:
            int: Length of longest path from current point to end
        """
        if pt == end:
            return 0

        max_len: int = float("-inf")

        seen.add(pt)
        for next_pt in graph[pt]:
            if next_pt not in seen:
                max_len = max(max_len, dfs(next_pt) + graph[pt][next_pt])
        seen.remove(pt)

        return max_len

    return dfs(start)


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        return None

    return find_path(data)


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.
    """
    grid = copy.deepcopy(data)

    for r, row in enumerate(data):
        for c, val in enumerate(row):
            if val != '#':
                grid[r][c] = '.'
            else:
                grid[r][c] = '#'

    return find_path(grid)


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
