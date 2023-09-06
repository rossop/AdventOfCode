class Rope:
  '''
  Rope class contain the position of the Head and Tail
  '''

  def __init__(self):
    with open('in/9.input') as file:
      lines = [(line.split(' ')[0], int(line.split(' ')[1]))
               for line in file.read().strip().split('\n')]

      self.instructions = lines
      self.head_pos = [0, 0]
      self.tail_pos = [0, 0]
      self.dir = {'R': (0, 1), 'L': (0, -1), 'U': (1, 0), 'D': (-1, 0)}
      self.dr = 0
      self.dc = 0
      self.visited = set()
      self.visited.add(tuple(self.tail_pos))

    print(self.instructions)

  def __repr__(self):
    return self.head_pos, self.tail_pos

  def move_head(self, move):
    direction = self.dir[move[0]]

    for ii in range(move[1]):
      self.head_pos = [
        self.head_pos[0] + direction[0], self.head_pos[1] + direction[1]
      ]
      self.tail_distance()
      if abs(self.dr) > 1 or abs(self.dc) > 1:
        self.move_tail()

  def move_tail(self):
    if abs(self.dr) > 1:
      if self.dc == 0:  # move vertically
        self.tail_pos[0] = self.tail_pos[0] + self.dr / abs(self.dr)
      else:  # move diagonally
        self.tail_pos = [
          self.tail_pos[0] + self.dr / abs(self.dr),
          self.tail_pos[1] + self.dc / abs(self.dc)
        ]

    if abs(self.dc) > 1:
      if self.dr == 0:  # move horizontally
        self.tail_pos[1] = self.tail_pos[1] + self.dc / abs(self.dc)
        pass
      else:  # move diagonally
        self.tail_pos = [
          self.tail_pos[0] + self.dr / abs(self.dr),
          self.tail_pos[1] + self.dc / abs(self.dc)
        ]

    self.visited.add(tuple(self.tail_pos))

  def tail_distance(self):
    self.dr = self.head_pos[0] - self.tail_pos[0]
    self.dc = self.head_pos[1] - self.tail_pos[1]

  def is_tail_adjacent(self):
    pass

  def start(self):
    for instruction in self.instructions:
      self.move_head(instruction)

class LongRope(Rope):
  def __

R = Rope()
R.start()
print(len(R.visited))

