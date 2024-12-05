"""
Template for Advent of Code solutions.

This module provides a structure for solving Advent of Code challenges.
The input files are expected to be located in the '2024/in' directory.
"""

import os
import sys
from typing import List, Any, Dict, Optional
from collections import defaultdict


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
    order: Dict[int, List[int]] = defaultdict(list)
    pages_to_update: List[List[str]] = []
    raw_order: str
    raw_pages_to_update: str
    raw_order, raw_pages_to_update = raw_data.split('\n\n')

    for line in raw_order.splitlines():
        start, end = line.strip().split('|')
        order[int(start)].append(int(end))

    for line in raw_pages_to_update.splitlines():
        pages_to_update.append(
            list(
                map(
                    int,
                    line.strip().split(',')
                )
            )
        )

    processed_data: Dict[str, Any] = {
        'order': order,
        'pages_to_update': pages_to_update
    }
    return processed_data


def find_middle_page_sum(
        pages_to_update: List[List[int]],
        ordered_pages: Optional[List[int]] = None
) -> int:
    """Find sum of mid pages"""
    ans: int = 0
    if ordered_pages is None:
        ordered_pages = range(len(pages_to_update))
    for i in ordered_pages:
        lst = pages_to_update[i]
        pos: int = len(lst)//2
        ans += lst[pos]
    return ans


def is_ordered(
        list_of_pages: List[int],
        order: Dict[int, List[int]]
) -> bool:
    """Check if the given list of pages is in the correct order.

    Args:
        list_of_pages (List[int]): The list of pages to check.
        order (Dict[int, List[int]]): The order mapping.

    Returns:
        bool: True if the pages are in the correct order, False otherwise.
    """
    p1: int = 0
    while p1 < len(list_of_pages):
        page_number_a: int = list_of_pages[p1]
        pages_that_follow: List[int] = order[page_number_a]

        for p2 in range(p1 + 1, len(list_of_pages)):
            page_number_b: int = list_of_pages[p2]
            if page_number_b not in pages_that_follow:
                return False
        p1 += 1
    return True


def check_page_orders(
        pages_to_update: List[List[int]],
        order: Dict[int, List[int]]
) -> List[int]:
    """Check for rows (lists of pages) with correct page orders.
    """
    ordered_pages: List[int] = []
    unordered_pages: List[List[int]] = []
    for i, list_of_pages in enumerate(pages_to_update):
        if is_ordered(list_of_pages, order):
            ordered_pages.append(i)
        else:
            unordered_pages.append([i, len(list_of_pages) - 1])
    return ordered_pages, unordered_pages


def reorder_pages(
        pages_to_reorder: List[List[int]],
        pos_breaking_order: List[int],
        order: Dict[int, List[int]]
) -> List[List[int]]:
    """Reorders pages to satisfy the given ordering rules.

    Args:
        pages_to_reorder (List[List[int]]): Lists of pages that need reordering
        pos_breaking_order (List[int]): Initial positions where order breaks
        order (Dict[int, List[int]]): Dictionary defining valid page orderings

    Returns:
        List[List[int]]: Lists with pages in correct order
    """
    for list_of_pages in pages_to_reorder:
        # Bubble sort with the ordering rules
        n: int = len(list_of_pages)
        for i in range(n):
            for j in range(0, n-i-1):
                page_a: int = list_of_pages[j]
                page_b: int = list_of_pages[j+1]
                # If page_b should come before page_a, swap them
                if page_b not in order[page_a]:
                    list_of_pages[j], list_of_pages[j+1] = \
                        list_of_pages[j+1], list_of_pages[j]

    return pages_to_reorder


if __name__ == "__main__":
    # TODO: review variable names
    day: str = __file__.rsplit('/', maxsplit=1)[-1].replace('.py', '')
    infile = sys.argv[1] if len(sys.argv) >= 2 else f'{day}.in'

    raw_data = read_input(infile)

    data = process(raw_data['data'])

    order: Dict[int, List[int]] = data['order']
    pages_to_update: List[List[int]] = data['pages_to_update']

    ordered_pages: List[int]
    unordered_pages: List[List[int]]

    ordered_pages, unordered_pages = \
        check_page_orders(pages_to_update, order)

    # Answer Pt 1
    result_part_one: int = find_middle_page_sum(
        pages_to_update,
        ordered_pages
    )

    pages_to_reorder = [pages_to_update[i] for i, j in unordered_pages]
    pos_breaking_oder = [j for i, j in unordered_pages]

    # Reorder the incorrectly ordered updates
    corrected_updates: List[List[int]] = reorder_pages(
        pages_to_reorder,
        pos_breaking_oder,
        order
    )

    # Calculate the sum of the middle page numbers
    result_part_two: Optional[int] = find_middle_page_sum(
        corrected_updates
    )

    if result_part_one is not None:
        print(f"Part One: {result_part_one}")

    if result_part_two is not None:
        print(f"Part Two: {result_part_two}")
