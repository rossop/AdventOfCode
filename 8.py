# Advent of Code
from copy import deepcopy
from collections import deque
import pprint

pp = pprint.PrettyPrinter(indent=4)


def read_input(filename):
  with open(filename) as file:
    forest = [list(map(int, line)) for line in file.read().strip().split('\n')]
  return forest


def part_one(forest):
  # Your code for part one goes here

  # check trees from all cardinal points
  R = len(forest)
  C = len(forest[0])
  R_edge = [0, R - 1]
  C_edge = [0, C - 1]


  # Initialize visibility_grid with False at borders and True inside
  visibility_grid = [[
    False if r != 0 and c != 0 and r != R - 1 and c != C - 1 else True
    for c in range(C)
  ] for r in range(R)]

  # Check from the top and bottom borders
  for r in range(R):
    val = forest[r][0]
    for c in range(1, C):
      if forest[r][c] > val:
        val = forest[r][c]
        if (r not in R_edge) and (c not in C_edge):
          visibility_grid[r][c] = True
      

    val = forest[r][-1]
    for c in range(C - 2, -1, -1):
      if forest[r][c] > val:
        val = forest[r][c]
        if (r not in R_edge) and (c not in C_edge):
          visibility_grid[r][c] = True
      

  # Check from the left and right borders
  for c in range(C):
    val = forest[0][c]
    for r in range(1, R):
      if forest[r][c] > val:
        val = forest[r][c]
        if (r not in R_edge) and (c not in C_edge):
          visibility_grid[r][c] = True
      

    val = forest[-1][c]
    for r in range(R - 2, -1, -1):
      if forest[r][c] > val:
        val = forest[r][c]
        if (r not in R_edge) and (c not in C_edge):
          visibility_grid[r][c] = True
      

  # Count the number of not visible points
  visible = sum(
    sum(1 for val in row if val) for row in visibility_grid)
  # Calculate the number of visible points

  return visible


def part_two(data):
  # Your code for part two goes here
  result = 0
  return result


def main():
  input_data = read_input("in/8.in")

  result_one = part_one(input_data)
  print(f"Part One: {result_one}")

  result_two = part_two(input_data)
  print(f"Part Two: {result_two}")


if __name__ == "__main__":
  main()
