import pprint
pp = pprint.PrettyPrinter(indent=4)

def read_input(filename):
  with open(filename, 'r') as f:
    data = f.read().strip().split('\n\n')
  return [list(map(eval, line.strip().split('\n'))) for line in data]

def compare(a,b):
  '''
  Using 1,0,-1 allows to consider both True False and Carry-on conditions 
  when are outside of a loop
  '''
  if isinstance(a, int) and isinstance(b, int):
    if a < b:
      return -1
    elif a == b:
      0
    elif a > b:
      return 1

  elif isinstance(a, list) and isinstance(b, list):
    for ai, bi in zip(a,b):
      c = compare(ai, bi)
      if c == -1:
        return -1
      elif c == 1:
        return 1
    
    if len(a) < len(b):
      return -1
    elif len(b) < len(a):
      return 1
    else:
      return 0
  elif isinstance(a, int) and isinstance(b, list):
    return compare([a], b)
  else:
    return compare(a, [b])

  


def part_one(data):
  '''
  Part one code
  '''
  packets = []
  result = 0
  for num, pair in enumerate(data, start=1):
    if compare(*pair) == -1:
      result += num
    packets.append(pair[0])
    packets.append(pair[1])

  return result, packets

def sort_packets(data):
  pass

def find_divider_packets(sorted_data, divider_packets):
  pass

def part_two(data):
  '''
  Part two code
  '''
  divider_packets = [[[2]],[[6]]]
  data.appened(divider_packets[0])
  data.appened(divider_packets[1])

  sorted_data = sort_packets(data)
  pos = find_divider_packets(sorted_data, divider_packets)
  result = pos[0] * pos[1]
  return result


def main():
  input_data = read_input("in/13.in")

  result_one, input_data_part2 = part_one(input_data)
  print(f"Part One: {result_one}")

  result_two = part_two(input_data_part2)
  print(f"Part Two: {result_two}")


if __name__ == "__main__":
  main()