import pprint

pp = pprint.PrettyPrinter(indent=4)

with open('in/8.test') as file:
  forest = [list(map(int, line)) for line in file.read().strip().split('\n')]

# check treess from all cardinal points
R = len(forest)
C = len(forest[0])

visibility_grid = [[
  False if r == 0 or c == 0 or r == R - 1 or c == C - 1 else True
  for r in range(R)
] for c in range(C)]

# directions = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1]
#               if not ((dr + dc) in [0, 2, -2])] # exclude center and diagonals
directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]

for r in range(R):
  val = forest[r][0]
  for c in range(1, C):
    if forest[r][c] > val:
      val = forest[r][c]
      visibility_grid[r][c] = False
    else:
      visibility_grid[r][c] = visibility_grid[r][c] and True
  val = forest[r][-1]
  for c in range(C - 2, -1, -1):
    if forest[r][c] > val:
      val = forest[r][c]
      visibility_grid[r][c] = False
    else:
      visibility_grid[r][c] = visibility_grid[r][c] and True

for c in range(C):
  val = forest[0][c]
  for c in range(1, R):
    if forest[r][c] >= val:
      val = forest[r][c]
      visibility_grid[r][c] = False
    else:
      visibility_grid[r][c] = visibility_grid[r][c] and True
  val = forest[-1][c]
  for c in range(R - 2, -1, -1):
    if forest[r][c] >= val:
      val = forest[r][c]
      visibility_grid[r][c] = False
    else:
      visibility_grid[r][c] = visibility_grid[r][c] and True

visible = sum(sum(1 for val in row if not val) for row in visibility_grid)

pp.pprint(visibility_grid)
print(visible)
# The code below was wrong because I was not checking the whole row, but only neighbouring trees

def is_visible(forest, pos):
  '''
  given a forest and a specific position calculate if that tree is
  visible from the outside
  '''
  neighbours = [(pos[0] + dr, pos[1] + dc) for dr in [-1, 0, 1]
                for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]
  visible = False
  for r, c in neighbours:
    visible = (forest[pos[0]][pos[1]] <) or visible

  return visible

def count_visible(forest):
  '''
  take the forest as an input and count outbounding and inside
  visible trees
  '''
  R = len(forest)
  C = len(forest[0])

  visible_counter = 2 * R + 2 * (C - 2)  # borders
  print(visible_counter)

  for r in range(1, R - 1):  # exclude border
    for c in range(1, C - 1):

      if is_visible(forest, [r][c]):
        visible_counter += 1
        print(forest[r][c])

  return visible_counter

print(count_visible(forest))
