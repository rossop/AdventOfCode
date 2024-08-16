#!/usr/bin/python3
# Advent of Code 2022
f = open("./input/day01.txt", 'r')
l = [int(x.split('\n')[0]) for x in f.readlines()]
#list = [199,200,208,210,200,207,240,269,260,263]
# Part 1
diff = []
for ii in range(len(l)-1):
    diff.append(l[ii+1] - l[ii])

pos_count = 0 
for val in diff:
    if val > 0:
        pos_count += 1

print(pos_count)

#Part 2
sliding_window_list = []
diff = []
for ii in range(len(l)-2):
    sliding_window_list.append(l[ii] + l[ii+1] + l[ii+2])

for ii in range(len(sliding_window_list)-1):
    diff.append(sliding_window_list[ii+1] - sliding_window_list[ii])

pos_count = 0 
for val in diff:
    if val > 0:
        pos_count += 1

print(pos_count)