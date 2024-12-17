"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
import sys
import re
from typing import Any, Dict, List, Tuple, NewType, Optional, Set
import copy

Claw = NewType('Claw', Dict[str, Tuple[int, int]])


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
    list_of_claws: List[str] = raw_data.strip().split('\n\n')
    claws: List[Claw] = []
    template_claw: Claw = {
        'A': (0, 0),
        'B': (0, 0),
        'Target': (0, 0),
    }
    # commet goes here
    # Regex patterns
    button_pattern = r'Button\s+([A-Z]):\s+X\+(\d+),\s+Y\+(\d+)'
    prize_pattern = r'Prize:\s+X=(\d+),\s+Y=(\d+)'
    for claw_str in list_of_claws:
        claw = copy.deepcopy(template_claw)

        # Find all button matches
        for match in re.finditer(button_pattern, claw_str):
            letter = match.group(1)
            x_val = int(match.group(2))
            y_val = int(match.group(3))
            claw[letter] = (x_val, y_val)

        # Find prize match
        prize_match = re.search(prize_pattern, claw_str)
        if prize_match:
            x_val = int(prize_match.group(1))
            y_val = int(prize_match.group(2))
            claw['Target'] = (x_val, y_val)

        claws.append(claw)

    return claws


def extend_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Returns gcd, x, y such that gcd = a * x + b * y.
    """
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extend_gcd(b, a % b)
    x: int = y1
    y: int = x1 - (a // b) * y1
    return g, x, y


def solve_diophantine(
    A: int,
    B: int,
    Target: int
) -> Optional[List[Tuple[int, int]]]:
    """Finds all integer solutions for A * x + B * y = Target.
    """
    g, x, y = extend_gcd(A, B)
    if Target % g != 0:
        # No solution
        return None

    scale: int = Target // g
    x0: int = x * scale
    y0: int = y * scale

    # Generate all integer solutions within a practial range:
    solutions: List[Tuple[int, int]] = []
    step_a: int = B // g
    step_b: int = A // g

    for k in range(-10000, 10001):
        a = x0 + k * step_a
        b = y0 - k * step_b
        if a >= 0 and b >= 0:
            solutions.append((a, b))

    return solutions


def minimize_cost(
    solutions: Set[Tuple[int, int]],
    cost_a: int = 3,
    cost_b: int = 1
):
    """Finds the solution witht minimum cost."""
    return min(solutions, key=lambda ab: ab[0] * cost_a + ab[1] * cost_b)


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.

    Args:
        data (Any): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """
    cost: Dict[str, int] = {"A": 3, "B": 1}
    total_cost: int = 0

    for machine in data:
        XA, YA = machine['A']
        XB, YB = machine['B']
        PX, PY = machine['Target']

        # Solve for X
        x_solutions = solve_diophantine(XA, XB, PX)
        if x_solutions is None:
            continue

        # Solve for Y
        y_solutions = solve_diophantine(YA, YB, PY)
        if y_solutions is None:
            continue

        # Find common solutions for X and Y
        common_solutions = set(x_solutions) & set(y_solutions)
        if not common_solutions:
            continue

        # Calculate minimum cost for this machine
        best_solution = minimize_cost(common_solutions, cost["A"], cost["B"])
        machine_cost = best_solution[0] * cost["A"] + \
            best_solution[1] * cost["B"]
        total_cost += machine_cost

    return total_cost


def solve_large_diophantine(A: int, B: int, Target: int) -> Optional[List[Tuple[int, int]]]:
    """Finds integer solutions for A * x + B * y = Target efficiently for large numbers.

    Args:
        A (int): Coefficient of x
        B (int): Coefficient of y
        Target (int): Target sum

    Returns:
        Optional[List[Tuple[int, int]]]: Minimal non-negative solution or None
    """
    g, x, y = extend_gcd(A, B)
    if Target % g != 0:
        return None

    # Get initial solution
    scale: int = Target // g
    x0: int = x * scale
    y0: int = y * scale

    # Calculate steps
    step_x: int = B // g
    step_y: int = A // g

    # Find k that makes both x and y non-negative
    # For x: x0 + k * step_x >= 0
    # For y: y0 - k * step_y >= 0
    k_min_x: int = (-x0 + step_x - 1) // step_x if x0 < 0 else 0
    k_max_y: int = y0 // step_y if y0 > 0 else 0
    k: int = k_min_x

    while k <= k_max_y + 1000:  # Add some margin for safety
        x1: int = x0 + k * step_x
        y1: int = y0 - k * step_y

        if x1 >= 0 and y1 >= 0:
            # Use modular arithmetic for verification to avoid overflow
            if (A * x1) % Target + (B * y1) % Target == Target % Target:
                return [(x1, y1)]
        k += 1

    return None


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.
®
    Args:
        data (List[str]): The input data for the challenge.

    Returns:
        int: Total minimum cost for all solvable machines.
    """
    cost: Dict[str, int] = {"A": 3, "B": 1}
    total_cost: int = 0
    modifier: int = 10000000000000

    # Update data for part two
    machines_pt2: List[Claw] = []
    for machine in data:
        new_machine = copy.deepcopy(machine)
        new_target_x = machine['Target'][0] + modifier
        new_target_y = machine['Target'][1] + modifier
        new_machine['Target'] = (new_target_x, new_target_y)
        machines_pt2.append(new_machine)

    for idx, machine in enumerate(machines_pt2, 1):
        XA, YA = machine['A']
        XB, YB = machine['B']
        PX, PY = machine['Target']

        print(f"\nAnalyzing machine {idx}:")
        print(f"Button A: X+{XA}, Y+{YA}")
        print(f"Button B: X+{XB}, Y+{YB}")
        print(f"Target: X={PX}, Y={PY}")

        try:
            # Solve for X and Y
            x_solutions = solve_large_diophantine(XA, XB, PX)
            if x_solutions is None:
                print(f"No X solution for machine {idx}")
                continue

            y_solutions = solve_large_diophantine(YA, YB, PY)
            if y_solutions is None:
                print(f"No Y solution for machine {idx}")
                continue

            # Find common solutions
            common_solutions = set(x_solutions) & set(y_solutions)
            if not common_solutions:
                print(f"No common solution for machine {idx}")
                continue

            # Calculate cost for this machine
            best_solution = minimize_cost(
                common_solutions, cost["A"], cost["B"])
            machine_cost = best_solution[0] * \
                cost["A"] + best_solution[1] * cost["B"]
            print(
                f"Machine {idx} solvable with {best_solution} costing {machine_cost}")
            total_cost += machine_cost

        except Exception as e:
            print(f"Error processing machine {idx}: {str(e)}")
            continue

    return total_cost


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
