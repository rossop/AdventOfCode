f = open("./input/day02.txt", 'r')
l = [x.split(' ') for x in f.read().splitlines()]
test_l = [["forward","5"],["down","5"],["forward", "8"],["up","3"],["down", "8"],
["forward", "2"]]
depth = 0
pos = 0

for move in l:
    dir = move[0]
    step = int(move[1])
    if dir == 'forward':
        pos += step
    elif dir == 'down':
        depth += step
    elif dir == 'up':
        depth -= step
print(depth)
print(pos)
print(depth*pos)

# Part 2
depth = 0
pos = 0
aim = 0
for move in l:
    dir = move[0]
    step = int(move[1])
    if dir == 'forward':
        pos += step
        depth += aim * step
    elif dir == 'down':
        aim += step
    elif dir == 'up':
        aim -= step
print(depth)
print(pos)
print(depth*pos)