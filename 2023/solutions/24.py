"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""
import os
import sys
from typing import Any, Dict, List, Set, Tuple
import sympy

from pathlib import Path
import copy

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


class Hailstone:
    """Hailstone class representitng state and velocity of the stones"""

    def __init__(self, sx, sy, sz, vx, vy, vz):
        self.sx = sx  # Starting x-coordinate
        self.sy = sy  # Starting y-coordinate
        self.sz = sz  # Starting z-coordinate (ignored for 2D calculations)
        self.vx = vx  # Velocity in x
        self.vy = vy  # Velocity in y
        self.vz = vz  # Velocity in z (ignored for 2D calculations)

        # Line coefficients for 2D motion in the form ax + by + c = 0
        self.a = vy
        self.b = -vx
        self.c = vy * sx - vx * sy

    def __repr__(self):
        return f"Hailstone(a={self.a}, b={self.b}, c={self.c})"


def process(raw_data):
    """Parses raw input data into Hailstone objects."""
    return [
        Hailstone(
            *map(
                int, line.replace("@", ",").split(",")
            )
        ) for line in raw_data.strip().splitlines()
    ]


def find_intersections(hailstones, test_area):
    """Finds intersections between hailstones within a given test area."""
    total = 0

    for i, hs1 in enumerate(hailstones):
        for hs2 in hailstones[:i]:  # Avoid duplicate pairs
            a1, b1, c1 = hs1.a, hs1.b, hs1.c
            a2, b2, c2 = hs2.a, hs2.b, hs2.c

            # Check if lines are parallel (a1/b1 == a2/b2)
            if a1 * b2 == b1 * a2:
                continue  # Lines are parallel, no intersection

            # Calculate intersection point (x, y)
            x = (c1 * b2 - c2 * b1) / (a1 * b2 - a2 * b1)
            y = (c2 * a1 - c1 * a2) / (a1 * b2 - a2 * b1)

            # Check if intersection is within the test area
            if test_area[0] <= x <= test_area[1] and test_area[2] <= y <= test_area[3]:
                # Check if both hailstones would reach the intersection point
                if all((x - hs.sx) * hs.vx >= 0 and (y - hs.sy) * hs.vy >= 0 for hs in (hs1, hs2)):
                    total += 1

    return total


def solve_part_one(data: Any):
    """Solves part one of the challenge."""
    test_area = (200000000000000, 400000000000000,
                 200000000000000, 400000000000000)
    hailstones = copy.deepcopy(data)
    print(hailstones)
    return find_intersections(hailstones, test_area)


def solve_part_two(data: Any):
    """Solves part one of the challenge."""
    hailstones = copy.deepcopy(data)
    xr, yr, zr, vxr, vyr, vzr = sympy.symbols("xr yr zr vxr vyr vzr")
    equations = []

    for i, hs in enumerate(hailstones):
        sx, sy, sz = hs.sx, hs.sy, hs.sz
        vx, vy, vz = hs.vx, hs.vy, hs.vz

        equations.append((xr - sx) * (vy - vyr) - (yr - sy) * (vx - vxr))
        equations.append((yr - sy) * (vz - vzr) - (zr - sz) * (vy - vyr))

        if i < 2:
            continue

        solutions = sympy.solve(
            equations, [xr, yr, zr, vxr, vyr, vzr], dict=True)
        integer_solutions = [
            soln for soln in solutions
            if all(val.is_integer for val in soln.values())
        ]

        if len(integer_solutions) == 1:
            answer = integer_solutions[0]
            return answer[xr] + answer[yr] + answer[zr]

    raise ValueError("No valid integer solution found")


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
