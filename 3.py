from functools import reduce


def common_chars(*strings):
  # Convert each string to a set of its characters
  sets = map(set, strings)
  # Compute the intersection of all sets
  common = reduce(set.intersection, sets)
  return ''.join(common)


# def common_chars(str1, str2):
#   # Convert both strings to sets
#   set1 = set(str1)
#   set2 = set(str2)

#   # Use set intersection to find common characters
#   common = set1 & set2

#   return common.pop()


def letter_to_number(letter: str) -> int:
  if letter.isupper():
    return ord(letter) - ord('A') + 1 + 26
  else:
    return ord(letter) - ord('a') + 1


with open('in/3.input') as file:
  lines = file.read().strip().split('\n')

### Part 1

compartments_sum = 0
for line in lines:
  mid = len(line) // 2
  first_half = line[:mid]
  second_half = line[mid:]

  common_char = common_chars(first_half, second_half)
  compartments_sum += letter_to_number(common_char)

print('Part 1:  ' + str(compartments_sum))

### Part 2
compartments_sum = 0
for i in range(0, len(lines), 3):
  # Get the next three items
  items = lines[i:i + 3]
  compartments_sum += letter_to_number(common_chars(*items))

print('Part 2:  ' + str(compartments_sum))