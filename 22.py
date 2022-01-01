#!/usr/bin/python3
from os import initgroups
import sys
import itertools
from itertools import islice
from collections import defaultdict, Counter, deque
sys.setrecursionlimit(int(1e6))
from pprint import pprint
import re


input = sys.argv[1] if len(sys.argv)>1 else './input/22.test2'


if __name__ == '__main__':
    with open(input, 'r') as f:
        reboot = f.read().strip().split('\n')
        # cuboid_regex = r'[\s|,][x-z]='
        # reboot = [re.split(cuboid_regex, s.strip()) for s in reboot]

    cuboid = set()

    for r, line in enumerate(reboot):    
        cmd, pos = line.split()
        regex = r"[+-]?\d+"
        x1, x2,y1,y2,z1,z2 = [int(x) for x in re. findall(regex, pos)]

        # x1 = max(x1,-50)
        # y1 = max(y1,-50)
        # z1 = max(z1,-50)
        # x2 = min(x2, 50)
        # y2 = min(y2, 50)
        # z2 = min(z2, 50)
        # print(x1,x2,y1,y2,z1,z2)
        X = [*range(x1,x2+1)]
        Y = [*range(z1,z2+1)]
        Z = [*range(y1,y2+1)]

        for x,y,z in itertools.product(X,Y,Z):
            if cmd == 'on':
                cuboid.add((x,y,z))
            else:
                assert cmd == 'off'
                cuboid.discard((x,y,z))
            
                    
    print(len(cuboid))