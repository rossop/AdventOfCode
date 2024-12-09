"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
import sys
from typing import List, Any, Dict, Union


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
            # Find the data section between Example data marker and answer section
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


def process(raw_data: str) -> List[List[Union[int, List[List[str]]]]]:
    """Processes the input data into a structured format.

    Args:
        raw_data (str): Raw input string containing game data.

    Returns:
        List[List[Union[int, List[List[str]]]]]: List of games, where each game contains:
            - game number (int)
            - list of turns, where each turn is a list of color counts
    """
    data: List[List[Union[int, List[List[str]]]]] = []
    for line in raw_data.splitlines():
        split_line: List[str] = line.split(': ')
        game_number: int = int(split_line[0].strip('Game '))
        game_play: List[List[str]] = [
            list(map(str.strip, turn.split(',')))
            for turn in split_line[1].split(';')
        ]
        data.append([game_number, game_play])

    return data


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.

    Args:
        data (Any): Processed game data.

    Returns:
        Any: The result of the solution for part one.
    """
    ans: int = 0
    for game, game_play in data:
        max_count: Dict[str, int] = {
            'red': 12,
            'green': 13,
            'blue': 14,
        }
        pass_condition: bool = True

        for turn in game_play:
            for draw in list(map(lambda x: x.split(','), turn)):
                parsed_draw = draw[0].split()
                num = int(parsed_draw[0])
                color = parsed_draw[1]
                if color in max_count.keys():
                    if max_count[color] < num:
                        pass_condition = False
                        break
        if pass_condition:
            ans += game

    return ans


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.

    Args:
        data (Any): Processed game data.

    Returns:
        Any: The result of the solution for part two.
    """
    ans: int = 0
    for game, game_play in data:
        max_count: Dict[str, int] = {
            'red': 0,
            'green': 0,
            'blue': 0,
        }

        for turn in game_play:
            for draw in list(map(lambda x: x.split(','), turn)):
                parsed_draw = draw[0].split()
                num = int(parsed_draw[0])
                color = parsed_draw[1]
                if color in max_count.keys():
                    if max_count[color] < num:
                        max_count[color] = num

        ans += max_count['red'] * max_count['green'] * max_count['blue']

    return ans


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'

    raw_data = read_input(infile)
    input_data = process(raw_data['data'])

    result_part_one = solve_part_one(input_data)
    if result_part_one is not None:
        print(f"Part One: {result_part_one}")
    result_part_two = solve_part_two(input_data)
    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")