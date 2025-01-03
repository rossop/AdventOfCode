"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

from collections import defaultdict
import os
import sys
from typing import Any, DefaultDict, Dict, List, Set, Tuple

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
        tuple(line.strip().split('-')) for line in raw_data.splitlines()
    ]


def create_graph(
    connection_list: List[Tuple[str, str]]
) -> Dict[str,Set[str]]:
    """Create graph from list of node connections
    """
    connections: Dict[str,Set[str]] = defaultdict(set)
    for comp1, comp2 in connection_list:
        connections[comp1].add(comp2)
        connections[comp2].add(comp1)
    return connections


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        return None

    lan_graph: Dict[str,Set[str]] = create_graph(data)

    triangles: Set[Tuple[str, ...]] = set()

    for node, adjacent_nodes in lan_graph.items():
        neighbors = set(adjacent_nodes)  # Convert to set for fast lookup
        for neighbor in neighbors:
            if neighbor > node:  # Enforce lexicographical order
                # Find mutual neighbors
                common_neighbors = neighbors.intersection(lan_graph[neighbor])
                for mutual_neighbor in common_neighbors:
                    if mutual_neighbor > neighbor:  # Enforce further ordering
                        # Create a sorted tuple to represent the triangle
                        triangle: Tuple[str, ...] = tuple(
                            sorted(
                                [node, neighbor, mutual_neighbor]
                                   )
                        )
                        triangles.add(triangle)

    count: int = 0
    for triangle in triangles:
        if any(n.startswith('t') for n in triangle):
            count += 1

    return count


def bron_kerbosch(
    R: Set[str],
    P: Set[str],
    X: Set[str],
    graph: Dict[str, Set[str]],
    cliques: List[Set[str]]
):
    """Find all maximal cliques using the Bron-Kerbosch algorithm."""
    if not P and not X:
        cliques.append(R)  # R is a maximal clique
        return
    for v in list(P):
        bron_kerbosch(
            R.union({v}),
            P.intersection(graph[v]),
            X.intersection(graph[v]),
            graph,
            cliques
        )
        P.remove(v)
        X.add(v)


def find_largest_clique(
    graph: Dict[str, Set[str]],
) -> List[str]:
    """Find the largest clique in the graph.
    """
    cliques = []
    nodes = set(graph.keys())
    bron_kerbosch(set(), nodes, set(), graph, cliques)
    largest_clique: List[str] = max(cliques, key = len)
    return sorted(largest_clique)


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.
    """
    lan_graph: Dict[str,Set[str]] = create_graph(data)

    largest_clique: List[str] = find_largest_clique(lan_graph)

    return ",".join(largest_clique)


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
