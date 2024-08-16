
#!/usr/bin/python3
# Advent of Code 2022

import sys
from pprint import pprint

input = sys.argv[1] if len(sys.argv)>1 else './input/day11.txt'
with open(input, 'r') as f:
    data = []
    for line in f:
        data.append([int(x) for x in list(line.strip())])

rows = len(data)
cols = len(data[0])
count = 0

def flash(r,c):
    global count
    count += 1
    data[r][c] = -1
    for dr in [-1,0,1]:
        for dc in [-1,0,1]:
            rr = r+dr
            cc = c+dc
            if 0<=rr<rows and 0<=cc<cols and data[rr][cc]!=-1:
                data[rr][cc] += 1
                if data[rr][cc] >= 10:
                    flash(rr,cc) 
    

if __name__ == '__main__':
    t = 0
    while True:
        t += 1
        # print("Step: " + str(t))
        # pprint(data)

        # Increment
        for r in range(rows):
            for c in range(cols):
                data[r][c] +=1
        # Flash
        for r in range(rows):
            for c in range(cols):
                if data[r][c] == 10:
                    flash(r,c)
        
        for r in range(rows):
            for c in range(cols):
                if data[r][c] < 0:
                    data[r][c] = 0
        
        all_flash = True
        for r in range(rows):
            for c in range(cols):
                if data[r][c] != 0:
                    all_flash = False
                    continue
        if t == 100:
            print(count)
        
        if all_flash:
            print(t)
            break



    # mask = [[0 for c in cols] for r in rows]