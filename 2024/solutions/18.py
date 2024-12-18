"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

from collections import deque
import os
import sys
from typing import Any, Deque, Dict, List, Optional, Set, Tuple
import copy


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
    data: Dict[str, Any] = {}
    data['coordinates'] =  [
        tuple(
            map(
                int,
                line.split(",")
                )
            ) for line in raw_data.splitlines()
    ]
    return data


def solve(data: Any) -> Any:
    """Solves part one of the challenge.

    Args:
        data (Any): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """
    cols: int = data['cols']
    rows: int = data['rows']
    coordinates: List[Tuple[int, int]] = data['coordinates']
    threshold: int = data['threshold']
    grid : List[List[str]] = [['.' for _ in range(cols)] for _ in range(rows)]

    for i, coordinate in enumerate(coordinates):
        x: int = coordinate[0]
        y: int = coordinate[1]
        grid[y][x] = '#'
        if i + 1 == threshold:
            break

     # for line in grid:
     #    print("".join(line))


    def bfs(
        grid: List[List[str]],
        start: Tuple[int, int],
        end: Tuple[int, int]
    ) -> Tuple[int, Optional[List[Tuple[int, int]]]]:
        """Breadth-First Search"""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        rows, cols = len(grid), len(grid[0])
        if (
            grid[start[1]][start[0]] == '#' or # x, y coordinate system
            grid[end[1]][end[0]] == '#'
        ):
            return -1, None
        queue: Deque[Tuple[Tuple[int, int], int]] = deque([(start, 0)])
        visited = set()
        parent: Dict[Tuple[int, int], Tuple[int, int]] = {}
        visited.add(start)


        while queue:
            coordinate, steps = queue.popleft()

            r, c = coordinate

            # Have we reached the end?
            if (r, c) == end:
                path = []
                current = end
                while current != start:
                    path.append(current)
                    current = parent[current]
                path.append(start)
                path.reverse()
                return steps, path

            # Erplore neighbors
            for dr, dc in directions:
                nr: int = r + dr
                nc: int = c + dc

                # Check bounds
                if (
                    0 <= nr < rows and
                    0 <= nc < cols and
                    (nr, nc) not in visited and
                    grid[nr][nc] != '#'
                ):
                    visited.add((nr, nc))
                    parent[(nr, nc)] = (r, c)
                    queue.append(((nr, nc), steps + 1))
        return -1, None  # Path not found

    shortest_path_steps, path = \
        bfs(grid, (0,0), (cols-1, rows-1))  # from x,y to r,c

    if path is None:
        return shortest_path_steps, None

    printable_grid = copy.deepcopy(grid)

    for i, coordinate in enumerate(list(path)):
        r: int = coordinate[0]
        c: int = coordinate[1]
        printable_grid[r][c] = 'O'

    #     print()
    #     for line in grid:
    #         print("".join(line))
    #     print()
    #     for line in printable_grid:
    #         print("".join(line))


    # Place bytes one by one and check if the exit becomes unreachable
    for i, (x, y) in enumerate(coordinates[threshold:]):
        grid[y][x] = '#'  # Corrupt the memory at this coordinate

        # Check if the path is blocked
        shortest_path_len, _ = bfs(grid, (0, 0), (cols - 1, rows - 1))
        if shortest_path_len < 0:
             return shortest_path_steps, f"{x},{y}"

    return shortest_path_steps, None


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'

    unprocessed_data = read_input(infile)
    input_data = process(unprocessed_data['data'])
    if 'test' in infile:
        input_data['rows'] = 7  # from 0 to 6 both included
        input_data['cols'] = 7
        input_data['threshold'] = 12
    else:
        input_data['rows'] = 71  # from 0 to 70 both included
        input_data['cols'] = 71
        input_data['threshold'] = 1024

    result_part_one, result_part_two = solve(input_data)
    if result_part_one is not None:
        print(f"Part One: {result_part_one}")
    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")
