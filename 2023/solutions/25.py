"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

import os
import sys
from typing import Any, List

from pathlib import Path
import networkx as nx

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
    g: nx.Graph = nx.Graph()

    # Split raw_data into lines if it's not already a list
    lines: List[str] = raw_data.splitlines() if isinstance(
        raw_data, str) else raw_data

    for line in lines:
        if ":" not in line:
            continue
        left, right = line.strip().split(":")
        for node in right.strip().split():
            g.add_edge(left, node)

    if len(g.nodes()) == 0:
        raise ValueError("No valid connections found in input data")

    return g


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        return None

    data.remove_edges_from(nx.minimum_edge_cut(data))
    a, b = nx.connected_components(data)

    answer = len(a) * len(b)

    return answer


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'

    file_path: str = os.path.join(input_directory, infile)
    unprocessed_data = utils.read_input(file_path)
    input_data = process(unprocessed_data['data'])

    result_part_one = solve_part_one(input_data)
    if result_part_one is not None:
        print(f"Part One: {result_part_one}")
