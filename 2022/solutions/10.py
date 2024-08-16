class Register:

  def __init__(self, val):
    self.values_archive = []
    self.value = val
    self.values_archive.append(self.value)
    self.cycle = 1
    self.signal_strength = 0
    self.signal_strength_archive = []
    self.programme = []
    self._import_data_()

    self.crt_len = 40
    self.crt_high = 6
    self.CRT = [' ' for ii in range(self.crt_len * self.crt_high)]

  def __repr__(self):

    CRT = self.CRT.copy()
    for ii in range(self.crt_high):
      line = []
      for jj in range(self.crt_len):
        line.append(CRT.pop(0))
      print("".join(line))
    return "Part 1: " + str(sum(self.signal_strength_archive))

  def _import_data_(self):
      with open('../in/10.in') as file:
        lines = file.read().strip().split('\n')
        parsed_lines = [(line.split()[0],
                       int(line.split()[1]) if len(line.split()) > 1 else None)
                      for line in lines]
        self.programme = parsed_lines

  def _cycle_up_(self):
    self.values_archive.append(self.value)
    self.cycle += 1
    # Part 1
    if self.cycle in [20, 60, 100, 140, 180, 220]:
      self.signal_strength = self.cycle * self.value
      self.signal_strength_archive.append(self.signal_strength)
    # Part 2
    sprite = [self.value - 1 + ii for ii in range(3)]
    if (self.cycle % self.crt_len - 1) in sprite:
      self.CRT[self.cycle - 1] = '#'

  def addx(self, val):
    '''
    Takes two cycles to run
    '''
    self._cycle_up_()
    self.value += val
    self._cycle_up_()

  def noop(self):
    '''
    Value is unaffected
    '''
    self._cycle_up_()

  def run(self):
    for line in self.programme:
      if line[0] == 'addx':
        self.addx(line[1])
      elif line[0] == 'noop':
        self.noop()


X = Register(1)
X.run()
print(X)
