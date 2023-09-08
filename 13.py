import pprint
pp = pprint.PrettyPrinter(indent=4)

def read_input(filename):
  with open(filename, 'r') as f:
    data = f.read().strip().split('\n\n')
  return [list(map(eval, line.strip().split('\n'))) for line in data]


def compare_lists(list_a, list_b):
  '''
  Compare list_a to list_b. 
  list_b must be larger according to a series of conditions.
  RETURN 
    - TRUE if in the right order
    - FALSE if NOT in the right order
    TODO
      - diffrent types
      - first list longer than second
      - first list shorter than second
      - 
  '''
  for a, b in zip(list_a, list_b):
    print(' ')
    print('-----')
    print(a)
    print(b)
    print(' ')
    if isinstance(a, list) and isinstance(b, list):
      if not compare_lists(a, b):
        # print('isinstance(a and b, list)')
        # print(a)
        # print(b)
        # print(' ')
        return False
      else:
        if len(a) == len(b):
          continue
        elif len(list_a) > len(list_b):
          return False
        return True

    elif isinstance(a, int) and isinstance(b, int):
      # print('HERE')
      if a > b:
        # print('here >')
        return False
        
      elif a == b:
        # print('here =')
        continue
        
      elif a < b:
        # print('here <')
        return True

    elif isinstance(a, list):
      # print('isinstance(a, list)')
      if not compare_lists(a, [b]):
        return False

    elif isinstance(b, list):
      # print('isinstance(b, list)')
      if not compare_lists([a], b):
        return False

  if len(list_a) < len(list_b):
    # print('len(list_a) < len(list_b)')
    return True

  elif len(list_a) > len(list_b):
    # print('len(list_a) > len(list_b):')
    return False
  print(' ')
  print('here we are at the end')
  print(list_a)
  print(list_b)
  print(' ')
  return True


def part_one(data):
  '''
  Part one code
  '''
  print('##############')
  result = 0
  for num, pair in enumerate(data, start=1):
    print(f'This is problem number {num}')
    if compare_lists(*pair):
      result += num
      print('pass')

    else:
      print('not pass')

    print(' ')
    print('##############')
    print(' ')
    print(' ')
    print(' ')
    print('##############')
    print(' ')
  return result


def part_two(data):
  '''
  Part two code
  '''
  result = 0
  return result


def main():
  input_data = read_input("in/13.in")

  result_one = part_one(input_data)
  print(f"Part One: {result_one}")

  result_two = part_two(input_data)
  print(f"Part Two: {result_two}")


if __name__ == "__main__":
  main()

'''
[[[],2,8],[[9,[8,10,6,9,8],0,[10,7,9,5],[]],2,3,4,6]]
[[[[4,0,3,3]]],[10],[6,5,[10,[0,0,10,7],[9],0],6]]


##############
 
This is problem number 124
 
-----
[[], 2, 8]
[[[4, 0, 3, 3]]]
 
 
-----
[]
[[4, 0, 3, 3]]
 
not pass
 
##############
'''
