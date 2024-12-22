"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""
from collections import defaultdict, deque
import os
import sys
from typing import Any, Deque, Dict, List, Optional, Tuple

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


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.

    For each code, we need to:
    1. Find path for first robot on number pad
    2. Find path for second robot on arrow pad to input first robot's commands
    3. Find path for human on arrow pad to input second robot's commands
    """
    number_pad: List[List[str]] = [
        ['7', '8', '9'],
        ['4', '5', '6'],
        ['1', '2', '3'],
        [' ', '0', 'A']
    ]

    arrow_pad: List[List[str]] = [
        [' ', '^', 'A'],
        ['<', 'v', '>'],
    ]

    # Get all possible transitions on arrow pad
    arrow_transitions = find_shortest_paths(arrow_pad)

    total_complexity: int = 0
    for code in data:
        print('code', code)
        # First robot path (on number pad)
        current_pos: str = 'A'
        first_robot_path: str = ""
        for target in code:
            paths = bfs(number_pad, current_pos, target)
            if not paths:
                continue
            first_robot_paths: List = []
            for shortest_path in paths:
                first_robot_path += moves_to_arrows(shortest_path) + 'A'
                first_robot_paths.append(first_robot_path)
            current_pos = target

        print('first_path', first_robot_path)

        # Second robot path (on arrow pad)
        second_robot_path: str = ""
        current_pos = 'A'
        for move in first_robot_path:
            if move == 'A':
                second_robot_path += 'A'
                continue
            paths = arrow_transitions[current_pos][move]
            if paths:
                second_robot_path += paths[0]
                current_pos = move

        print('second_path', second_robot_path)

        # Human path (on arrow pad)
        human_path: str = ""
        current_pos = 'A'
        for move in second_robot_path:
            if move == 'A':
                human_path += 'A'
                continue
            paths = arrow_transitions[current_pos][move]
            if paths:
                human_path += paths[0]
                current_pos = move

        # Calculate complexity using the length of the human input
        numeric_part: int = int(''.join(filter(str.isdigit, code)))
        complexity: int = len(human_path) * numeric_part
        total_complexity += complexity

        print('human_path', human_path)
        print('numeric_part',numeric_part)
        print('len', len(second_robot_path))
        print('')

    return total_complexity


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
