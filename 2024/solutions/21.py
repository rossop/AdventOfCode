"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""
from collections import defaultdict, deque
import os
import sys
from typing import Any, Deque, Dict, List, Optional, Tuple
from functools import cache

from itertools import product

from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import utils  # noqa: E402, F401

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
    return [list(line) for line in raw_data.splitlines()]


def map_valus_to_pos(
    grid: List[List[str]],
) -> Dict[str, Tuple[int, int]]:
    """Given a grid of unique values, create a map of value to position as
    tuple
    """
    rows: int = len(grid)
    cols: int = len(grid[0])

    grid_map: Dict[str, Tuple[int, int]] = {}

    for r in range(rows):
        for c in range(cols):
            grid_map[grid[r][c]] = (r, c)

    return grid_map


def bfs(
    grid: List[List[str]],
    start_value: str,
    end_value: str
) -> Optional[Optional[List[List[Tuple[int, int]]]]]:
    """Breadth first search of keypad
    """
    rows: int = len(grid)
    cols: int = len(grid[0])

    directions: List[Tuple[int, int]] = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
    ]

    grid_map: Dict[str, Tuple[int, int]] = map_valus_to_pos(grid)
    start: Optional[Tuple[int, int]] = grid_map.get(start_value, None)
    end: Optional[Tuple[int, int]] = grid_map.get(end_value, None)

    if start is None or end is None:
        return None

    queue: Deque[Tuple[int, int, List[Tuple[int, int]]]] = deque(
        [(start[0], start[1], [start])]  # x, y, path
    )
    distance: Dict[Tuple[int, int], int] = {}
    paths = defaultdict(list)
    distance[start] = 0
    paths[start].append([start])

    while queue:
        x, y, path = queue.popleft()
        # Custom logic

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if (
                0 <= nx < rows and
                0 <= ny < cols and
                grid[nx][ny] in '1234567890A<>^v'
            ):
                new_distance = distance[(x, y)] + 1

                if (
                    (nx, ny) not in distance or
                    new_distance == distance[(nx, ny)]
                ):
                    distance[(nx, ny)] = new_distance
                    paths[(nx, ny)].extend(
                        [p + [(nx, ny)] for p in paths[(x, y)]]
                    )

                    if new_distance == distance[(nx, ny)]:
                        queue.append((nx, ny, path + [(nx, ny)]))

    return paths.get(end, [])


def moves_to_arrows(moves: List[Tuple[int, int]]) -> str:
    """Given a list of positions, return the necessary arrow_pad bottons to
    move between them.
    """
    direction_map: Dict[Tuple[int, int], str] = {
        (0, 1): '>',
        (1, 0): 'v',
        (0, -1): '<',
        (-1, 0): '^',
    }

    move_path: List[str] = []
    for i in range(1, len(moves)):
        diff: Tuple[int, int] = (
            moves[i][0] - moves[i-1][0],
            moves[i][1] - moves[i-1][1]
        )
        move: str = direction_map[diff]
        move_path.append(move)

    return "".join(move_path)


def find_shortest_paths(
    grid: List[List[str]]
) -> Dict[str, Dict[str, List[str]]]:
    """Find the shortest path between two arrows on keypad
    """
    directions: List[Tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    # Extract positions of each button
    positions = {}
    for i, row in enumerate(grid):
        for j, button in enumerate(row):
            if button != ' ':
                positions[button] = (i, j)

    def bfs_shortest_paths(
        start_pos: Tuple[int, int],
        end_pos: Tuple[int, int]
    ) -> List[List[Tuple[int, int]]]:
        """Perform BFS to find all shortest paths between two positions."""
        queue = deque([[start_pos]])
        shortest_paths = []
        shortest_length = float('inf')

        while queue:
            path = queue.popleft()
            current = path[-1]

            # If we reach the destination
            if current == end_pos:
                if len(path) < shortest_length:
                    shortest_paths = [path]
                    shortest_length = len(path)
                elif len(path) == shortest_length:
                    shortest_paths.append(path)
                continue

            # If the current path exceeds the known shortest length, skip
            if len(path) > shortest_length:
                continue

            # Explore neighbors
            for direction in directions:
                new_pos = (
                    current[0] + direction[0],
                    current[1] + direction[1]
                )
                if (
                    0 <= new_pos[0] < len(grid) and
                    0 <= new_pos[1] < len(grid[0]) and
                    grid[new_pos[0]][new_pos[1]] != ' '
                ):
                    if new_pos not in path:  # Avoid cycles
                        queue.append(path + [new_pos])

        return shortest_paths

    # Create the dictionary of transitions
    transitions = {}
    for start, start_pos in positions.items():
        transitions[start] = {}
        for end, end_pos in positions.items():
            if start != end:
                # Find all shortest paths between start_pos and end_pos
                shortest_paths = bfs_shortest_paths(start_pos, end_pos)
                # Convert paths to arrow strings
                arrow_paths = [
                    moves_to_arrows(path) for path in shortest_paths
                ]
                transitions[start][end] = list(
                    map(lambda x: x + 'A', arrow_paths)
                )
            else:
                transitions[start][end] = ['A']

    return transitions


def compute_sequences(
    keypad: List[List[Optional[str]]]
) -> Dict[Tuple[str, str], List[str]]:
    """Compute all possible sequences between keypad positions.

    Args:
        keypad: A 2D grid representing the keypad layout.

    Returns:
        Dict mapping (start, end) positions to possible movement sequences.
    """
    positions: Dict[str, Tuple[int, int]] = {}
    for r, row in enumerate(keypad):
        for c, val in enumerate(row):
            if val is not None:
                positions[val] = (r, c)

    sequences: Dict[Tuple[str, str], List[str]] = {}
    directions: List[Tuple[int, int, str]] = [
        (-1, 0, "^"), (1, 0, "v"), (0, -1, "<"), (0, 1, ">")
    ]

    for start in positions.keys():
        for end in positions:
            if start == end:
                sequences[(start, end)] = ["A"]
                continue

            possibilities: List[str] = []
            queue: Deque[Tuple[Tuple[int, int], str]] = deque(
                [(positions[start], "")]
            )
            optimal_len: float = float("inf")

            while queue:
                (row, col), moves = queue.popleft()

                for nrow, ncol, move in [
                    (row + dr, col + dc, m) for (dr, dc, m) in directions
                ]:
                    if not (
                        0 <= nrow < len(keypad) and
                        0 <= ncol < len(keypad[0])
                    ):
                        continue
                    if keypad[nrow][ncol] is None:
                        continue

                    if keypad[nrow][ncol] == end:
                        if optimal_len < len(moves) + 1:
                            break
                        optimal_len = len(moves) + 1
                        possibilities.append(moves + move + "A")
                    else:
                        queue.append(((nrow, ncol), moves + move))
                else:
                    continue
                break

            sequences[(start, end)] = possibilities

    return sequences


def solve_sequence(
    string: str,
    sequences: Dict[Tuple[str, str], List[str]]
) -> List[str]:
    """Generate all possible movement sequences for a given input string.

    Args:
        string: Input sequence of buttons to press.
        sequences: Pre-computed sequences between positions.

    Returns:
        List of possible movement sequences.
    """
    options: List[List[str]] = [
        sequences[(x, y)] for x, y in zip("A" + string, string)
    ]
    return ["".join(x) for x in product(*options)]


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.

    For each code, we need to:
    1. Find path for first robot on number pad
    2. Find path for second robot on arrow pad to input first robot's commands
    3. Find path for human on arrow pad to input second robot's commands
    """
    number_pad: List[List[Optional[str]]] = [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        [None, "0", "A"]
    ]
    arrow_pad: List[List[Optional[str]]] = [
        [None, "^", "A"],
        ["<", "v", ">"]
    ]

    # Compute sequences for both pads
    num_sequences: Dict[Tuple[str, str], List[str]] = compute_sequences(
        number_pad
    )
    dir_sequences: Dict[Tuple[str, str], List[str]] = compute_sequences(
        arrow_pad
    )
    dir_lengths: Dict[Tuple[str, str], int] = {
        key: len(value[0]) for key, value in dir_sequences.items()
    }

    @cache
    def compute_length(seq: str, depth: int = 25) -> int:
        """Recursively compute the minimum length of commands needed.

        Args:
            seq: The sequence to compute length for
            depth: Current recursion depth

        Returns:
            Minimum length of commands needed
        """
        if depth == 1:
            return sum(dir_lengths[(x, y)] for x, y in zip("A" + seq, seq))

        length: int = 0
        for x, y in zip("A" + seq, seq):
            length += min(
                compute_length(subseq, depth - 1)
                for subseq in dir_sequences[(x, y)]
            )
        return length

    total: int = 0
    for line in data:
        code: str = "".join(line)
        inputs: List[str] = solve_sequence(code, num_sequences)
        length: int = min(map(compute_length, inputs))
        total += length * int(code[:-1])

    return total


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.
    """
    # TODO: Implement the solution for part two
    return None


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
