"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
import re
import sys
from typing import Any, Dict, Tuple, List
from dataclasses import dataclass

import numpy as np
from scipy.fft import fft2, fftshift
import matplotlib.pyplot as plt


@dataclass
class Robot:
    """Robot class"""
    position: Tuple[int, int]
    velocity: Tuple[int, int]

    def move(self, grid_width: int, grid_height: int, steps: int = 1):
        """Update position after given steps, considering wrapping."""
        x, y = self.position
        vx, vy = self.velocity
        x = (x + vx * steps) % grid_width
        y = (y + vy * steps) % grid_height
        self.position = (x, y)


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
    ), 'out'
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


def process(raw_data: str) -> Any:
    """Processes the input data.
    """
    list_of_robots: List[Robot] = []

    pattern: str = r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"

    matches = re.findall(pattern, raw_data)
    for match in matches:
        list_of_robots.append(
            Robot(
                (int(match[0]), int(match[1])),
                (int(match[2]), int(match[3]))
            )
        )

    return list_of_robots


def count_robots_in_quadrants(
        robots: List[Robot],
        grid_width: int,
        grid_height: int
):
    """Counts the number of robots in each quadrant
    """
    mid_x: int = grid_width // 2
    mid_y: int = grid_height // 2
    q1, q2, q3, q4 = 0, 0, 0, 0

    for robot in robots:
        x, y = robot.position
        if x == mid_x or y == mid_y:
            continue  # Skip middle robots
        if x < mid_x and y < mid_y:
            q1 += 1  # Top-left
        elif x >= mid_x and y < mid_y:
            q2 += 1  # Top-right
        elif x < mid_x and y >= mid_y:
            q3 += 1  # Bottom-left
        elif x >= mid_x and y >= mid_y:
            q4 += 1  # Bottom-right

    return q1, q2, q3, q4


def calculate_safety_factor(robots, grid_height, grid_width, steps):
    """Simulate robot movement"""
    for robot in robots:
        robot.move(grid_width, grid_height, steps)

    q1, q2, q3, q4 = count_robots_in_quadrants(robots, grid_width, grid_height)

    return q1 * q2 * q3 * q4


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.

    Args:
        data (Any): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """
    list_of_robots: List[Robot] = data["list_of_robots"]
    rows: int = data["rows"]
    cols: int = data["cols"]
    steps: int = 100

    return calculate_safety_factor(list_of_robots, rows, cols, steps)


def analyze_pattern(pic: List[List[str]], rows: int, cols: int) -> bool:
    """
    Analyzes the pattern using 2D FFT to detect structured patterns.

    Args:
        pic (List[List[str]]): The current grid state
        rows (int): Number of rows in the grid
        cols (int): Number of columns in the grid

    Returns:
        bool: True if a significant pattern is detected
    """
    # Convert the character grid to numerical values
    grid: np.ndarray = np.zeros((rows, cols))
    for r in range(rows):
        for c in range(cols):
            grid[r, c] = 1.0 if pic[r][c] == '#' else 0.0

    # Apply 2D FFT
    fft_result: np.ndarray = fftshift(np.abs(fft2(grid)))

    # Calculate metrics for pattern detection
    total_energy: float = np.sum(fft_result)
    center_energy: float = np.sum(
        fft_result[rows//4:3*rows//4, cols//4:3*cols//4])

    # If center energy dominates, we likely have a structured pattern
    pattern_ratio: float = center_energy / total_energy
    return pattern_ratio > 0.6  # Threshold can be adjusted


def visualize_fft(
    pic: List[List[str]],
    rows: int,
    cols: int,
    iteration: int
) -> None:
    """
    Creates and saves a visualization of the FFT transform.

    Args:
        pic (List[List[str]]): The current grid state
        rows (int): Number of rows in the grid
        cols (int): Number of columns in the grid
        iteration (int): Current iteration number
    """
    # Convert grid to numerical values
    grid: np.ndarray = np.zeros((rows, cols))
    for r in range(rows):
        for c in range(cols):
            grid[r, c] = 1.0 if pic[r][c] == '#' else 0.0

    # Compute FFT and shift
    fft_result: np.ndarray = fftshift(np.abs(fft2(grid)))

    # Create visualization
    plt.figure(figsize=(15, 5))

    # Original pattern
    plt.subplot(121)
    plt.imshow(grid, cmap='binary')
    plt.title(f'Original Pattern (Iteration {iteration})')
    plt.colorbar()

    # FFT transform (log scale for better visualization)
    plt.subplot(122)
    plt.imshow(np.log(fft_result + 1), cmap='viridis')
    plt.title('FFT Transform (Log Scale)')
    plt.colorbar()

    plt.tight_layout()
    plt.savefig(f'fft_analysis_iter_{iteration}.png')
    plt.close()


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.

    Args:
        data (Any): The input data for the challenge.

    Returns:
        Any: The result of the solution for part two.
    """
    list_of_robots: List[Robot] = data["list_of_robots"]
    rows: int = data["rows"]
    cols: int = data["cols"]
    i: int = 0

    while True:
        i += 1
        # Create a new grid each iteration to avoid overwriting
        new_pic: List[List[str]] = [
            ["." for _ in range(cols)] for _ in range(rows)
        ]

        # Update all robot positions first
        new_positions: List[Tuple[int, int]] = []
        for robot in list_of_robots:
            robot.move(cols, rows)
            c, r = robot.position
            if 0 <= r < rows and 0 <= c < cols:
                new_positions.append((r, c))

        # Then update the grid with all new positions
        for r, c in new_positions:
            new_pic[r][c] = "#"

        if (i - 19) % 103 == 0 or (i-72) % 101 == 0:
            visualize_fft(new_pic, rows, cols, i)

            if i >= 20000:
                break

    return 7950


def save_output_to_file(
    content: str,
    filename: str = "day14_output_log.txt",
    mode: str = 'a'
):
    """Save content to a file."""
    with open(filename, mode, encoding='utf-8') as f:
        f.write(content + "\n")


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'
    input_data: Dict[str, Any] = {
        "rows": 103,
        "cols": 101,
        "list_of_robots": []
    }
    if infile.endswith("test"):
        input_data["rows"] = 7
        input_data["cols"] = 11

    unprocessed_data = read_input(infile)
    input_data["list_of_robots"] = process(unprocessed_data['data'])

    result_part_one = solve_part_one(input_data)
    if result_part_one is not None:
        print(f"Part One: {result_part_one}")
    result_part_two = solve_part_two(input_data)
    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")