"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
import sys
from typing import Any, Dict, List


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
    cards: Dict[int, List[List[int]]] = {}

    for line in raw_data.splitlines():
        split_vals = line.split(":")
        card_num = int(split_vals[0].strip('Card').strip())

        number_parts: List[str] = split_vals[1].split("|")
        winning_nums: List[int] = [
            int(n.strip()) for n in number_parts[0].split()
        ]
        player_nums: List[int] = [
            int(n.strip()) for n in number_parts[1].split()
        ]

        cards[card_num] = [winning_nums, player_nums]
    return cards


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.

    Args:
        data (Any): The input data for the challenge.

    Returns:
        Any: The result of the solution for part one.
    """
    ans: int = 0
    for _, card in data.items():
        winning_numbers: List[int] = card[0]
        played_numbers: List[int] = card[1]

        count: int = 0
        for num in played_numbers:
            if num in winning_numbers:
                count += 1
        if count > 0:
            ans += 2 ** (count - 1)
    return ans


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.

    Args:
        data (List[str]): The input data for the challenge.

    Returns:
        Any: The result of the solution for part two.
    """
    # Start with just one copy of card 1
    card_counts: Dict[int, int] = {card_num: 1 for card_num in data.keys()}

    # Process each card number in order
    for card_num in range(1, max(data.keys()) + 1):
        if card_num not in card_counts:
            continue

        card: List[List[int]] = data[card_num]
        winning_numbers: List[int] = card[0]
        played_numbers: List[int] = card[1]

        # Count matches
        matches: int = sum(
            1 for num in played_numbers if num in winning_numbers)

        # For each copy of current card, add new copies of subsequent cards
        current_copies: int = card_counts[card_num]
        for next_card in range(card_num + 1, card_num + matches + 1):
            if next_card in data:  # Only add cards that exist
                card_counts[next_card] = card_counts.get(
                    next_card, 0) + current_copies

    return sum(card_counts.values())


if __name__ == "__main__":
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'

    unprocessed_data = read_input(infile)
    input_data = process(unprocessed_data['data'])

    result_part_one = solve_part_one(input_data)
    if result_part_one is not None:
        print(f"Part One: {result_part_one}")
    result_part_two = solve_part_two(input_data)
    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")
