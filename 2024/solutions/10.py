"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
import sys
from typing import Any, Dict, Tuple, List, Set


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
    return [
        [
            int(num) for num in line
        ] for line in raw_data.splitlines()
    ]


def find_trailheads(
    topographic_map: List[List[int]]
) -> List[Tuple[int, int]]:
    """Finds zero height on topological map
    """
    trailheads: List[Tuple[int, int]] = []

    rows: int = len(topographic_map)
    cols: int = len(topographic_map[0])

    for r in range(rows):
        for c in range(cols):
            if topographic_map[r][c] == 0:
                trailheads.append((r, c))

    return trailheads


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.

    Args:
        data (Any): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """
    # Find tailheads
    trailheads: List[Tuple[int, int]] = find_trailheads(data)
    memo: Set[Tuple[int, int, int]] = {}

    rows: int = len(data)
    cols: int = len(data[0])

    # Find path
    def dfs(r: int, c: int, current_height: int) -> set[tuple[int, int]]:
        """Performs depth-first search to find reachable positions with
        height 9.
        """
        if not (0 <= r < rows and 0 <= c < cols):
            return set()  # Out of Bounds
        if data[r][c] != current_height:
            return set()  # Invalid Step
        if current_height == 9:
            return {(r, c)}  # Reached height 9

        if (r, c, current_height) in memo:
            return memo[(r, c, current_height)]

        neighbours: list[tuple[int, int]] = [
            (r + dx, c + dy) for dx, dy in [
                (-1, 0), (1, 0), (0, -1), (0, 1)
            ]
        ]
        reachable_nines: set[tuple[int, int]] = set()
        for nx, ny in neighbours:
            reachable_nines |= dfs(nx, ny, current_height + 1)

        memo[(r, c, current_height)] = reachable_nines
        return reachable_nines

    total_score: int = 0
    for r, c in trailheads:
        total_score += len(dfs(r, c, 0))

    return total_score


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.

    Args:
        data (List[List[int]]): The input data for the challenge.

    Returns:
        int: The number of distinct paths reaching height 9.
    """
    # Find tailheads
    trailheads: List[Tuple[int, int]] = find_trailheads(data)
    memo: Dict[Tuple[int, int, int], List[List[Tuple[int, int]]]] = {}
    rows: int = len(data)
    cols: int = len(data[0])

    def dfs(
        r: int,
        c: int,
        current_height: int,
        current_path: List[Tuple[int, int]]
    ) -> List[List[Tuple[int, int]]]:
        """Performs depth-first search to find all paths reaching height 9.
        """
        if not (0 <= r < rows and 0 <= c < cols):
            return []  # Out of Bounds
        if data[r][c] != current_height:
            return []  # Invalid Step

        new_path: List[Tuple[int, int]] = current_path + [(r, c)]

        if current_height == 9:
            return [new_path]  # Reached height 9

        if (r, c, current_height) in memo:
            return [current_path + p for p in memo[(r, c, current_height)]]

        neighbours: List[Tuple[int, int]] = [
            (r + dx, c + dy) for dx, dy in [
                (-1, 0), (1, 0), (0, -1), (0, 1)
            ]
        ]
        distinct_paths: List[List[Tuple[int, int]]] = []
        for nx, ny in neighbours:
            distinct_paths.extend(
                dfs(nx, ny, current_height + 1, new_path)
            )

        # Store only the part of the paths after current position
        memo[(r, c, current_height)] = [
            p[len(new_path):] for p in distinct_paths
        ]
        return distinct_paths

    all_distinct_paths: List[List[Tuple[int, int]]] = []
    for r, c in trailheads:
        all_distinct_paths.extend(dfs(r, c, 0, []))

    return len(all_distinct_paths)


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
