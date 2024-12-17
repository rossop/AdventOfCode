"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
import sys
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import cv2
from collections import deque


input_directory: str = os.path.join(
    os.path.dirname(
        os.path.abspath(
            os.path.dirname(__file__)
        )
    ), 'in'
)


output_directory: str = os.path.join(
    os.path.dirname(
        os.path.abspath(
            os.path.dirname(__file__)
        )
    ), 'out', 'day15'
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


def enlanrge_warehouse(raw_board: str) -> List[List[str]]:
    """Enlarge warehouse to account for robot and box pushing.
    """
    transform: Dict[str, List[str]] = {
        'O': ['[', ']'],
        '#': ['#', '#'],
        '.': ['.', '.'],
        '@': ['@', '.']
    }

    enlarged_board: List[List[str]] = []
    for line in raw_board.splitlines():
        enlarged_line: List[str] = []
        for char in line:
            enlarged_line.extend(transform.get(char, [char, char]))
        enlarged_board.append(enlarged_line)

    return enlarged_board


def process(raw_data: str) -> Any:
    """Processes the input data.
    """
    raw_board, raw_instructions = raw_data.split('\n\n')
    board: List[List[str]] = [
        [
            c for c in line
        ] for line in raw_board.splitlines()
    ]
    instructions: List[str] = [
        c for line in raw_instructions.splitlines() for c in line
    ]

    data: Dict[str, List] = {
        "board": board,
        "instructions": instructions,
        "enlarged_board": enlanrge_warehouse(raw_board)
    }

    return data


def can_move(
    instruction: str,
    board: List[List[str]],
    position: Tuple[int, int]
) -> bool:
    """Check if a piece can be moved in the specified direction.
    """
    moves: Dict[str, Tuple[int, int]] = {
        "^": (-1, 0),
        "<": (0, -1),
        "v": (1, 0),
        ">": (0, 1)
    }

    next_pos: Tuple[int, int] = (
        position[0] + moves[instruction][0],
        position[1] + moves[instruction][1]
    )

    # Wall - cannot move
    if board[next_pos[0]][next_pos[1]] == '#':
        return False

    # Empty space - can move
    if board[next_pos[0]][next_pos[1]] == '.':
        return True

    # Handle box movement
    # Check for both single and multi-character boxes
    if board[next_pos[0]][next_pos[1]] in ['O', '[', ']', '@']:
        # Vertical movement
        if instruction in ['^', 'v']:
            # Box with '[' at the start
            if board[next_pos[0]][next_pos[1]] == '[':
                # Check both halves of the box can move vertically
                left_move: bool = can_move(instruction, board, next_pos)
                right_move: bool = can_move(
                    instruction, board, (next_pos[0], next_pos[1]+1))
                return left_move and right_move

            # Box with ']' at the end
            elif board[next_pos[0]][next_pos[1]] == ']':
                # Check both halves of the box can move vertically
                left_move: bool = can_move(
                    instruction, board, (next_pos[0], next_pos[1]-1))
                right_move: bool = can_move(instruction, board, next_pos)
                return left_move and right_move

            # Single character box or robot
            else:
                return can_move(instruction, board, next_pos)

        # Horizontal movement
        elif instruction == '>':
            # Box with '[' at the start
            if board[next_pos[0]][next_pos[1]] == '[':
                # Other half of the box can move horizontally
                right_move: bool = can_move(
                    instruction, board, (next_pos[0], next_pos[1] + 1))
                return right_move

        elif instruction == '<':
            # Box with ']' at the end
            if board[next_pos[0]][next_pos[1]] == ']':
                # Check both halves of the box can move horizontally
                left_move: bool = can_move(
                    instruction, board, (next_pos[0], next_pos[1] - 1))
                return left_move

        # Single character box or robot
        return can_move(instruction, board, next_pos)

    return False


def move_with_bfs(
    instruction: str,
    board: List[List[str]],
    position: Tuple[int, int]
) -> Tuple[List[List[str]], Tuple[int, int]]:
    """Move pieces using BFS to handle connected components.

    Args:
        instruction (str): Direction to move (^, v, <, >)
        board (List[List[str]]): Current board state
        position (Tuple[int, int]): Current position (r,c)

    Returns:
        Tuple[List[List[str]], Tuple[int, int]]: Updated board and new position
    """
    moves: Dict[str, Tuple[int, int]] = {
        "^": (-1, 0),
        ">": (0, 1),
        "v": (1, 0),
        "<": (0, -1)
    }

    r, c = position
    dr, dc = moves[instruction]

    # Check if next position is wall
    if board[r + dr][c + dc] == '#':
        return board, position

    # If next position is empty, just move
    if board[r + dr][c + dc] == '.':
        board[r + dr][c + dc] = '@'
        board[r][c] = '.'
        return board, (r + dr, c + dc)

    # If we hit a box or part of box, do BFS
    if board[r + dr][c + dc] in ['[', ']', 'O']:
        queue: deque = deque([(r, c)])
        seen: set = set()
        can_move: bool = True

        # First phase: BFS to check if movement is possible
        while queue:
            rr, cc = queue.popleft()
            if (rr, cc) in seen:
                continue
            seen.add((rr, cc))

            rrr, ccc = rr + dr, cc + dc

            # Hit a wall - movement impossible
            if board[rrr][ccc] == '#':
                can_move = False
                break

            # Add connected box parts to queue
            if board[rrr][ccc] in ['O', '[', ']']:
                queue.append((rrr, ccc))

                # Handle two-part boxes
                if board[rrr][ccc] == '[':
                    assert board[rrr][ccc + 1] == ']'
                    queue.append((rrr, ccc + 1))
                elif board[rrr][ccc] == ']':
                    assert board[rrr][ccc - 1] == '['
                    queue.append((rrr, ccc - 1))

        # If movement is impossible, return unchanged
        if not can_move:
            return board, position

        # Second phase: Move all pieces
        while seen:
            # Sort to ensure consistent movement
            movable = []
            for rr, cc in sorted(seen):
                rrr, ccc = rr + dr, cc + dc
                if (rrr, ccc) not in seen:
                    movable.append((rr, cc))

            # Move pieces that can move
            for rr, cc in movable:
                rrr, ccc = rr + dr, cc + dc
                assert board[rrr][ccc] == '.'
                board[rrr][ccc] = board[rr][cc]
                board[rr][cc] = '.'
                seen.remove((rr, cc))

        return board, (r + dr, c + dc)

    return board, position


def calculate_coordinate_value(position: Tuple[int, int]) -> int:
    """Calculates the GPS coordinate value based on the position.
    """
    row, col = position
    return 100 * row + col


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.

    Args:
        data (Any): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """
    # setup
    board: List[List[str]] = data["board"]
    instructions: List[str] = data["instructions"]

    rows: int = len(board)
    cols: int = len(board[0])

    # find position
    robot_position: Optional[Tuple[int, int]] = None

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == "@":
                robot_position = (r, c)
                break

    if robot_position is None:
        return None

    # simulate movements
    for instr in instructions:
        board, robot_position = move_with_bfs(instr, board, robot_position)

    ans: int = 0
    # calculate GPS coordinates
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O':
                ans += calculate_coordinate_value((r, c))

    return ans


def print_board(board: List[List[str]]) -> None:
    """Prints the board.
    """
    rows: int = len(board)

    for r in range(rows):
        print("".join(board[r]))

    return


def create_ascii_video(
    board_history: List[List[List[str]]],
    instructions: List[str],
    output_file: str = 'board_animation.mp4',
    font_scale: float = 0.5,
    thickness: int = 1
) -> None:
    """Create a video from ASCII board states using OpenCV.

    Args:
        board_history (List[List[List[str]]]): List of board states to animate.
        instructions (List[str]): List of movement instructions.
        output_file (str, optional): Path to save the output video.
        font_scale (float, optional): Font scale for rendering. Defaults to 0.5.
        thickness (int, optional): Line thickness for text. Defaults to 1.
    """
    # Color mapping for different board elements
    color_map: Dict[str, Tuple[int, int, int]] = {
        '#': (50, 50, 50),     # Dark gray for walls
        '.': (200, 200, 200),  # Light gray for empty space
        '@': (0, 255, 0),      # Green for robot
        'O': (255, 0, 0),      # Red for boxes
        '[': (255, 165, 0),    # Orange for left box edge
        ']': (255, 165, 0),    # Orange for right box edge
    }

    # Video writer setup
    height: int = len(board_history[0]) * 30 + \
        50  # Extra space for instruction
    width: int = len(board_history[0][0]) * 20
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, 2.0, (width, height))

    # Create video frames
    for idx, board in enumerate(board_history):
        # Create a blank image
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame.fill(0)  # Black background

        # Render each character
        for y, row in enumerate(board):
            for x, char in enumerate(row):
                # Get color for the character
                color: Tuple[int, int, int] = color_map.get(
                    char, (255, 255, 255))

                # Put text on the frame
                cv2.putText(
                    frame,
                    char,
                    (x * 20, (y + 1) * 30),  # Position
                    cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale,
                    color,
                    thickness
                )

        # Add movement instruction to the bottom of the frame
        if idx > 0 and idx-1 < len(instructions):
            instruction: str = instructions[idx-1]
            cv2.putText(
                frame,
                f"Move: {instruction}",
                (10, height - 10),  # Position at the bottom
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,  # Slightly larger font
                (255, 255, 255),  # White color
                2  # Thicker line
            )

        # Write the frame
        out.write(frame)

    # Release the video writer
    out.release()


def solve_part_two(data: Any, infile: str) -> Any:
    """Solves part two of the challenge.

    Args:
        data (List[str]): The input data for the challenge.
        infile (str): Name of the input file being processed.

    Returns:
        Any: The result of the solution for part two.
    """
    # setup
    board: List[List[str]] = data["enlarged_board"]
    instructions: List[str] = data["instructions"]

    rows: int = len(board)
    cols: int = len(board[0])

    # Track board history for animation
    board_history: List[List[List[str]]] = [
        [row.copy() for row in board]
    ]

    # find position
    robot_position: Optional[Tuple[int, int]] = None

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == "@":
                robot_position = (r, c)

    if robot_position is None:
        return None

    # simulate movements
    for instr in instructions:
        board, robot_position = move_with_bfs(instr, board, robot_position)
        # Create a deep copy of the board for history
        board_history.append([row.copy() for row in board])

    # Create output filename based on input file
    prefix: str = 'day15_test_' if '.test' in infile else 'day15_'
    output_file: str = os.path.join(output_directory, f'{prefix}board_animation.mp4')

    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Create ASCII video
    create_ascii_video(board_history, instructions, output_file)

    ans: int = 0
    # calculate GPS coordinates
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == '[':
                ans += calculate_coordinate_value((r, c))

    return ans


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'

    unprocessed_data = read_input(infile)
    input_data = process(unprocessed_data['data'])

    result_part_one = solve_part_one(input_data)
    if result_part_one is not None:
        print(f"Part One: {result_part_one}")
    result_part_two = solve_part_two(input_data, infile)
    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")
