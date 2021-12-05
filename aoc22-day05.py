
import numpy as np
from operator import methodcaller
# def check_for_bingo(arr : np.array) -> bool:
#     return False

def straight_lines_filter(vecs): #TODO rename
    vec1, vec2 = vecs
    if 0 in vec1-vec2:
        return True
    else:
        return False

if __name__ == '__main__':
    with open("./input/day05_test.txt", 'r') as f:
        vector_strings = [[y for y in x.split(' -> ')] for x in f.read().split('\n')]
    list_of_vectors = [[*map(methodcaller('split',','), list_of_strings)] 
        for list_of_strings in vector_strings]
        
    list_of_string_arrays = [[*map(np.array, l)] for l in list_of_vectors]
    list_of_arrays = [[*map(methodcaller('astype', int), l)] 
        for l in list_of_string_arrays]
    
    #Create cordinates
        # max_c_value = 
        # max_x_value = 
        # create a np.array(max_c_pos, max_r,pos)
        #

    print(list_of_arrays)
    #Part 1 filter straight lines
    straight_arrays = [*filter(straight_lines_filter, list_of_arrays)]
    print(straight_arrays)

    #increase values in sub arrays that are identified by vectos

    #Part 2 


    #TODO rename all variable