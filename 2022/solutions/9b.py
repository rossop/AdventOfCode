def read_instructions_from_file(file_path):
  with open(file_path) as file:
    lines = [
      (direction, int(steps))
      for direction, steps in (line.split()
                               for line in file.read().strip().split('\n'))
    ]
  return lines


class Rope:
  '''
  Rope class contain the position of the Head and Tail
  '''

  def __init__(self):
    self.part = 1
    self.instructions = read_instructions_from_file('../in/9.input')
    self.head_pos = [0, 0]
    self.tail_pos = [0, 0]
    self.dir = {'R': (0, 1), 'L': (0, -1), 'U': (1, 0), 'D': (-1, 0)}
    self.dr = 0
    self.dc = 0
    self.visited = set()
    self.visited.add(tuple(self.tail_pos))

  def __repr__(self):
    return f"Part {self.part}: Head Position: {self.head_pos}, Tail Position: {self.tail_pos} which visited {len(self.visited)} positions"

  def move_head(self, move):
    direction, steps = move
    dx, dy = self.dir[direction]

    for _ in range(steps):
      self.head_pos[0] += dx
      self.head_pos[1] += dy
      self.update_tail_distance()
      self.move_tail_if_needed()

  def move_tail_if_needed(self):
    if abs(self.dr) > 1 or abs(self.dc) > 1:
      self.move_tail()

  def move_tail(self):
    '''

    '''
    if self.dc == 0:  # move vertically
      self.tail_pos[0] += self.dr // abs(self.dr)
    elif self.dr == 0:  # move horizontally
      self.tail_pos[1] += self.dc // abs(self.dc)
    else:  # move diagonally
      self.tail_pos = [
        self.tail_pos[0] + self.dr // abs(self.dr),
        self.tail_pos[1] + self.dc // abs(self.dc)
      ]

    self.visited.add(tuple(self.tail_pos))

  def update_tail_distance(self):
    self.dr = self.head_pos[0] - self.tail_pos[0]
    self.dc = self.head_pos[1] - self.tail_pos[1]

  def start(self):
    for instruction in self.instructions:
      self.move_head(instruction)


class LongRope(Rope):

  def __init__(self):
    super().__init__()
    self.part = 2
    self.number_of_knots = 10
    self.tail_pos = [[0, 0] for _ in range(self.number_of_knots - 1)]
    self.dr = [0 for _ in range(len(self.tail_pos))]
    self.dc = [0 for _ in range(len(self.tail_pos))]
    self.knots_pos = [self.head_pos] + self.tail_pos
    # all knots start on 0,0 so there is no need in changing self.visited

  def __repr__(self):
    self.tail_pos = self.knots_pos[1:]
    self.head_pos = self.knots_pos[0]
    return super().__repr__()

  def move_head(self, move):
    direction, steps = move
    dx, dy = self.dir[direction]

    for _ in range(steps):
      self.knots_pos[0][0] += dx
      self.knots_pos[0][1] += dy
      self.move_tail()

  def move_tail(self):
    '''

    '''
    for ii in range(len(self.knots_pos) - 1):
      self.update_tail_distance(ii)
      if abs(self.dr[ii]) > 1 or abs(self.dc[ii]) > 1:
        if self.dc[ii] == 0:  # move vertically
          self.knots_pos[ii + 1][0] += self.dr[ii] // abs(self.dr[ii])
        elif self.dr[ii] == 0:  # move horizontally
          self.knots_pos[ii + 1][1] += self.dc[ii] // abs(self.dc[ii])
        else:  # move diagonally
          self.knots_pos[ii + 1] = [
            self.knots_pos[ii + 1][0] + self.dr[ii] // abs(self.dr[ii]),
            self.knots_pos[ii + 1][1] + self.dc[ii] // abs(self.dc[ii])
          ]
      # else:
      #   break

    self.visited.add(tuple(self.knots_pos[-1]))

  def update_tail_distance(self,ii):
      self.dr[ii] = self.knots_pos[ii][0] - self.knots_pos[ii + 1][0]
      self.dc[ii] = self.knots_pos[ii][1] - self.knots_pos[ii + 1][1]


if __name__ == "__main__":
  rope = Rope()
  rope.start()
  print(rope)

  long_rope = LongRope()
  long_rope.start()
  print(long_rope)
