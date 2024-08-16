from copy import deepcopy
import pprint
pp = pprint.PrettyPrinter(indent=4)

def read_input(filename):
  with open(filename, 'r') as f:
    parts = f.read().split('\n\n')

  crate_lines = parts[0].split('\n')
  moves = parts[1].split('\n')

  slot_len = 4
  max_line_len = max([len(line) for line in crate_lines])

  num_crates = max_line_len // slot_len + 1
  crates = [[] for _ in range(num_crates)]

  for line in crate_lines:
    slots = [line[i:i+slot_len-1] for i in range(0,len(line), slot_len)]
    for num, slot in enumerate(slots):
      if slot.strip():
        crates[num].append(slot.strip().strip('[]'))
      # else:
      #   crates[num].append(None)

  stack = {}
  for crate in crates:
    key = int(crate.pop(-1))
    _ = crate.reverse()
    stack.setdefault(key,crate)

  parsed_moves = []
  for move_line in moves:
    words = move_line.split()
    parsed_moves.append({
      words[0]:int(words[1]),
      words[2]:int(words[3]),
      words[4]:int(words[5])
    })

  return stack, parsed_moves

def output_result(stack):
  letters = []
  for num in range(len(stack)):
    if stack[num+1]:
      letters.append(stack[num+1][-1])
    else:
      letters.append(' ')
  return ''.join(letters)

def part_one(stack,moves):
  # CrateMover 9000
  for move in moves:
    for _ in range(move['move']):
      val = stack[move['from']].pop()
      stack[move['to']].append(val)

  return output_result(stack)


def part_two(stack,moves):
 # CrateMover 9001
  for move in moves:
    num_blocks_to_move = move['move']

    # Remove the blocks from the source stack
    blocks_to_move = stack[move['from']][-num_blocks_to_move:]
    del stack[move['from']][-num_blocks_to_move:]

    # Add the blocks to the destination stack
    stack[move['to']].extend(blocks_to_move)

  return output_result(stack)


def main():
  input_stack, moves = read_input("../in/5.in")
  stack_part_one = deepcopy(input_stack)
  stack_part_two = deepcopy(input_stack)
  # Deepcopy was used because changed to input stack in part one persist even
  # if inputstack isn't returned or global.

  result_one = part_one(stack_part_one, moves)
  print(f"Part One: {result_one}")

  result_two = part_two(stack_part_two, moves)
  print(f"Part Two: {result_two}")

if __name__ == "__main__":
  main()
