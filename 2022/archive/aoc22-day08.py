import numpy as np
from operator import methodcaller
from typing import List

def get_specific_elements_of_nested_list(element,vals):
    # https://stackabuse.com/python-get-number-of-elements-in-a-list/
    count = 0
    if isinstance(element, list):
        for each_element in element:
            count += get_specific_elements_of_nested_list(each_element,vals)
    else:
        if element in vals:
            count += 1  
    return count

def sum_numbers(element,reading_key):
    # https://stackabuse.com/python-get-number-of-elements-in-a-list/
    count = 0
    len_key = {2:'1', 4:'4', 3:'7', 5:'8'}
    if any(isinstance(x, list) for x in element):
        for each_element in element:
            count += sum_numbers(each_element,reading_key)
    else:
        digits = element[:]
        for ii, each_element in enumerate(element):
            if each_element in [*reading_key.keys()]:
                digits[ii] = reading_key[each_element]
            else:
                digits[ii] = len_key[len(each_element)]
                        
        count += int(''.join(digits))
    return count

def same_permutation(str1, str2):
    d = collections.defaultdict(int)
    for x in str1:
        d[x] += 1
    for x in str2:
        d[x] -= 1
    return not any(d.itervalues())


def ispermutation(str1, str2):
    threshold = 10000
    returnvalue = false
    if len(stra) == len(str2):
    if len(stra) < threshold:
        returnvalue = (sorted(str1) == sorted(str2))
    else:
        returnvalue = same_permutation(str1, str2)
    return returnvalue


if __name__ == '__main__':
    with open("./input/day08_test.txt", 'r') as f:
        input = [x.split(' | ') for x in f.read().split('\n')]

    commands = input[:]
    strips_counter = commands
    for ii,com in enumerate(commands):
        commands[ii] = [*map(methodcaller('split', ' '), com)]
        strips_counter[ii][0] = [*map(len, commands[ii][0])]
        strips_counter[ii][1] = [*map(len, commands[ii][1])]
    
    # Remove front digits
    for counter_list in strips_counter:
        counter_list.pop(0)

    print(get_specific_elements_of_nested_list(strips_counter,[2,4,3,7]))

    # Part 2
    commands = input[:]
    reading_key = {'cedgfb': '8', 'cdfbe': '5', 'gcdfa': '2', 'fbcad': '3', 
            'dab': '7', 'cefabd': '9', 'cdfgeb': '6', 'eafb': '4', 'cagedb': '0', 'ab': '1'}
        
    for ii,com in enumerate(commands): #TODO avoid redoing this by fixing overwriting in line 33 34
        commands[ii] = [*map(methodcaller('split', ' '), com)]
        com.pop(0)

    print(sum_numbers(commands,reading_key))
    

    



