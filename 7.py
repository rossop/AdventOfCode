# Advent of Code
from copy import deepcopy
from collections import defaultdict
from functools import reduce

from typing import List, Dict, Set, Tuple, Optional

import pprint

pp = pprint.PrettyPrinter(indent=4)


def read_input(filename):
	try:
		with open(filename, 'r') as f:
			data = f.read().strip().split('\n')
	except TypeError:
		print("Expected a filename as a string.")
	except FileNotFoundError:
		print(f"File {filename} not found.")

	return data


def calc_size(lines):
	sizes = defaultdict(int)
	path = []

	for line in lines:
		words = line.strip().split()
		if words[1] == 'cd':
			if words[2] == '..':
				path.pop()
			else:
				path.append(words[2])
		elif words[1] == 'ls':
			continue
		elif words[0] == 'dir':
			continue
		else:
			sz = int(words[0])
			for i in range(len(path) + 1):
				sizes['/'.join(path[:i])] += sz
	return sizes


def part_one(sizes):
	filter_size = 100000
	filtered_sizes = reduce(lambda acc, x: acc + (x if x < filter_size else 0),
	                        sizes.values(), 0)
	return filtered_sizes


def part_two(sizes):
	tot_disk_space = 70000000
	necessary_disk_space = 30000000
	max_usable_disk_space = tot_disk_space - necessary_disk_space  # max usable disk space

	used_disk_space = sizes['/']  # root folder size
	need_to_free = used_disk_space - max_usable_disk_space

	filtered_directories = [*filter(lambda x: x >= need_to_free, sizes.values())]
	if filtered_directories:
		result = min(filtered_directories)
	else:
		result = None

	return result


def main():
	input_data = read_input("in/7.in")
	sizes = calc_size(input_data)
	
	result_one = part_one(sizes)
	print(f"Part One: {result_one}")

	result_two = part_two(sizes)
	print(f"Part Two: {result_two}")


if __name__ == "__main__":
	main()
