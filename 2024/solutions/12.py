"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
import sys
from typing import Any, Dict, Set, List, Tuple
import copy


input_directory: str = os.path.join(
    os.path.dirname(
        os.path.abspath(
            os.path.dirname(__file__)
        )
    ), 'in'
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
    return [
        list(line) for line in raw_data.splitlines()
    ]


def solve(data: Any) -> Any:
    """Solves part one of the challenge.

    Args:
        data (Any): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """
    # Find Regions
    # This is similar to Island problems in Leetcode
    rows: int = len(data)
    cols: int = len(data[0])

    regions: Dict = {}
    visited: Set = set()
    grid: List[List[str]] = copy.deepcopy(data)

    def get_edges(plants: List[Tuple[int, int]],
                  perimeter_points: List[Tuple[int, int]]) -> int:
        """
        Counts number of distinct edges in a region by finding connected
        components.
        """
        plant_set: List[Tuple[int, int]] = set(plants)
        perimeter_set: Set[Tuple[int, int]] = set(perimeter_points)
        visited: Set[Tuple[int, int]] = set()
        components: int = 0

        # Find bounds for visualization
        min_x: int = min(min(x for x, _ in plants),
                         min(x for x, _ in perimeter_points))
        max_x: int = max(max(x for x, _ in plants),
                         max(x for x, _ in perimeter_points))
        min_y: int = min(min(y for _, y in plants),
                         min(y for _, y in perimeter_points))
        max_y: int = max(max(y for _, y in plants),
                         max(y for _, y in perimeter_points))

        def get_adjacent_positions(x: int, y: int) -> List[Tuple[int, int]]:
            """Get all valid adjacent positions."""
            return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

        def dfs_component(point: Tuple[int, int],
                          current_component: Set[Tuple[int, int]]) -> None:
            """DFS to find connected perimeter points."""
            visited.add(point)
            current_component.add(point)

            x, y = point
            for next_point in get_adjacent_positions(x, y):
                if (
                    next_point in perimeter_set and
                    next_point not in visited
                ):
                    # Check if there's a plant between these perimeter points
                    shared_plant: bool = False
                    for plant in plants:
                        if (
                            is_adjacent(next_point, plant) and
                            is_adjacent(point, plant)
                        ):
                            shared_plant = True
                            break
                    if not shared_plant:
                        dfs_component(next_point, current_component)

        def visualize_component(component_points: Set[Tuple[int, int]],
                                component_num: int) -> None:
            """Visualize a single component with ASCII art."""
            print(f"\nComponent {component_num}:")
            for x in range(min_x - 1, max_x + 2):
                row: str = ""
                for y in range(min_y - 1, max_y + 2):
                    if (x, y) in component_points:
                        row += str(component_num)
                    elif (x, y) in plant_set:
                        row += "P"
                    elif (x, y) in perimeter_set:
                        row += "."
                    else:
                        row += " "
                print(row)

        def is_adjacent(p1: Tuple[int, int], p2: Tuple[int, int]) -> bool:
            """Check if two points are adjacent."""
            x1, y1 = p1
            x2, y2 = p2
            return abs(x1 - x2) + abs(y1 - y2) == 1

        # Find and visualize connected components
        print(f"\nAnalyzing region with {len(plants)} plants...")
        for point in perimeter_points:
            if point not in visited:
                components += 1
                current_component: Set[Tuple[int, int]] = set()
                dfs_component(point, current_component)
                visualize_component(current_component, components)

        print(f"Total components found: {components}\n")
        return components

    def dfs(i, j, region):
        if (
            i < 0 or
            i >= rows or
            j < 0 or
            j >= cols or
            grid[i][j] != region[0]
        ):
            regions[region]["perimeter"] += 1
            return "Perimeter"
        elif (i, j) in visited:
            return "Visited"

        visited.add((i, j))
        regions[region]["plants"].append((i, j))
        regions[region]["area"] += 1
        status = dfs(i+1, j, region)
        if status == "Perimeter":
            regions[region]["PerimeterPlants"].append((i+1, j))
        status = dfs(i-1, j, region)
        if status == "Perimeter":
            regions[region]["PerimeterPlants"].append((i-1, j))
        status = dfs(i, j+1, region)
        if status == "Perimeter":
            regions[region]["PerimeterPlants"].append((i, j+1))
        status = dfs(i, j-1, region)
        if status == "Perimeter":
            regions[region]["PerimeterPlants"].append((i, j-1))
        return

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                label: str = grid[r][c]
                region: Tuple[str, int, int] = (label, r, c)

                regions[region] = {
                    "plants": [],
                    "perimeter": 0,
                    "area": 0,
                    "PerimeterPlants": []
                }
                # use region for differentiate regions with same letter
                dfs(r, c, region)

    # calc values
    ans: int = 0
    ans2: int = 0
    # Create a grid that is 1 larger than the original grid

    # Fill the visual grid with plants and perimeter markers
    for (label, r, c), info in regions.items():
        visual_grid: List[List[str]] = [
            [' ' for _ in range(cols + 2)] for _ in range(rows + 2)
        ]
        for (plant_r, plant_c) in info["plants"]:
            # Offset by 1 for the border
            visual_grid[plant_r + 1][plant_c + 1] = label
        for (perimeter_r, perimeter_c) in info["PerimeterPlants"]:
            # Offset by 1 for the border
            visual_grid[perimeter_r + 1][perimeter_c + 1] = '#'

        # Print the visual grid
        for row in visual_grid:
            print(''.join(row))

    for _, info in regions.items():
        perimeter: int = info["perimeter"]
        area: int = info["area"]
        sides: int = get_edges(info["plants"], info["PerimeterPlants"])
        ans += area * perimeter
        ans2 += area * sides
        print(info)
    print(ans, ans2)
    return ans


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'

    unprocessed_data = read_input(infile)
    input_data = process(unprocessed_data['data'])
    result_part_one = solve(input_data)
    if result_part_one is not None:
        print(f"Part One: {result_part_one}")
    result_part_two = None
    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")
