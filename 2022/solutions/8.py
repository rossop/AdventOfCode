# Advent of Code
from copy import deepcopy
from collections import deque
import pprint

pp = pprint.PrettyPrinter(indent=4)


def read_input(filename):
  with open(filename) as file:
    forest = [list(map(int, line)) for line in file.read().strip().split('\n')]
  return forest


class Forest():

  def __init__(self, data):
    self.forest = data
    # check trees from all cardinal points
    self.R = len(self.forest)
    self.C = len(self.forest[0])
    self.R_edge = [0, self.R - 1]
    self.C_edge = [0, self.C - 1]

    # Initialize visibility_grid with True at borders and False inside
    self.visibility_grid = [[
      False
      if r != 0 and c != 0 and r != self.R - 1 and c != self.C - 1 else True
      for c in range(self.C)
    ] for r in range(self.R)]

  def part_one(self):
    # Check from the top and bottom borders
    for r in range(self.R):
      val = self.forest[r][0]
      for c in range(1, self.C):
        if self.forest[r][c] > val:
          val = self.forest[r][c]
          if (r not in self.R_edge) and (c not in self.C_edge):
            self.visibility_grid[r][c] = True

      val = self.forest[r][-1]
      for c in range(self.C - 2, -1, -1):
        if self.forest[r][c] > val:
          val = self.forest[r][c]
          if (r not in self.R_edge) and (c not in self.C_edge):
            self.visibility_grid[r][c] = True

    # Check from the left and right borders
    for c in range(self.C):
      val = self.forest[0][c]
      for r in range(1, self.R):
        if self.forest[r][c] > val:
          val = self.forest[r][c]
          if (r not in self.R_edge) and (c not in self.C_edge):
            self.visibility_grid[r][c] = True

      val = self.forest[-1][c]
      for r in range(self.R - 2, -1, -1):
        if self.forest[r][c] > val:
          val = self.forest[r][c]
          if (r not in self.R_edge) and (c not in self.C_edge):
            self.visibility_grid[r][c] = True

    # Count the number of not visible points
    visible = sum(sum(1 for val in row if val) for row in self.visibility_grid)
    # Calculate the number of visible points

    return visible

  def part_two(self):
    # Your code for part two goes here
    # Check from the top and bottom borders
    max_scenic_score = -1
    for r in range(1,self.R):
      for c in range(1, self.C):
        if True: # not self.visibility_grid[r][c]:
          val = self.forest[r][c]
          scene = [0, 0, 0, 0]

          # go up
          counter = 0
          for cc in range(c - 1, -1, -1):
            counter += 1
            if self.forest[r][cc] >= val:
              break
          scene[0] = counter

          # go left
          counter = 0
          for rr in range(r - 1, -1, -1):
            counter += 1
            if self.forest[rr][c] >= val:
              break
          scene[1] = counter

          # go down
          counter = 0
          for cc in range(c + 1, self.C):
            counter += 1
            if self.forest[r][cc] >= val:
              break
          scene[2] = counter

          # go right
          counter = 0
          for rr in range(r + 1, self.R):
            counter += 1
            if self.forest[rr][c] >= val:
              break
          scene[3] = counter


          scenic_score = 1

          for score in scene:
            scenic_score *= score
          if scenic_score > max_scenic_score:
            max_scenic_score = scenic_score


    return max_scenic_score


def main():
  input_data = read_input("../in/8.in")

  f = Forest(input_data)
  result_one = f.part_one()
  print(f"Part One: {result_one}")

  result_two = f.part_two()
  print(f"Part Two: {result_two}")


if __name__ == "__main__":
  main()
