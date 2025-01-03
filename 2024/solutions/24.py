"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

import os
from pprint import pprint
import sys
from typing import Any, Callable, Dict, List, Set, Tuple

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
    info: List[str] = raw_data.split('\n\n')
    processed_data: Dict = {}
    processed_data['inputs'] = {}
    processed_data['operations'] = []

    processed_data['inputs'].update(
        map(
            lambda line: (
                line.split(': ')[0],
                int(line.split(': ')[1])
            ),
            info[0].splitlines()
        )
    )

    processed_data['operations'].extend(
        map(
            lambda line: (
                line.split(' ')[0],
                line.split(' ')[1],
                line.split(' ')[2],
                line.split(' ')[4],
            ),
            info[1].splitlines()
        )
    )
    # pprint(processed_data)
    return processed_data


def simulate_wiring(
    inputs: Dict[str, int],
    operations: List[Tuple[str, str, str, str]]
):
    """
    Starting with inputs and operations, simulates wiring.
    """
    operation_map: Dict[str, Callable[[int, int], int]] = {
        "AND": lambda x, y: x and y,  # Logical AND
        "OR": lambda x, y: x or y,   # Logical OR
        "XOR": lambda x, y: x ^ y,   # Logical XOR
    }

    while True:
        filtered_tuples = list(
            filter(
                lambda t: (
                    t[3] not in inputs and  # Already processed
                    t[0] in inputs and      # First input present
                    t[2] in inputs          # Second input present
                ),
                operations
            ),
        )
        if len(filtered_tuples) < 1:
            break

        for ft in filtered_tuples:
            bin1: int = inputs[ft[0]]
            op: str = ft[1]
            bin2: int = inputs[ft[2]]
            inputs[ft[3]] = operation_map[op](bin1, bin2)

    return inputs


def compute_binary_values(inputs):
    """Compute binary values for x, y, z
    """
    x_value: int = int(
        "".join(str(inputs[key]) for key in sorted(inputs) if key.startswith('x')), 2)
    y_value: int = int(
        "".join(str(inputs[key]) for key in sorted(inputs) if key.startswith('y')), 2)
    z_value: int = int(
        "".join(str(inputs[key]) for key in sorted(inputs) if key.startswith('z')), 2)
    return x_value, y_value, z_value


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        error_str: str = "Invalid input data"
        raise ValueError(error_str)

    inputs: Dict[str, int] = data['inputs']
    operations: List[Tuple[str, str, str, str]] = data['operations']

    inputs: Dict[str, int] = simulate_wiring(inputs, operations)

    binary_value: str = "".join(
        str(inputs[key]) for key in sorted(
            inputs,
            reverse=True
        ) if key.startswith('z')
    )

    # print('Binary Value: ', binary_value)
    integer_value: int = int(binary_value, 2)  # Part One Result
    return integer_value


def make_wire(char: str, num: int) -> str:
    """Creates a wire identifier string.

    Args:
        char: The wire type (x, y, or z)
        num: The wire number

    Returns:
        Formatted wire identifier
    """
    return char + str(num).rjust(2, "0")


def verify_z(wire: str, num: int, formulas: Dict) -> bool:
    """Verifies if a z-wire correctly implements addition.

    Args:
        wire: Wire identifier to verify
        num: Bit position
        formulas: Dictionary of circuit formulas

    Returns:
        True if wire correctly implements addition
    """
    if wire not in formulas:
        return False
    op, x, y = formulas[wire]
    if op != "XOR":
        return False
    if num == 0:
        return sorted([x, y]) == ["x00", "y00"]
    return (verify_intermediate_xor(x, num, formulas) and
            verify_carry_bit(y, num, formulas)) or (
        verify_intermediate_xor(y, num, formulas) and
        verify_carry_bit(x, num, formulas))


def verify_intermediate_xor(wire: str, num: int, formulas: Dict) -> bool:
    """Verifies intermediate XOR operations.

    Args:
        wire: Wire identifier to verify
        num: Bit position
        formulas: Dictionary of circuit formulas

    Returns:
        True if wire correctly implements XOR
    """
    if wire not in formulas:
        return False
    op, x, y = formulas[wire]
    if op != "XOR":
        return False
    return sorted([x, y]) == [make_wire("x", num), make_wire("y", num)]


def verify_carry_bit(wire: str, num: int, formulas: Dict) -> bool:
    """Verifies carry bit operations.

    Args:
        wire: Wire identifier to verify
        num: Bit position
        formulas: Dictionary of circuit formulas

    Returns:
        True if wire correctly implements carry
    """
    if wire not in formulas:
        return False
    op, x, y = formulas[wire]
    if num == 1:
        if op != "AND":
            return False
        return sorted([x, y]) == ["x00", "y00"]
    if op != "OR":
        return False
    return (verify_direct_carry(x, num - 1, formulas) and
            verify_recarry(y, num - 1, formulas)) or (
        verify_direct_carry(y, num - 1, formulas) and
        verify_recarry(x, num - 1, formulas))


def verify_direct_carry(wire: str, num: int, formulas: Dict) -> bool:
    """Verifies direct carry generation.

    Args:
        wire: Wire identifier to verify
        num: Bit position
        formulas: Dictionary of circuit formulas

    Returns:
        True if wire correctly implements direct carry
    """
    if wire not in formulas:
        return False
    op, x, y = formulas[wire]
    if op != "AND":
        return False
    return sorted([x, y]) == [make_wire("x", num), make_wire("y", num)]


def verify_recarry(wire: str, num: int, formulas: Dict) -> bool:
    """Verifies carry recombination.

    Args:
        wire: Wire identifier to verify
        num: Bit position
        formulas: Dictionary of circuit formulas

    Returns:
        True if wire correctly implements carry recombination
    """
    if wire not in formulas:
        return False
    op, x, y = formulas[wire]
    if op != "AND":
        return False
    return (verify_intermediate_xor(x, num, formulas) and
            verify_carry_bit(y, num, formulas)) or (
        verify_intermediate_xor(y, num, formulas) and
        verify_carry_bit(x, num, formulas))


def verify(num: int, formulas: Dict) -> bool:
    """Verifies if bit position implements correct addition.

    Args:
        num: Bit position to verify
        formulas: Dictionary of circuit formulas

    Returns:
        True if bit position correctly implements addition
    """
    return verify_z(make_wire("z", num), num, formulas)


def progress(formulas: Dict) -> int:
    """Counts number of correctly implemented bits.

    Args:
        formulas: Dictionary of circuit formulas

    Returns:
        Number of correctly implemented bits
    """
    i = 0
    while True:
        if not verify(i, formulas):
            break
        i += 1
    return i


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.

    Args:
        data: Processed input data

    Returns:
        Comma-separated string of swapped wires
    """
    if data is None:
        raise ValueError("Invalid input data")

    # Convert operations to formulas format
    formulas: Dict[str, Tuple[str, str, str]] = {}
    for op in data['operations']:
        formulas[op[3]] = (op[1], op[0], op[2])

    swaps: List[str] = []

    # Find 4 pairs of swapped wires
    for _ in range(4):
        baseline = progress(formulas)
        for x in formulas:
            for y in formulas:
                if x == y:
                    continue
                # Try swapping
                formulas[x], formulas[y] = formulas[y], formulas[x]
                if progress(formulas) > baseline:
                    break
                # Revert swap if no improvement
                formulas[x], formulas[y] = formulas[y], formulas[x]
            else:
                continue
            break
        swaps.extend([x, y])

    return ",".join(sorted(swaps))


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
