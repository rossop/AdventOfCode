"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
import re
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
    data: Dict[str, Any] = {}
    pattern: str = r'Register ([A-Z]): (\d+)'
    for match in re.finditer(pattern, raw_data):
        key: str = match.group(1)
        val: int = int(match.group(2))
        data[key] = val

    pattern: str = r'Program: ([\d,]+)'
    matches = re.findall(pattern, raw_data)
    match = matches[0]
    key: str = "program"
    val: List[int] = list(
            map(
            int,
            match.split(',')
            )
    )

    data[key] = val

    return data


def simulate_program(
    registers,
    program,
    expected_output=None
):
    """
    Simulate the 3-bit computer program.
    If expected_output is provided, stop early on divergence or exact match.
    """
    A, B, C = registers
    IP = 0
    output = []

    def get_combo_value(operand):
        if operand <= 3:
            return operand
        elif operand == 4:
            return A
        elif operand == 5:
            return B
        elif operand == 6:
            return C
        elif operand == 7:
            raise ValueError("Invalid combo operand 7")

    while IP < len(program):
        if IP + 1 >= len(program):  # Prevent overflow
            break

        opcode = program[IP]
        operand = program[IP + 1]

        if opcode == 0:  # adv
            A //= 2 ** get_combo_value(operand)
        elif opcode == 1:  # bxl
            B ^= operand
        elif opcode == 2:  # bst
            B = get_combo_value(operand) % 8
        elif opcode == 3:  # jnz
            if A != 0:
                IP = operand
                continue
        elif opcode == 4:  # bxc
            B ^= C
        elif opcode == 5:  # out
            value = get_combo_value(operand) % 8
            output.append(value)

            # Check for divergence
            if expected_output:
                if len(output) > len(expected_output) or output[-1] != expected_output[len(output) - 1]:
                    return False  # Divergence detected
                if len(output) == len(expected_output):
                    return True  # Exact match found

        elif opcode == 6:  # bdv
            B = A // (2 ** get_combo_value(operand))
        elif opcode == 7:  # cdv
            C = A // (2 ** get_combo_value(operand))
        else:
            raise ValueError(f"Invalid opcode: {opcode}")

        IP += 2

    return output if expected_output is None else False


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.

    Args:
        data (Any): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """
    A: int = data['A']
    B: int = data['B']
    C: int = data['C']
    register: Tuple[int, int, int] = (A, B, C)
    program: List[int] = data['program']

    if None in (A, B, C, program):
        return None

    return ','.join(map(str, simulate_program(register, program)))


def find_lowest_valid_a_brute_force(program):
    """
    Find the lowest positive value for register A that causes the program to output itself.
    """
    target_output = program[:]  # Copy of the program
    A = 10037743000
    # Start testing from 1

    while True:
        registers = (A, 0, 0)
        result = simulate_program(registers, program, expected_output=target_output)

        if result is True:  # Exact match found
            return A
        if A % 10000000 == 0:
            print(A)
        A += 1


def find_lowest_valid_a(program):
    """
    Find the lowest positive value for register A that causes the program to output itself.
    Optimized with binary search.
    """
    target_output = program[:]

    def is_valid_a(A):
        registers = (A, 0, 0)
        return simulate_program(registers, program, expected_output=target_output) is True

    # Binary search bounds
    low, high = 1, 2**30  # Arbitrary high bound; adjust if needed

    while low < high:
        mid = (low + high) // 2
        if is_valid_a(mid):
            high = mid  # Narrow the search to lower values
        else:
            low = mid + 1  # Increase the lower bound

    return low if is_valid_a(low) else None


def solve_part_two(data: Any) -> Any:
    """
    Solves part two of the challenge.
    """
    program: List[int] = data['program']
    return find_lowest_valid_a_brute_force(program)


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
