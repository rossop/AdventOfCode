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
				print(path)
		elif words[1] == 'ls':
			continue
		else:
			try:
				sz = int(words[0])
				for i in range(len(path) + 1):
					sizes['/'.join(path[:i])] += sz
			except:
				pass
		# print(path)
	return sizes


def part_one(data):
	sizes = calc_size(data)
	pp.pprint(sizes)
	filter_size = 100000
	filtered_sizes = reduce(lambda acc, x: acc + (x if x < filter_size else 0),
	                        sizes.values(), 0)
	return filtered_sizes


def part_two(data):

	result = 0
	return result


def main():
	input_data = read_input("in/7.in")

	result_one = part_one(input_data)
	print(f"Part One: {result_one}")

	result_two = part_two(input_data)
	print(f"Part Two: {result_two}")


if __name__ == "__main__":
	main()
