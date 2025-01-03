"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

import os
import sys
from typing import Any, Dict, List, Set

from collections import deque

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
    return [
        tuple(
            map(
                lambda x: tuple(
                    map(
                        int,
                        x.split(',')
                    )
                ),
                line.split('~')
            )
        ) for line in raw_data.splitlines()
    ]


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        return None
    # Convert parsed input into a list of bricks represented by their bounding
    # box coordinates.
    # Each brick is stored as [x_min, y_min, z_min, x_max, y_max, z_max].
    # This representation is compact and efficient for processing.
    bricks = []
    for (start, end) in data:
        x1, y1, z1 = start
        x2, y2, z2 = end
        # Ensure that each dimension is stored with min and max values,
        # regardless of input order.
        bricks.append(
            [
                min(x1, x2),
                min(y1, y2),
                min(z1, z2),
                max(x1, x2),
                max(y1, y2),
                max(z1, z2)
            ]
        )
    # Sort bricks by their starting z-coordinate (z_min).
    # This ensures we process lower bricks first, which is important for
    # simulating falling and support.
    bricks.sort(key=lambda brick: brick[2])

    # Function to check if two bricks overlap in the x and y dimensions.
    # Overlap in x and y is necessary for one brick to physically support another.
    def overlaps(a, b):
        return (
            max(a[0], b[0]) <= min(a[3], b[3]) and
            max(a[1], b[1]) <= min(a[4], b[4])
        )
    # Adjust the positions of bricks to simulate their settling after falling.
    # Bricks "fall" until they reach either the ground (z=1) or are supported
    # by another brick.
    for index, brick in enumerate(bricks):
        max_z = 1  # Start with the assumption that the brick falls to the ground.
        for check in bricks[:index]:  # Only consider bricks that are already settled.
            if overlaps(brick, check):  # Check if this brick overlaps another in x and y dimensions.
                max_z = max(max_z, check[5] + 1)  # Adjust max_z to the top of the supporting brick.
        # Update the brick's z_min and z_max to reflect its settled position.
        brick[5] -= brick[2] - max_z  # Adjust the top z-coordinate.
        brick[2] = max_z              # Adjust the bottom z-coordinate.

    # Re-sort bricks by their starting z-coordinate after settling adjustments.
    # This ensures the order remains consistent for further calculations.
    bricks.sort(key=lambda brick: brick[2])

    # Create dictionaries to track support relationships between bricks:
    # - `k_supports_v`: Maps each brick (k) to the set of bricks (v) it directly supports.
    # - `v_supports_k`: Maps each brick (v) to the set of bricks (k) that directly support it.
    k_supports_v = {i: set() for i in range(len(bricks))}
    v_supports_k = {i: set() for i in range(len(bricks))}

    # Populate the support relationships.
    for j, upper in enumerate(bricks):  # Iterate over each brick (potentially supported brick).
        for i, lower in enumerate(bricks[:j]):  # Check bricks below it (potential supports).
            # A brick is supported if:
            # - It overlaps in x and y dimensions.
            # - Its z_min is exactly 1 unit above the z_max of the supporting brick.
            if overlaps(lower, upper) and upper[2] == lower[5] + 1:
                k_supports_v[i].add(j)  # Add brick j as supported by brick i.
                v_supports_k[j].add(i)  # Add brick i as a support for brick j.

    # Calculate the total number of "safe" bricks.
    # A brick is "safe" if removing it does not cause any supported bricks to lose all their supports.
    total = 0

    for i in range(len(bricks)):  # Iterate over all bricks.
        # Check if all bricks directly supported by this brick have at least 2 other supports.
        if all(len(v_supports_k[j]) >= 2 for j in k_supports_v[i]):
            total += 1  # This brick is safe to disintegrate.

    # Output the total number of safe bricks.
    return total


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge."""
    if data is None:
        return None

    # Convert parsed input into a list of bricks represented by their bounding box coordinates
    bricks = []
    for (start, end) in data:
        x1, y1, z1 = start
        x2, y2, z2 = end
        bricks.append(
            [
                min(x1, x2),
                min(y1, y2),
                min(z1, z2),
                max(x1, x2),
                max(y1, y2),
                max(z1, z2),
            ]
        )

    # Sort bricks by starting z-coordinate (z_min)
    bricks.sort(key=lambda brick: brick[2])

    # Helper function to check if two bricks overlap in x and y dimensions
    def overlaps(a, b):
        return max(a[0], b[0]) <= min(a[3], b[3]) and max(a[1], b[1]) <= min(a[4], b[4])

    # Adjust the positions of bricks to simulate their settling after falling
    for index, brick in enumerate(bricks):
        max_z = 1  # Start with the assumption that the brick falls to the ground
        for check in bricks[:index]:  # Only consider bricks that are already settled
            if overlaps(brick, check):  # Check if this brick overlaps another in x and y dimensions
                max_z = max(max_z, check[5] + 1)  # Adjust max_z to the top of the supporting brick
        # Update the brick's z_min and z_max to reflect its settled position
        brick[5] -= brick[2] - max_z  # Adjust the top z-coordinate
        brick[2] = max_z              # Adjust the bottom z-coordinate

    # Re-sort bricks by starting z-coordinate after adjustment
    bricks.sort(key=lambda brick: brick[2])

    # Build support relationships
    k_supports_v = {i: set() for i in range(len(bricks))}
    v_supports_k = {i: set() for i in range(len(bricks))}

    for j, upper in enumerate(bricks):
        for i, lower in enumerate(bricks[:j]):
            if overlaps(lower, upper) and upper[2] == lower[5] + 1:
                k_supports_v[i].add(j)  # Add brick j as supported by brick i
                v_supports_k[j].add(i)  # Add brick i as a support for brick j

    # Calculate the total number of bricks that would fall for each disintegration
    total = 0

    for i in range(len(bricks)):
        # Use a deque to track bricks that would fall in a chain reaction
        q = deque(j for j in k_supports_v[i] if len(v_supports_k[j]) == 1)
        falling = set(q)
        falling.add(i)  # Add the initial disintegrated brick to the set of falling bricks

        # Process the chain reaction
        while q:
            j = q.popleft()
            for k in k_supports_v[j] - falling:
                if v_supports_k[k] <= falling:  # Check if all supports of brick k are in falling
                    q.append(k)
                    falling.add(k)

        # Add the number of bricks that fell, minus the initially disintegrated brick
        total += len(falling) - 1

    return total


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
