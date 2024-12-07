"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
import sys
from typing import Optional, Tuple, List, Any, Dict, Set
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


def process(data: str) -> Any:
    """Processes the input data.
    """
    processed_data: List[List[str]] = [
        list(line.strip()) for line in data.splitlines()
    ]

    return processed_data


def solve_part_one(data: List[List[str]]) -> Any:
    """Solves part one of the challenge.

    Args:
        data (List[List[str]]): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """
    guard_col: Optional[int] = None
    for i, line in enumerate(data):
        for j, val in enumerate(line):
            if val == '^':
                guard_col = j
        # What if we have > V < instead of ^?
        if guard_col is not None:
            guard_row: int = i
            break

    rows: int = len(data)
    cols: int = len(data[0])

    dirr: List[Tuple[int]] = [
        (-1, 0),  # 0 → ^
        (0, 1),   # 0 → >
        (1, 0),   # 0 → v
        (0, -1)   # 0 → <
    ]
    guard: int = 0  # Starting direction (^)

    loop_corner = [guard_row, guard_col]
    loops = [[]]

    while (0 <= guard_row < rows) and (0 <= guard_col < cols):
        d: Tuple[int, int] = dirr[guard]
        new_row: int = guard_row + d[0]
        new_col: int = guard_col + d[1]

        data[guard_row][guard_col] = 'X'

        if not (0 <= new_row < rows and 0 <= new_col < cols):
            break

        if data[new_row][new_col] == '#':
            guard = (guard + 1) % 4
            loop_corner = [new_row, new_col]
            if len(loops[-1]) < 4:
                loops[-1].append(loop_corner)
            else:
                loops.append([])
                loops[-1].append(loop_corner)
            continue

        if len(loops[-1]) == 3:
            first_corner = loops[-1][0]
            if (new_row == first_corner[0] or new_col == first_corner[1]):
                loop_corner = [new_row, new_col]
                loops[-1].append(loop_corner)
                loops.append([])

        guard_row = new_row
        guard_col = new_col

    # Attempt to solve pt2 with pt1
    # valid_loops: int = len([loop for loop in loops if len(loop) == 4])

    ans: int = sum(row.count('X') for row in data)
    return ans, data


def solve_part_two(data: List[List[str]]) -> Any:
    """Solves part two of the challenge.

    Args:
        data (List[List[str]]): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """
    # Find guard's starting position
    guard_start: Optional[Tuple[int, int]] = None
    rows: int = len(data)
    cols: int = len(data[0])

    for r in range(rows):
        for c in range(cols):
            if data[r][c] == '^':
                guard_start = (r, c)
                break
        if guard_start:
            break

    loop_count: int = 0
    # Try placing obstacle at each position
    for o_r in range(rows):
        for o_c in range(cols):
            # Skip existing obstacles and guard's starting position
            if data[o_r][o_c] in ['#', '^']:
                continue

            r, c = guard_start
            d: int = 0  # 0=up, 1=right, 2=down, 3=left
            seen: Set[Tuple[int, int, int]] = set()

            while True:
                state: Tuple[int, int, int] = (r, c, d)
                if state in seen:
                    loop_count += 1
                    break
                seen.add(state)

                dr, dc = [(-1, 0), (0, 1), (1, 0), (0, -1)][d]
                new_r: int = r + dr
                new_c: int = c + dc

                # Break if guard hits boundary
                if not (0 <= new_r < rows and 0 <= new_c < cols):
                    break

                # Check if guard hits obstacle (existing or new)
                if data[new_r][new_c] == '#' or \
                        (new_r == o_r and new_c == o_c):
                    d = (d + 1) % 4
                else:
                    r, c = new_r, new_c

    return loop_count


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'

    raw_data = read_input(infile)
    input_data = process(raw_data['data'])

    # Create separate copies for each part
    part_one_data = copy.deepcopy(input_data)
    part_two_data = copy.deepcopy(input_data)
    # [row[:] for row in input_data]

    result_part_one, marked_data = solve_part_one(part_one_data)
    result_part_two = solve_part_two(part_two_data)

    if result_part_one is not None:
        print(f"Part One: {result_part_one}")
    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")
