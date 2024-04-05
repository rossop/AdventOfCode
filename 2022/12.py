# Advent of Code
'''
A problem with breadth-first-search
'''
from copy import deepcopy
from collections import deque 

from typing import List, Dict, Set, Tuple, Optional


import pprint
pp = pprint.PrettyPrinter(indent=4)

Vertex = Tuple[int,int,str]
Graph = Dict[Tuple[int, int, str], List[Tuple[int, int, str]]]


def read_input(filename):
	with open(filename, 'r') as f:
		data = f.readlines()
	return [[char for char in line.strip()]  for line in data]


def find_pos(grid : List[List[str]], char:str)-> List[Vertex]:
	R, C = len(grid), len(grid[0])

	found_vertices = []
	for r in range(R):
		for c in range(C):
			if grid[r][c] == char:
				found_vertices.append( (r,c,grid[r][c]) )

	if len(found_vertices) == 1:
		return found_vertices[0]
	return found_vertices


def build_graph(grid: List[List[str]]) -> Graph:
	graph: Graph = {}
	R, C = len(grid), len(grid[0])

	# possible moves
	moves: List[Tuple[int, int]] = [(0, -1), (0, 1), (-1, 0), (1, 0)]

	for r in range(R):
		for c in range(C):
			graph[(r, c, grid[r][c])] = []
			for dr, dc in moves:
				rr, cc = r + dr, c + dc
				if 0 <= rr < R and 0 <= cc < C:  # check if within boundaries
					current_height = ord(grid[r][c])
					neighbour_height = ord(grid[rr][cc])
					
					if grid[rr][cc] == 'S':
						neighbour_height = ord('a')
					elif grid[rr][cc] == 'E':
						neighbour_height = ord('z')

					if grid[r][c] == 'S':
						current_height = ord('a')
					elif grid[r][c] == 'E':
						current_height = ord('z')

					if neighbour_height - current_height <= 1:
						graph[(r, c, grid[r][c])].append((rr, cc, grid[rr][cc]))

	return graph


def bfs_shortest_distance(graph: Graph,
						  start: Vertex,
						  target: Vertex) -> Optional[int]:
	
	visited: Set[Vertex] = set()
	queue = deque([(start, 0)])  # Item in queue is a tuple (node, distance from start)

	while queue:
		vertex, distance = queue.popleft()  # Dequeue front node and distance from start
		
		if vertex == target:
			return distance  # Found target, return distance

		if vertex not in visited:
			visited.add(vertex)
			for neighbor in graph[vertex]:
				if neighbor not in visited:
					queue.append((neighbor, distance + 1))
	
	return None  # No distance == the target vertex is not reachable from start


def bfs_test():
  # Example usage
  graph = {
	'A': ['B', 'C'],
	'B': ['A', 'D', 'E'],
	'C': ['A', 'F'],
	'D': ['B'],
	'E': ['B', 'F'],
	'F': ['C', 'E']
  }
  start_node = 'A'
  print(bfs_shortest_distance(graph, start_node,'D'))
  return None


def part_one(data):
	# Your code for part one goes here
	graph = build_graph(data)
	start  = find_pos(data,'S')
	end  = find_pos(data,'E')

	distance = bfs_shortest_distance(graph, start, end)
	return distance


def part_two(data):
	# Your code for part two goes here
	graph = build_graph(data)
	
	start_S  = find_pos(data,'S')
	start_a = find_pos(data,'a')
	# Check if Start_S or start a is a list
	start_vertices = [start_S] + start_a

	end  = find_pos(data,'E')

	distances = []
	for start in start_vertices:
		distance = bfs_shortest_distance(graph, start, end)
		distances.append(distance)
	
	return min(filter(lambda x: x is not None, distances))


def main():
	input_data = read_input("in/12.in")

	result_one = part_one(input_data)
	print(f"Part One: {result_one}")
	
	result_two = part_two(input_data)
	print(f"Part Two: {result_two}")


if __name__ == "__main__":
	main()