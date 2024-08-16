
import numpy as np
from operator import methodcaller
# def check_for_bingo(arr : np.array) -> bool:
#     return False

def sum_col(arr : np.array) -> None: #TODO use lambda
    arr.sum(axis=0)
    print(type(arr))
    print(arr)

def create_mask(arr : np.array) -> np.array:
    
    array_shape = arr.shape
    mask = np.zeros(array_shape)

    return mask

def search_value(val:int, arr:np.array, arr_mask:np.array) -> None:
    
    pos = np.where(arr == val)
    arr_mask[pos] = 1

    return None

# def check_bingo(arr_l_masks : list[np.array]) -> bool:
# def check_bingo(arr_l_masks) -> tuple(bool, int):
def check_bingo(arr_l_masks):
    for ii, arr in enumerate(arr_l_masks):
        rows_status = list(arr.sum(axis=1))
        cols_status = list(arr.sum(axis=0))
        card_status = rows_status + cols_status
        if 5 in  card_status:
            return True, ii

    return False, 0

if __name__ == '__main__':
    with open("./input/day04.txt", 'r') as f:
        l = [[y for y in x.split('\n')] for x in f.read().split('\n\n')]

    # Process String of commands
    commands_string = l.pop(0)[0]
    commands = [*map(int,commands_string.split(','))]

    # Create list of boards
    l = [[*map(methodcaller('split'), string)] for string in l]
    int_l = []
    for lst in l:
        intermediate_l = []
        for list_of_strings in lst:
            intermediate_l.append([*map(int, list_of_strings)])
        int_l.append(intermediate_l[:])

    arr_l = [*map(np.array, int_l)]

    # Part 1
    # Simulate extraction executing command_list
    arr_l_masks = [*map(create_mask, arr_l)]
    bingo = False
    for val in commands:
        for ii in range(len(arr_l)):
            search_value(val, arr_l[ii], arr_l_masks[ii])
        bingo, arr_number = check_bingo(arr_l_masks)
        if bingo:
            unmarked_numbers = arr_l[arr_number]-arr_l[arr_number]*arr_l_masks[arr_number]
            sum_of_unmarked_numbers = unmarked_numbers.sum()
            print(val * sum_of_unmarked_numbers)
            break
        
    # Part 2
    # Simulate extraction executing command_list
    print(commands)
    winning_boards = []
    arr_l_masks = [*map(create_mask, arr_l)]
    for val in commands:
        for ii in range(len(arr_l)):
            search_value(val, arr_l[ii], arr_l_masks[ii])
        bingo, arr_number = check_bingo(arr_l_masks)
        if bingo:
            unmarked_numbers = arr_l[arr_number]-arr_l[arr_number]*arr_l_masks[arr_number]
            sum_of_unmarked_numbers = unmarked_numbers.sum()
            winning_boards.append((arr_l.pop(arr_number), arr_l_masks.pop(arr_number)))
            print((len(arr_l), val, sum_of_unmarked_numbers))
            print(unmarked_numbers)
            winning_stats = (val, sum_of_unmarked_numbers)


    print(winning_stats[0]*winning_stats[1])

