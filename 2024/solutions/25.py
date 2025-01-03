"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

from collections import Counter, defaultdict
from itertools import product
import os
from pprint import pprint
import sys
from typing import Any, Dict, List, Set, Tuple

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
    schematics = raw_data.split('\n\n')
    def parse(schem):
        rows: List[str] = schem.splitlines()
        if all(val == '#' for val in rows[0]):
             schematic_type: str = 'lock'
        elif all(val == '#' for val in rows[-1]):
             schematic_type: str = 'key'
        else:
            schematic_type: str = 'error'

        column_counters: Dict[int, int] = defaultdict(lambda: -1)
        for row in rows:
            for col_index, char in enumerate(row):
                if char =='#':
                    column_counters[col_index] += 1

        # Extract the count of '#' in each column
        return schematic_type, column_counters

    return list(map(parse,schematics))


def key_lock_check(key: Dict[int, int], lock: Dict[int, int]) -> bool:
    """Check if key opens lock
    """
    ans: bool = True
    for lk, lv in lock.items():
        if lk in key.keys():
            ans =  ans and (lv + key[lk] <= 5)

    return ans


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        return None

    keys : List[Dict[int, int]] = [tup[1] for tup in data if tup[0] == 'key']
    locks : List[Dict[int, int]] = [tup[1] for tup in data if tup[0] == 'lock']

    part_one_answer = sum(
        [
            key_lock_check(key, lock) for key, lock in product(keys, locks)
        ]
    )

    return part_one_answer


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'

    file_path: str = os.path.join(input_directory, infile)
    unprocessed_data = utils.read_input(file_path)
    input_data = process(unprocessed_data['data'])

    result_part_one = solve_part_one(input_data)
    if result_part_one is not None:
        print(f"Part One: {result_part_one}")

