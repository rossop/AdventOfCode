"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
import sys
from typing import Any, Dict, List, Optional, Tuple


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
    return list(map(int, raw_data))


def decrypt_disk(encryption: str) -> List[Optional[int]]:
    """Decrypt Disk
    """
    decrypted_disk_list: List[Optional[int]] = []
    val: int = 0
    for position, count in enumerate(encryption):
        # Ensure count is treated as an integer
        count: int = int(count)  # Convert count to int
        if position % 2 == 0:
            decrypted_disk_list.extend([val] * count)
            val += 1
        else:
            decrypted_disk_list.extend([None] * count)
    return decrypted_disk_list


def tuple_decrypt_disk(encryption: str) -> List[Tuple[int, Optional[int]]]:
    """Decrypt Disk using Tuples
    """
    decrypted_disk_list: List[Tuple[int, Optional[int]]] = []
    val: int = 0
    for position, count in enumerate(encryption):
        # Ensure count is treated as an integer
        count: int = int(count)  # Convert count to int
        if position % 2 == 0:
            decrypted_disk_list.append((count, val))
            val += 1
        else:
            decrypted_disk_list.append((count, None))
    return decrypted_disk_list


def move_file_blocks(dd: List[Optional[int]]) -> List[Optional[int]]:
    """Moves file blocks
    """
    p1, p2 = 0, len(dd) - 1
    while p1 < p2:
        if dd[p1] is not None:
            p1 += 1
        else:
            if dd[p2] is None:
                p2 -= 1
                continue
            dd[p1], dd[p2] = dd[p2], dd[p1]

    return dd


def defrag(
    disk: List[Tuple[int, Optional[int]]]
) -> List[Tuple[int, Optional[int]]]:
    """ Defrag Disk
    """
    p2: int = len(disk) - 1

    while p2 > 0:
        if disk[p2][1] is None:
            p2 -= 1
            continue
        p1: int = 0
        while p1 < p2:
            if disk[p1][1] is not None:
                p1 += 1
                continue
            if disk[p2][0] == disk[p1][0]:
                disk[p1], disk[p2] = disk[p2], disk[p1]
                break
            elif disk[p2][0] < disk[p1][0]:
                moving_part = disk[p2]
                still_part = (disk[p1][0] - disk[p2][0], None)
                empty_part = (disk[p2][0], None)
                disk = (
                    disk[:p1] + [moving_part, still_part]
                    + disk[p1+1:p2] + [empty_part] + disk[p2+1:]
                )
                p2 += 1
                break
            else:
                p1 += 1

        p2 -= 1
    return disk


def linearise_disk(
    tuple_disk: List[Tuple[int, Optional[int]]]
) -> List[Optional[int]]:
    """Go from Tuple representation of list of ints"""
    disk: List[Optional[int]] = []
    for count, val in tuple_disk:
        disk.extend([val] * count)
    return disk


def filesystem_checksum(disk: List[Optional[int]]) -> int:
    """Calculate disk checksum
    """
    checksum: int = 0

    for pos, digit in enumerate(disk, start=0):
        if digit is not None:
            checksum += pos * int(digit)

    return checksum


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.

    Args:
        data (Any): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """
    decrypted_disk_str: List[Optional[int]] = decrypt_disk(data)
    cleared_disk_str: List[Optional[int]] = move_file_blocks(
        decrypted_disk_str
    )
    checksum: int = filesystem_checksum(cleared_disk_str)
    return checksum


def print_disk(disk: List[Optional[int]]) -> None:
    """Print disk
    """
    disk_str: str = ''.join(
        [str(digit) if digit is not None else '.' for digit in disk]
    )
    print(disk_str)


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.

    Args:
        data (List[str]): The input data for the challenge.

    Returns:
        Any: The result of the solution for part two.
    """
    decrypted_disk: List[Tuple[int, Optional[int]]] = tuple_decrypt_disk(data)
    defragged_disk: List[Tuple[int, Optional[int]]] = defrag(decrypted_disk)
    linearised_disk: List[Optional[int]] = linearise_disk(defragged_disk)
    checksum: int = filesystem_checksum(linearised_disk)
    return checksum


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
