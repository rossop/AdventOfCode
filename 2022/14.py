# Advent of Code
from copy import deepcopy
from collections import defaultdict
from functools import reduce

from typing import List, Dict, Set, Tuple, Optional

import pprint

pp = pprint.PrettyPrinter(indent=4)


def test_add_wall():
	vertices = [[(498, 4), (498, 6)], [(498, 6), (496, 6)]]

	wall = set()
	for v in vertices:
		w = add_wall(v)
		wall |= w

	pp.pprint(wall)


def add_wall(vertices):
	wall = set()

	xi, yi = vertices[0]
	xj, yj = vertices[1]

	xi, xj = sorted([xi, xj])
	yi, yj = sorted([yi, yj])

	wall = [(x, y) for x in range(xi, xj + 1) for y in range(yi, yj + 1)]

	return set(wall)


def build_grid(data):
	wall = set()

	for vertices in data:
		w = add_wall(vertices)
		wall |= w

	return wall


# The rock is pouring into the cave from point 500,0.


def read_input(filename):
	with open(filename, 'r') as f:
		data = f.readlines()
		data = [line.strip() for line in data]
	input_data = []
	for line in data:
		vertices = line.split(' -> ')
		for v in range(len(vertices) - 1):
			first_vertex = tuple(map(int, vertices[v].split(',')))
			second_vertex = tuple(map(int, vertices[v + 1].split(',')))
			input_data.append([first_vertex, second_vertex])

	return input_data


def move_rock(wall):
	start_rock = (500, 0)  # start rock
	floor = max([y for x,y in wall]) 
	hi_x = max([x for x,y in wall])
	lo_x = min([x for x,y in wall])

	
	saturation_step = 0
	
	for step in range(int(5e4)):
		rock = deepcopy(start_rock)
		moves = True
		if rock in wall:
			break 
			
		while moves:
			if (rock[0], rock[1] + 1) not in wall:
				rock = (rock[0], rock[1] + 1)
			elif (rock[0] - 1, rock[1] + 1) not in wall:
				rock = (rock[0] - 1, rock[1] + 1)
			elif (rock[0] + 1, rock[1] + 1) not in wall:
				rock = (rock[0] + 1, rock[1] + 1)
			else:
				wall.add(rock)
				saturation_step += 1
				moves = False
			if rock[1] > floor:
				moves = False

			if rock[0] < lo_x or rock[0] > hi_x:
				break
				
	return saturation_step


def part_one(data):
	# Your code for part one goes here
	wall = build_grid(data)
	result = move_rock(wall)

	return result


def part_two(data):
	# Your code for part two goes here
	wall = build_grid(data)
	floor = max([y for x,y in wall]) 
	hi_x = int(max([x for x,y in wall]) + 1e4)
	lo_x = int(min([x for x,y in wall]) - 1e4)
	bottom_wall = [(x,floor + 2)for x in range(hi_x - lo_x)]
	wall |= set(bottom_wall)

	result = move_rock(wall)
	return result


def main():
	input_data = read_input("in/14.in")

	result_one = part_one(input_data)
	print(f"Part One: {result_one}")

	result_two = part_two(input_data)
	print(f"Part Two: {result_two}")


if __name__ == "__main__":
	main()
