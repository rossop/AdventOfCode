#!/usr/bin/python3
from os import initgroups
import sys
import itertools
from itertools import islice
from collections import defaultdict, Counter, deque
sys.setrecursionlimit(int(1e6))
from pprint import pprint
import re
import ast


input = sys.argv[1] if len(sys.argv)>1 else './input/24.test'

def inp(a=1): #???
    return a

def add(a,b):
    return a+b, b

def mul(a,b):
    return a*b, b 

def div(a,b):
    assert b != 0
    return a / b

def mod(a,b):
    assert a>=0
    assert b>0
    return a%b, b

def eql(a,b):
    return  int(a == b)

if __name__ == '__main__':
    with open(input, 'r') as f:
        commands = f.read().strip().split('\n')
        commands = [com.split() for com in commands]
        
        C = []
        for ii, com in enumerate(commands):
            c = com.copy()
            if len(c) == 3 and c[-1] not in 'wxyz':
                c[-1] = int(c[-1])
            C.append(c)
        
        w, x, y, z = 0, 0, 0, 0
        for ii, com in enumerate(C):
                op = ast.parse(com)
        print(C)