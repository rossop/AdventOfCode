#!/usr/bin/python3
from os import initgroups
import sys
import itertools
from itertools import islice
from collections import defaultdict, Counter, deque
sys.setrecursionlimit(int(1e6))
from pprint import pprint
import re


input = sys.argv[1] if len(sys.argv)>1 else './input/21.test'


if __name__ == '__main__':
    with open(input, 'r') as f:
        player_string = f.read().strip()
        regex = r"\bPlayer\b\s(\d)\s\bstarting\sposition:\s\b(\d+)"
        matches = re.finditer(regex, player_string, re.MULTILINE)

        starting = {}

        for matchNum, match in enumerate(matches, start=1):
            a,b = match.groups()
            starting[int(a)] = int(b) #Player: Starting pos #TODO revise regex 
    
    print(starting)

    board_sz = 10
    dice_counter = 0
    player = 1
    ii = 1
    
    flag = False
    while not flag:
        die_rolled = [(ii+jj)%100 for jj in [0,1,2]]
        roll = sum(die_rolled)
        dice_counter += 3
        if ii%2 == 0:
            starting[1] += roll%board_sz +1
        else:
            starting[2] += roll%board_sz +1

        if starting[2] >= 1000:
            print(starting[1] * dice_counter)
            print(starting)
            flag = True
            break

        elif starting[1] >= 1000:
            print(starting[2] * dice_counter)
            print(starting)
            flag = True
            break
        print(starting)
        ii += 3
