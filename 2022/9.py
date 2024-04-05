''' 
Planning
I need to decide
  - How to represent the position of head and tail
  - how large is the space I want to use to map HT
  - How i am going to move head and tail
  
Procedure should be something along the line of 
  - apply movement for H
  - check relative position for T
  - apply movement for T
  - save new position of T in set

Final notes
I didn't need a board, I just need two list with position and a third list with the visited positions
  
'''

import numpy as np


class Rope:
  '''
  Rope class containin the position of the Head and Tail
  and takes in cosideration the movement of the head and tail
  '''

  def __init__(self):
    with open('in/9.test') as file:
      lines = [(line.split(' ')[0], int(line.split(' ')[1]))
               for line in file.read().strip().split('\n')]

    self.lines = lines
    self.tail_positions = self.create_board(10, 10)
    # [[" " for _ in range(10)] for _ in range(10)]  #I picked an arbitrary large number
    self.tail_positions[0][0] = 'T'
    self.head_positions= self.tail_positions.copy()
    self.head_positions[0][0] = 'H'

  def __repr__(self):
    for row in self.tail_positions:
      print(row)

    print(' ')
    for row in self.head_positions:
      print(row)
    return ' '

  def create_board(self, rows, cols):
    return np.full((rows, cols), ' ')

  def is_tail_adjacent(self):
    '''
    is_tail_adjacent checks if the tail is adjacent to the head
    Returns:
      - True if tail is adjacent to the head
      - False if the tail is NOT adjacent to the head
    '''
    H_pos = np.where(self.head_positions == 'H')
    T_pos = np.where(self.tail_positions == 'T')

    for ii in range(-1, 2):
      for jj in range(-1,2):
        if H_pos = (T_pos[0] + ii, T_pos[1] + jj):
          return True
    
    return False

  def move_tail(self):
    H_pos = np.where(self.head_positions == 'H')
    T_pos = np.where(self.tail_positions == 'T')

    diff = tuple([x-y for x,y in zip(H_pos,T_pos)])

    for x, y in zip(*T_pos):
      self.tail_positions[x, y] = self.tail_positions[x, y].lower()
      
    if diff[0] == 0: 
      self.tail_positions[x, y - diff[1]] = 'T'
      
    elif diff[1] == 0:
      self.tail_positions[x - diff[0], y] = 'T'
      
    else:
      

  def move_head(self, move):
    '''
    move_head uses move instructions to move the H position
    '''
    if move[0] == 'R':
      t = [0, 1]
    elif move[0] == 'L':
      t = [0, -1]
    elif move[0] == 'U':
      t = [1, 0]
    elif move[0] == 'D':
      t = [-1, 0]

    for step in range(move[1]):
      for x, y in zip(*pos):
        pos = np.where(self.head_positions == 'H')
        # pos = list(zip(pos[0], pos[1]))table
        for x, y in zip(*pos):
          self.head_positions[x, y] = self.head_positions[x, y].lower()
          
        self.head_positions[x + t[0], y + t[1]] = 'H'

        while not self.is_tail_adjacent():
          self.move_tail()

      
R = Rope()
print(R)
