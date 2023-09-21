# Advent of Code
from copy import deepcopy
from collections import defaultdict
from functools import reduce
import re

from typing import List, Dict, Set, Tuple, Optional

import pprint

pp = pprint.PrettyPrinter(indent=4)


def read_input(filename):
	with open(filename, 'r') as f:
		data = f.readlines()

	return data


def part_one(sensor_data, beacond_data):
	# Your code for part one goes here
	result = 0

	return result


def part_two(sensor_data, beacond_data):
	# Your code for part one goes here
	result = 0

	return result


def main():
	sensor_data, beacond_data = read_input("in/1.test")

	result_one = part_one(sensor_data, beacond_data)
	print(f"Part One: {result_one}")

	result_two = part_two(sensor_data, beacond_data)
	print(f"Part Two: {result_two}")


if __name__ == "__main__":
	main()
