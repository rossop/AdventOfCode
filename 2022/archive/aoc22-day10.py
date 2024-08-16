from collections import defaultdict, Counter, deque
from operator import methodcaller
from typing import List
# TODO: add author of solutions that you are usin to improve on you previous solution


# def format(input):
#     return list(map(lambda w: ''.join(sorted(w)), input))

def split(word):
    return [char for char in word]

def command_check(stack, com):
    closing_coms = [ ')', '}', ']', '>']
    is_closing_dict = {')': '(',']': '[', '}': '{','>': '<'}
    e_weight = {')': 3,']': 57,'}': 1197,'>': 25137}
    val = 0
    if com not in closing_coms:
        stack.append(com)
        return stack, val
    else:
        if len(stack) > 0:
                if com in closing_coms:
                    if is_closing_dict[com] == stack[-1]:
                        stack.pop() 
                    else:
                        val = e_weight[com]
                        return stack, val
                else:
                    stack.append(com)
        else:
            if com not in closing_coms:
                stack.append(com)
            else:
                val = e_weight[com]
                return stack, val

    return stack,val

def autocomplete(stack):
    score = 0
    score_table = {')': 1, ']': 2,'}': 3,'>': 4,'(': 1, '[': 2,'{': 3,'<': 4}
    while len(stack) > 0 :
        com = stack.pop()
        score = score*5 + score_table[com]
    return score

        

if __name__ == '__main__':
    location_heights = []
    with open("./input/day10.txt", 'r') as f:
        lines = f.read().split('\n')
        # lines = [line.split() for line in lines] #TODO use lambda? 

lines = [*map(split, lines)]  
e_weight = {')': 3,']': 57,'}': 1197,'>': 25137}
is_closing_dict = {')': '(',']': '[', '}': '{','>': '<'}
# is_closing_dict = {'(': ')', '[' : ']', '{': '}','<': '>'}



# lines = [lines[0]]
scores = []
autocomplete_scores = []
#test
# lines = [split('{([(<{}[<>[]}>{[]{[(<()>')]
for l in lines:
    print(l)
    com_stack = deque()
    while len(l)>0:
        command = l.pop(0)
        print(com_stack),print(command)
        
        com_stack, val = command_check(com_stack, command)
        if val > 0:
            print(val)
            scores.append(val)
            break
    autocomplete_scores.append(autocomplete(com_stack))
    
print(scores)
print(sum(scores))

autocomplete_scores.sort()
print(autocomplete_scores)
print(autocomplete_scores[int(len(autocomplete_scores)/2)])
        # print(com_stack)