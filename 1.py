# with open('in/1.test') as file:
#   lines = file.read().split('\n\n')
#   elves = [[int(num) for num  in line.split('\n')] for line in lines]

# print([*map(sum(), elves)])

with open('in/1.input') as file:
  lines = file.read().strip().split('\n\n')
  elves = [[int(num) for num in line.split('\n')] for line in lines]

# print([sum(elf) for elf in elves])
# print(max(sum(elf) for elf in elves))
total_calories_per_elf = list(map(sum, elves))
print('Part 1:  ' + str(max(total_calories_per_elf)))

sorted_lst = sorted(total_calories_per_elf, reverse=True)
top_3 = sorted_lst[:3]
print('Part 2:  ' + str(sum(top_3)))