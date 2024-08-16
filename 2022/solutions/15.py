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
	sensor = []
	beacon = []
	for line in data:
		sensor_match = re.search(r'Sensor at x=(-?\d+), y=(-?\d+)', line)
		beacon_match = re.search(r'closest beacon is at x=(-?\d+), y=(-?\d+)', line)

		if sensor_match and beacon_match:
			sensor.append(  #tuple
			 (int(sensor_match.group(1)), int(sensor_match.group(2))))
			beacon.append(  #tuple
			 (int(beacon_match.group(1)), int(beacon_match.group(2))))

	return sensor, beacon


def mark_area(sensor, beacon):

	marked_area = set()

	DX = abs(beacon[0] - sensor[0])
	DY = abs(beacon[1] - sensor[1])
	LEN = DX + DY  # Manhattan distance

	for dx in range(-LEN, LEN + 1):
		for dy in range(-LEN, LEN + 1):
			if abs(dx) + abs(dy) <= LEN:
				marked_area.add((sensor[0] + dx, sensor[1] + dy))
	return marked_area


def part_one(sensor_data, beacon_data):
	# Your code for part one goes here
	marked_area = set()

	for sensor, beacon in zip(sensor_data, beacon_data):
		marked_area |= mark_area(sensor, beacon)

	# y = 2000000 # filtered row
	y = 10  # test filtered row
	filtered_data = set()
	for pos in marked_area:
		if pos[1] == y:
			filtered_data.add(pos)

	# remove already existing beacons from the filtered marked area
	filtered_data = set(
	 [item for item in filtered_data if item not in beacon_data or item[1] != y])

	return len(filtered_data)


def part_two(sensor_data, beacon_data):
	# Your code for part one goes here
	result = 0

	return result


def main():
	sensor_data, beacon_data = read_input("../in/15.test")

	result_one = part_one(sensor_data, beacon_data)
	print(f"Part One: {result_one}")

	result_two = part_two(sensor_data, beacon_data)
	print(f"Part Two: {result_two}")


if __name__ == "__main__":
	main()
