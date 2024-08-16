
import numpy as np
from operator import methodcaller
from typing import List

def straight_lines_filter(vecs): #TODO rename
    vec1, vec2 = vecs
    if 0 in vec1-vec2:
        return True
    else:
        return False

def range_dir(start, end):
    if start <= end:
        return range(start,end+1)
    elif start > end:
        return range(start,end-1,-1)

def find_bounds(vecs : List[List[np.array]]): #TODO arrage typing 
    concat_vecs = np.concatenate(vecs)
    # vec_r_min = concat_vecs[:,0].min()
    # vec_c_min = concat_vecs[:,0].min()
    vec_r_max = concat_vecs[:,0].max()
    vec_c_max = concat_vecs[:,0].max()

    return vec_c_max + 1, vec_r_max + 1

def mark_lines(sea_arr : np.array, vec: List[np.array]):
    if 0 == ((vec[0]-vec[1])[1]):
        c = vec[0][1]
        for r in range_dir(vec[0][0], vec[1][0]):
            try:
                sea_arr[c,r] += 1
            except:
                print(c,r)
    elif 0 == ((vec[0]-vec[1])[0]):
        r = vec[0][0]
        for c in range_dir(vec[0][1], vec[1][1]):
            try:
                sea_arr[c,r] += 1
            except:
                print(c,r)
    else: 
        for r,c in zip(range_dir(vec[0][0], vec[1][0]),range_dir(vec[0][1], vec[1][1])):
            try:
                sea_arr[c,r] += 1
            except:
                print(c,r)


if __name__ == '__main__':

    with open("./input/day05.txt", 'r') as f:
        vector_strings = [[y for y in x.split(' -> ')] for x in f.read().split('\n')]


    list_of_vectors = [[*map(methodcaller('split',','), list_of_strings)] 
        for list_of_strings in vector_strings]
    list_of_string_arrays = [[*map(np.array, l)] for l in list_of_vectors]
    list_of_arrays = [[*map(methodcaller('astype', int), l)] 
        for l in list_of_string_arrays]
    
    
    
    #Part 1 filter straight lines
    sea_arr = np.zeros(find_bounds(list_of_arrays))
    straight_arrays = [*filter(straight_lines_filter, list_of_arrays)]
    for arr in straight_arrays:
        mark_lines(sea_arr,arr)

    print(len(np.where((sea_arr>=2))[0]))

    #Part 2 
    sea_arr = np.zeros(find_bounds(list_of_arrays))
    for arr in list_of_arrays:
        mark_lines(sea_arr,arr)

    print(len(np.where((sea_arr>=2))[0]))
