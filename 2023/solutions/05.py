"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

import utils
from collections import deque
import os
from pprint import pprint
import sys
from typing import Any, Deque, Dict, List, Tuple, Optional, TypeAlias, Union
from typing import NewType

from pathlib import Path

# Add the parent directory of 'utils' to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

Value = NewType('Value', int)
MapEntry: TypeAlias = Tuple[int, int, int]
SeedMap: TypeAlias = List[MapEntry]
ProcessedData: TypeAlias = Dict[str, Union[List[int], List[MapEntry]]]


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
    sections: List[str] = raw_data.strip().split("\n\n")

    def parse_section(section):
        """Separate key and values
        """
        header, *lines = section.split("\n")
        key: str = header.split(":")[0].strip().replace(
            " map", "")  # Clean key
        if key == "seeds":  # Handle seeds section differently
            values = [*map(int, header.split(":")[1].strip().split())]
        else:
            values: List[Tuple[int, ...] | int] = list(
                map(
                    lambda x: tuple(
                        map(
                            int,
                            x.split()
                        )
                    ),
                    lines
                )
            )
        return key, values

    return dict(map(parse_section, sections))


def map_single_value(
    value: Value,
    current_map: MapEntry
) -> Optional[Value]:
    """Map a single value using the current map without generating all ranges.
    """
    dest_start, source_start, range_len = current_map
    if source_start <= value < source_start + range_len:
        offset: Value = value - source_start
        return dest_start + offset
    return None


def map_values(
    value: Value,
    current_maps: SeedMap
) -> List[Value]:
    """Evaluate all mappings for a value and return a list of valid mapped
    values.
    """
    mapped_value: Optional[Value] = None

    # Try all mappings until we find one that works
    for mapping in current_maps:
        mapped = map_single_value(value, mapping)
        if mapped is not None:
            mapped_value = mapped
            break

    # If no mapping found, use original value
    return [mapped_value if mapped_value is not None else value]


def iterative_map(
    seeds: List[Value],
    maps: Dict,
    steps: List[str]
) -> List[Value]:
    """
    Iteratively maps values though alls tages of maps a queue
    """
    q: Deque = deque([(seed, 0) for seed in seeds])
    results: List[Value] = []

    while q:
        value, step_index = q.popleft()

        if step_index >= len(steps):
            results.append(value)
            continue

        current_step = steps[step_index]
        current_map = maps[current_step]

        mapped_values = map_values(value, current_map)

        for mapped_val in mapped_values:
            q.append((mapped_val, step_index + 1))

    return results


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        return None

    seeds = data['seeds']
    steps = [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]

    results: List[Value] = iterative_map(seeds, data, steps)

    return min(results) if results else None


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.
    """
    if data is None:
        return None

    # Initialize seed ranges
    seeds: List[Tuple[int, int]] = []
    raw_seeds: List[int] = data['seeds']
    for i in range(0, len(raw_seeds), 2):
        seeds.append((raw_seeds[i], raw_seeds[i] + raw_seeds[i + 1]))

    # Define processing steps
    steps: List[str] = [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]

    # Process each mapping block
    for step in steps:
        new_ranges: List[Tuple[int, int]] = []
        current_maps: List[Tuple[int, ...]] = data[step]

        while seeds:
            start, end = seeds.pop()
            for dest_start, source_start, length in current_maps:
                overlap_start: int = max(start, source_start)
                overlap_end: int = min(end, source_start + length)

                if overlap_start < overlap_end:
                    new_ranges.append((
                        overlap_start - source_start + dest_start,
                        overlap_end - source_start + dest_start
                    ))

                    if overlap_start > start:
                        seeds.append((start, overlap_start))
                    if end > overlap_end:
                        seeds.append((overlap_end, end))
                    break
            else:
                new_ranges.append((start, end))

        seeds = new_ranges

    return min(start for start, _ in seeds) if seeds else None


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
