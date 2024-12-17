"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
import sys
from typing import Any, Dict, Set, List, Tuple
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
    return [
        list(line) for line in raw_data.splitlines()
    ]


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.

    Args:
        data (Any): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """
    # Find Regions
    # This is similar to Island problems in Leetcode
    rows: int = len(data)
    cols: int = len(data[0])

    regions: Dict = {}
    visited: Set = set()
    grid: List[List[str]] = copy.deepcopy(data)

    def dfs(i, j, region):
        if (
            i < 0 or
            i >= rows or
            j < 0 or
            j >= cols or
            grid[i][j] != region[0]
        ):
            regions[region]["perimeter"] += 1
            return "Perimeter"
        elif (i, j) in visited:
            return "Visited"

        visited.add((i, j))
        regions[region]["plants"].append((i, j))
        regions[region]["area"] += 1
        status = dfs(i+1, j, region)
        if status == "Perimeter":
            regions[region]["PerimeterPlants"].append((i+1, j))
        status = dfs(i-1, j, region)
        if status == "Perimeter":
            regions[region]["PerimeterPlants"].append((i-1, j))
        status = dfs(i, j+1, region)
        if status == "Perimeter":
            regions[region]["PerimeterPlants"].append((i, j+1))
        status = dfs(i, j-1, region)
        if status == "Perimeter":
            regions[region]["PerimeterPlants"].append((i, j-1))
        return

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                label: str = grid[r][c]
                region: Tuple[str, int, int] = (label, r, c)
                regions[region] = {
                    "plants": [],
                    "perimeter": 0,
                    "area": 0,
                    "PerimeterPlants": []
                }
                # use region for differentiate regions with same letter
                dfs(r, c, region)

    # calc values
    ans: int = 0
    for identification, info in regions.items():
        perimeter: int = info["perimeter"]
        area: int = info["area"]
        # sides = count_sides(info["plants"], info["PerimeterPlants"])
        ans += area * perimeter

    return ans


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.

    Args:
        data (List[str]): The input data for the challenge.

    Returns:
        Any: The result of the solution for part two.
    """
    # TODO: Implement the solution for part two
    return None


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
