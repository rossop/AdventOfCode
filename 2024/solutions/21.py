"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""
from collections import defaultdict, deque
import os
import sys
from typing import Any, Deque, Dict, List, Optional, Tuple

import heapq

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
    """Solves part one of the challenge."""
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

    def get_pad_value(pad: List[List[str]], pos: Tuple[int, int]) -> Optional[str]:
        """Get value at position if valid, None otherwise."""
        r, c = pos
        if 0 <= r < len(pad) and 0 <= c < len(pad[r]):
            return pad[r][c] if pad[r][c] != ' ' else None
        return None

    def apply_move(pos: Tuple[int, int], move: str) -> Tuple[int, int]:
        """Apply move to position."""
        r, c = pos
        if move == 'A':
            return (r, c)
        elif move == '<':
            return (r, c-1)
        elif move == '^':
            return (r-1, c)
        elif move == '>':
            return (r, c+1)
        elif move == 'v':
            return (r+1, c)
        return pos

    def get_arrow_moves(from_pos: Tuple[int, int], to_move: str) -> int:
        """Calculate number of moves needed on arrow pad to input a move."""
        if to_move == 'A':
            return 1  # Just need to press A

        # Find position of target move on arrow pad
        target_pos = None
        for r in range(len(arrow_pad)):
            for c in range(len(arrow_pad[r])):
                if arrow_pad[r][c] == to_move:
                    target_pos = (r, c)
                    break
            if target_pos:
                break

        # Calculate Manhattan distance plus 1 for the final 'A' press
        if target_pos:
            return (abs(from_pos[0] - target_pos[0]) +
                    abs(from_pos[1] - target_pos[1]) + 1)
        return float('inf')

    total_complexity: int = 0
    for code_list in data:
        code = ''.join(code_list)  # Convert list to string
        # Start with robot at 'A' position (3,2) on number pad
        # and at (0,2) on arrow pad (where 'A' is)
        start = (0, (3, 2), (0, 2), '')  # (cost, num_pos, arrow_pos, output)
        queue = [(0, start)]
        seen = set()

        while queue:
            cost, (_, num_pos, arrow_pos, output) = heapq.heappop(queue)

            if output == code:
                numeric_part = int(''.join(filter(str.isdigit, code)))
                total_complexity += cost * numeric_part
                break

            if not code.startswith(output):
                continue

            if get_pad_value(number_pad, num_pos) is None:
                continue

            state = (num_pos, arrow_pos, output)
            if state in seen:
                continue
            seen.add(state)

            for move in ['^', '<', 'v', '>', 'A']:
                new_num_pos = apply_move(num_pos, move)
                new_output = output

                if move == 'A':
                    pad_value = get_pad_value(number_pad, num_pos)
                    if pad_value:
                        new_output = output + pad_value

                # Calculate cost of moving on arrow pad to input this move
                move_cost = get_arrow_moves(arrow_pos, move)
                # Find new arrow pad position after inputting move
                new_arrow_pos = arrow_pos
                if move != 'A':
                    for r in range(len(arrow_pad)):
                        for c in range(len(arrow_pad[r])):
                            if arrow_pad[r][c] == move:
                                new_arrow_pos = (r, c)
                                break

                heapq.heappush(queue,
                               (cost + move_cost,
                                (0, new_num_pos, new_arrow_pos, new_output)))

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
