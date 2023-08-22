with open('in/6.input') as file:
  signals = file.read().strip().split('\n')


def find_marker(signal: str, length: int) -> int:
  for marker_pos in range(len(signal) - length):
    marker = signal[marker_pos:marker_pos + length]
    if len(set(marker)) == length:
      return marker_pos + length


print('Part 1:  ' + str(find_marker(signals[0], 4)))
print('Part 1:  ' + str(find_marker(signals[0], 14)))
