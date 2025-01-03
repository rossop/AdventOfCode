"""
Template for Advent of Code solutions (located in YYYY/solutions).

This file provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the 'YYYY/in' directory.
"""

import os
import sys
from typing import Any, Counter, Dict, List, Optional, Tuple
from typing import Counter as TypingCounter

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
        (
            line.split()[0],
            int(line.split()[1])
        ) for line in raw_data.splitlines()
    ]


def evaluate_hand(
    hand: str,
    part2: Optional[bool] = False
) -> Tuple[int, List[int]]:
    """Evaluates a hand of cards.

    Args:
        hand: A string representing the cards in hand.
        part2: Boolean flag for part 2 rules where J is a joker.

    Returns:
        Tuple containing:
            - Hand type rank (0-6, higher is better)
            - List of card values for tie-breaking
    """
    card_value: Dict[str, int] = {
        'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7,
        '6': 6, '5': 5, '4': 4, '3': 3, '2': 2
    }
    if part2:
        card_value['J'] = 1

    numerical_hand = [card_value[card] for card in hand]
    card_counts: TypingCounter[int] = Counter(numerical_hand)

    # Special handling for jokers in part 2
    if part2 and 1 in card_counts:  # 1 is the value of J in part2
        joker_count: int = card_counts[1]
        if joker_count == 5:  # All jokers case
            return (6, numerical_hand)  # Five of a kind

        del card_counts[1]  # Remove jokers temporarily
        # Find the card that appears most frequently
        most_common_cards = card_counts.most_common()
        # Add jokers to the most frequent card
        card_counts[most_common_cards[0][0]] += joker_count

    most_common_cards = card_counts.most_common()
    counts = [count for _, count in most_common_cards]

    # Determine hand type
    if 5 in counts:
        return (6, numerical_hand)  # Five of a kind
    if 4 in counts:
        return (5, numerical_hand)  # Four of a kind
    if 3 in counts:
        if 2 in counts:
            return (4, numerical_hand)  # Full house
        return (3, numerical_hand)  # Three of a kind
    if counts.count(2) == 2:
        return (2, numerical_hand)  # Two pair
    if 2 in counts:
        return (1, numerical_hand)  # One pair
    return (0, numerical_hand)  # High card


def solve_part_one(data: Any) -> Any:
    """Solves part one of the challenge.
    """
    if data is None:
        return None

    # Evaluate all hands
    plays = []
    for hand, bid in data:
        type_rank, tie_breakers = evaluate_hand(hand, part2=False)
        plays.append((type_rank, tie_breakers, bid))

    # Sort plays based on rank and original card order
    sorted_plays = sorted(plays, key=lambda x: (x[0], x[1]), reverse=False)

    # Calculate total winnings
    total_winnings = sum((i + 1) * bid for i, (_, _, bid)
                         in enumerate(sorted_plays))
    return total_winnings


def solve_part_two(data: Any) -> Any:
    """Solves part two of the challenge.
    """
    if data is None:
        return None

    # Evaluate all hands
    plays = []
    for hand, bid in data:
        type_rank, tie_breakers = evaluate_hand(hand, part2=True)
        plays.append((type_rank, tie_breakers, bid))

    # Sort plays based on rank and original card order
    sorted_plays = sorted(plays, key=lambda x: (x[0], x[1]), reverse=False)

    # Calculate total winnings
    total_winnings = sum((i + 1) * bid for i, (_, _, bid)
                         in enumerate(sorted_plays))
    return total_winnings


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
