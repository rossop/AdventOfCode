#!/usr/bin/python3
from os import initgroups
import sys
import itertools
from collections import defaultdict, Counter, deque
sys.setrecursionlimit(int(1e6))
from pprint import pprint

input = sys.argv[1] if len(sys.argv)>1 else './input/20_test.txt'

def show(img):
    r_min = min([r for r,c in img])
    r_max = max([r for r,c in img])
    c_min = min([c for r,c in img])
    c_max = max([c for r,c in img])
    for r in range(r_min-5, r_max+5):
        row = ''
        for c in range(c_min-5, c_min+5):
            if (r,c) in img:
                row += '#'
            else:
                row += ' '
        print(row)

def step(img, on):
    img_output = set()
    r_min = min([r for r,c in img])
    r_max = max([r for r,c in img])
    c_min = min([c for r,c in img])
    c_max = max([c for r,c in img])

    for r in range(r_min-5,r_max+5):
        for c in range(c_min-5,c_max+5):
            code = ''
            for dr in range(-1,2):
                for dc in range(-1,2):
                    if ( (r+dr,c+dc) in img ) == on:
                        code += '1'
                    else:
                        code += '0'
            bin_code = ["0" if c=='.' else "1" for c in code]
            dec_code = int(''.join(bin_code),2)
            assert 0 <= dec_code < 512
            if (iea[dec_code] == '#') != on:
                img_output.add((r,c))
    
    return img_output
        

if __name__ == '__main__':
    with open(input, 'r') as f:
        iea, input_img = f.read().strip().split('\n\n')
        iea = iea.strip()
        assert len(iea) == 512
        img = set()
        for r, line in enumerate(input_img.strip().split('\n')):
            for c,x in enumerate(line.strip()):
                if x == '#':
                    img.add((r,c))
                    
    # output_img = input_img.copy()
    for t in range(2):
        if t == 2:
            print(len(img))
        on = t%2 == 0
        img = step(img,on)
        # show(img)
    print(len(img))



