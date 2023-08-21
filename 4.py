with open('in/4.input') as file:
  lines = [line.split(',') for line in file.read().strip().split('\n')]

### Part 1
overlap_count = 0
for line1, line2 in lines:
  range_1 = tuple(int(x) for x in line1.split('-'))
  range_2 = tuple(int(x) for x in line2.split('-'))

  set_1 = {*range(range_1[0], range_1[1] + 1)}
  set_2 = {*range(range_2[0], range_2[1] + 1)}
  common = set_1 & set_2

  lengths = [len(set_1), len(set_2)]

  if len(common) in lengths:
    overlap_count += 1

print('Part 1:  ' + str(overlap_count))

### Part 2
overlap_count = 0
for line1, line2 in lines:
  range_1 = tuple(int(x) for x in line1.split('-'))
  range_2 = tuple(int(x) for x in line2.split('-'))

  set_1 = {*range(range_1[0], range_1[1] + 1)}
  set_2 = {*range(range_2[0], range_2[1] + 1)}
  common = set_1 & set_2

  if len(common) > 0:
    overlap_count += 1

print('Part 2:  ' + str(overlap_count))