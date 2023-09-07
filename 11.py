import pprint

pp = pprint.PrettyPrinter(indent=4)


def read_input(filename):
  with open(filename, 'r') as f:
    data = f.read().strip()
    data = [[line.strip() for line in paragraph.split('\n')]
            for paragraph in data.split('\n\n')]
  return data

def string_to_lambda(equation):
    equation = equation.strip()
    equation = equation.replace("new", "")
    equation = equation.replace("old", "x")
    equation = equation.replace("=", "")
    equation = equation.strip()
    return eval(f"lambda x: {equation}")


def part_one(data):
  # Your code for part one goes here
  ID = []
  ITEMS = []
  OPS = []
  TESTS = []
  DIV = []
  TRUE = []
  FALSE = []
  COUNTERS = []

  for index, monkey in enumerate(data):
    parsed_monkey = [*map(lambda x: x.split(': '), monkey)]
    
    id = index
    starting_items = [*map(int,parsed_monkey[1][1].split(','))]
    operation = string_to_lambda(parsed_monkey[2][1])
    _, test_num = parsed_monkey[3][1].split("divisible by ")
    # test = lambda x: not (x % int(test_num))
    def test_function(x, tn=int(test_num)):
            return not (x % tn)
    
    _, destination_if_true = parsed_monkey[4][1].split("throw to monkey ")
    _, destination_if_false = parsed_monkey[5][1].split("throw to monkey ")

    ID.append(id)
    ITEMS.append(starting_items)
    OPS.append(operation)
    TESTS.append(test_function)
    DIV.append(int(test_num))
    TRUE.append(int(destination_if_true))
    FALSE.append(int(destination_if_false))
    COUNTERS.append(0)
  
  lcm = 1
  for div in DIV:
    lcm *= div
  for _ in range(10000):
    for monkey in range(len(ID)):
      while ITEMS[monkey]:
        item = ITEMS[monkey].pop(0)
        monkey_operation = OPS[monkey]
        worry_level = monkey_operation(item) % lcm
        # worry_level = worry_level // lcm
        monkey_test = TESTS[monkey]
        destination_monkey = TRUE[monkey] if monkey_test(worry_level) else FALSE[monkey]
        ITEMS[destination_monkey].append(worry_level)
        COUNTERS[monkey] += 1
  
  counters = []
  sorted_counters = sorted(COUNTERS, reverse=True)
  result = sorted_counters[0] * sorted_counters[1]
  return result


def part_one_dict(data):
  # Your code for part one goes here
  monkey_structure = {
      'id' : None,
      'Starting Items': [],
      'Operation': None,
      'Test': None,
      True : None,
      False : None,
      "inspection_counter" : 0
                      }
  monkeys = []
  for index, monkey in enumerate(data):
    parsed_monkey = [*map(lambda x: x.split(': '), monkey)]
    
    id = index
    starting_items = [*map(int,parsed_monkey[1][1].split(','))]
    operation = string_to_lambda(parsed_monkey[2][1])
    _, test_num = parsed_monkey[3][1].split("divisible by ")
    # test = lambda x: not (x % int(test_num))
    def test_function(x, tn=int(test_num)):
            return not (x % tn)
    
    _, destination_if_true = parsed_monkey[4][1].split("throw to monkey ")
    _, destination_if_false = parsed_monkey[5][1].split("throw to monkey ")

    monkey = monkey_structure.copy()
    monkey['id'] = id
    monkey['Starting Items'] = starting_items
    monkey['Operation'] = operation
    monkey['Test'] = test_function
    monkey[True] = int(destination_if_true)
    monkey[False] = int(destination_if_false)
  
    monkeys.append(monkey)

  for _ in range(20):
    for monkey in monkeys:
      for item in monkey['Starting Items']:
        monkey_operation =monkey['Operation']
        worry_level = monkey_operation(item) // 3
        monkey_test = monkey['Test']
        destination_monkey = monkey[monkey_test(worry_level)]
        monkeys[destination_monkey]['Starting Items'].append(worry_level)

  counters = []
  for monkey in monkeys:
    counters.append(monkey["inspection_counter"])
  sorted_counters = sorted(counters, reverse=True)
  result = sorted_counters[0] * sorted_counters[1]
  return result


def part_two(data):
  # Your code for part two goes here
  result = 0
  return result


def main():
  input_data = read_input("in/11.in")

  result_one = part_one(input_data)
  print(f"Part One: {result_one}")

  result_two = part_two(input_data)
  print(f"Part Two: {result_two}")


if __name__ == "__main__":
  main()
