"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
import sys
from typing import Any, Dict, List, Optional, Set, Tuple, Deque
import heapq
from collections import deque


input_directory: str = os.path.join(
    os.path.dirname(
        os.path.abspath(
            os.path.dirname(__file__)
        )
    ), 'in'
)


def read_input(file_name: str) -> Dict[str, Any]:
    """Reads input from a specified file and separates metadata for test files.

    Args:
        file_name (str): Name of the input file (.in or .test)

    Returns:
        Dict[str, Any]: Dictionary containing:
            - 'data': Raw string of input data
            - 'answer_a': Expected answer for part 1 (None for .in files)
            - 'answer_b': Expected answer for part 2 (None for .in files)
    """
    file_path: str = os.path.join(input_directory, file_name)
    result: Dict[str, Any] = {
        'data': None,
        'answer_a': None,
        'answer_b': None
    }

    with open(file_path, 'r', encoding='utf-8') as file:
        content: str = file.read()

        # Handle .test files with metadata
        if file_name.endswith('.test'):
            # Find the data section between Example data marker and answer
            # section
            data_start: int = content.find('Example data')
            if data_start != -1:
                data_start = content.find('\n', data_start) + 1
                data_end: int = content.find('\n-----------------', data_start)
                if data_end != -1:
                    result['data'] = content[data_start:data_end].strip()

            # Extract answers if present
            answer_section: str = content[data_end:] if data_end != -1 else ''
            for line in answer_section.splitlines():
                if line.startswith('answer_a:'):
                    ans: str = line.split(':')[1].strip()
                    result['answer_a'] = ans if ans != '-' else None
                elif line.startswith('answer_b:'):
                    ans: str = line.split(':')[1].strip()
                    result['answer_b'] = ans if ans != '-' else None

        # Handle regular .in files
        else:
            result['data'] = content.strip()

    return result


def process(raw_data: str) -> Any:
    """Processes the input data.
    """
    data: List[List[str]] = [
        list(line) for line in raw_data.splitlines()
    ]
    return data


def find_start_and_end(
    grid: List[List[str]]
) -> Tuple[Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
    """Find Start and End
    """
    end: Optional[Tuple[int, int]] = None
    start: Optional[Tuple[int, int]] = None

    found_counter: int = 0

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == 'S':
                start = (r, c)
                found_counter += 1
                if found_counter > 1:
                    break
            elif cell == 'E':
                end = (r, c)
                found_counter += 1
                if found_counter > 1:
                    break
    return start, end


def is_valid_move(
    grid: List[List[str]],
    x: int,
    y: int
) -> bool:
    """Checks if a move is valid (within bounds and not into a wall
    """
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != '#'


def dikstra(
    grid: List[List[str]],
    start: Tuple[int, int],
    end: Tuple[int, int]
) -> int:
    """Implements Dikstra's algorithm to find the minimum cost from start to
    end
    """
    directions: List[Tuple[int, int]] = [
        (0, 1),   # East
        (1, 0),   # South
        (0, -1),  # West
        (-1, 0)   # North
    ]
    pq: List[Tuple[int, int, int, int]] = [
        (
            0,          # cost
            start[0],   # x
            start[1],   # y
            0,          # direction
        )
    ]
    visited: Set[Tuple[int, int, int]] = set()  # (x, y, direction)

    while pq:
        cost, x, y, d = heapq.heappop(pq)

        if (x, y) == end:
            return cost

        if (x, y, d) in visited:
            continue
        visited.add((x, y, d))

        # Forward move
        nx, ny = x + directions[d][0], y + directions[d][1]
        if is_valid_move(grid, nx, ny):
            heapq.heappush(pq, (cost + 1, nx, ny, d))

        # Rotate clockwise
        nd = (d + 1) % 4
        heapq.heappush(pq, (cost + 1000, x, y, nd))

        # Rotate anti-clockwise
        nd = (d - 1) % 4
        heapq.heappush(pq, (cost + 1000, x, y, nd))

    raise ValueError("No path found from start to end")


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.

    Args:
        data (Any): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """
    start, end = find_start_and_end(data)
    if start is None or end is None:
        return None

    return dikstra(data, start, end)


def visualize_optimal_tiles(
    grid: List[List[str]],
    optimal_tiles: Set[Tuple[int, int]]
) -> None:
    """Visualizes the optimal tiles in the grid.

    Args:
        grid (List[List[str]]): The original grid
        optimal_tiles (Set[Tuple[int, int]]): Set of optimal path coordinates
    """
    for r in range(len(grid)):
        row = ""
        for c in range(len(grid[0])):
            if grid[r][c] == '#':
                row += '#'
            elif (r, c) in optimal_tiles:
                row += 'O'
            else:
                row += '.'
        print(row)


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.

    Args:
        data (List[str]): The input data for the challenge.

    Returns:
        int: Number of tiles that are part of any optimal path.
    """
    start, end = find_start_and_end(data)
    if start is None or end is None:
        return None

    # Find minimum cost first
    min_cost = dikstra(data, start, end)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Forward pass from start
    forward_costs: Dict[Tuple[int, int, int], int] = {}
    pq: List[Tuple[int, int, int, int]] = [(0, start[0], start[1], 0)]
    seen: Set[Tuple[int, int, int]] = set()

    while pq:
        cost, r, c, d = heapq.heappop(pq)
        state = (r, c, d)
        if state not in forward_costs:
            forward_costs[state] = cost
        if state in seen:
            continue
        seen.add(state)

        # Forward move
        dr, dc = directions[d]
        nr, nc = r + dr, c + dc
        if is_valid_move(data, nr, nc):
            heapq.heappush(pq, (cost + 1, nr, nc, d))
        # Rotations
        heapq.heappush(pq, (cost + 1000, r, c, (d + 1) % 4))
        heapq.heappush(pq, (cost + 1000, r, c, (d - 1) % 4))

    # Backward pass from end
    backward_costs: Dict[Tuple[int, int, int], int] = {}
    pq = [(0, end[0], end[1], d) for d in range(4)]
    seen = set()

    while pq:
        cost, r, c, d = heapq.heappop(pq)
        state = (r, c, d)
        if state not in backward_costs:
            backward_costs[state] = cost
        if state in seen:
            continue
        seen.add(state)

        # Backward move (opposite direction)
        dr, dc = directions[(d + 2) % 4]
        nr, nc = r + dr, c + dc
        if is_valid_move(data, nr, nc):
            heapq.heappush(pq, (cost + 1, nr, nc, d))
        # Rotations
        heapq.heappush(pq, (cost + 1000, r, c, (d + 1) % 4))
        heapq.heappush(pq, (cost + 1000, r, c, (d - 1) % 4))

    # Find all positions that are part of optimal paths
    optimal_tiles: Set[Tuple[int, int]] = set()
    for r in range(len(data)):
        for c in range(len(data[0])):
            for d in range(4):
                state = (r, c, d)
                if (
                    state in forward_costs and
                    state in backward_costs and
                    forward_costs[state] + backward_costs[state] == min_cost
                ):
                    optimal_tiles.add((r, c))
                    break

    return len(optimal_tiles)


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'

    unprocessed_data = read_input(infile)
    input_data = process(unprocessed_data['data'])

    result_part_one = solve_part_one(input_data)
    if result_part_one is not None:
        print(f"Part One: {result_part_one}")
    result_part_two = solve_part_two(input_data)
    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")
