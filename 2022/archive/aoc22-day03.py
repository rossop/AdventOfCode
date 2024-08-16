
import numpy as np
from decimal import localcontext, Decimal, ROUND_HALF_UP


f = open("./input/day03.txt", 'r')
l = [x.split(' ')[0] for x in f.read().splitlines()] #TODO

# l = ["00100","11110", "10110","10111","10101","01111","00111","11100","10000","11001","00010","01010"]

arr_l = np.array([list(string) for string in l])
arr_l = arr_l.astype(np.int64)

bin_gamma_rate = ''
bin_epsilon_rate = ''

counter = np.sum(arr_l, axis=0)
print(counter)
length = len(l)

for ii in range(len(counter)):
    if counter[ii] < length/2:
        bin_gamma_rate += "0"
        bin_epsilon_rate += "1"
    else:
        bin_gamma_rate += "1"
        bin_epsilon_rate += "0"        

#List approach
    # for num in l:
    #     zeros = num.count("0")
    #     ones = num.count("1")
    #     if zeros > ones:
    #         bin_gamma_rate += "0"
    #         bin_epsilon_rate += "1"
    #     else: 
    #         bin_gamma_rate += "1"
    #         bin_epsilon_rate += "0"


gamma_rate = int(bin_gamma_rate,2)
epsilon_rate = int(bin_epsilon_rate,2)
power_consumption = gamma_rate * epsilon_rate
# print(power_consumption)

# Part 2
oxygen_generator_rating = 0
CO2_scrubber_rating = 0

# Analyse Diagnostic Report
#TODO do this with recursion

col = 0
arr_l_1 = arr_l
with localcontext() as ctx:
    ctx.rounding = ROUND_HALF_UP
    while len(arr_l_1) > 1 and col < len(l[0]):
        count = arr_l_1[:,col].sum()
        ratio = float(count) / len(arr_l_1[:,col])
        num = int(Decimal(ratio).to_integral_value())
        pos = np.where(arr_l_1[:,col] != num)
        arr_l_1 = np.delete(arr_l_1, pos, axis=0)
        print(arr_l_1)
        col += 1

oxygen_generator_rating_bin = ''.join([*map(str,arr_l_1[0])])
print(oxygen_generator_rating_bin)
oxygen_generator_rating = int(oxygen_generator_rating_bin,2)
print(oxygen_generator_rating)


col = 0
arr_l_2 = arr_l
with localcontext() as ctx:
    ctx.rounding = ROUND_HALF_UP
    while len(arr_l_2) > 1 and col < len(l[0]):
        count = arr_l_2[:,col].sum()
        ratio = float(count) / len(arr_l_2[:,col])
        num = int(Decimal(ratio).to_integral_value())
        pos = np.where(arr_l_2[:,col] == num)
        arr_l_2 = np.delete(arr_l_2, pos, axis=0)
        print(arr_l_2)
        col += 1

CO2_scrubber_rating_bin = ''.join([*map(str,arr_l_2[0])])
CO2_scrubber_rating = int(CO2_scrubber_rating_bin,2)
print(CO2_scrubber_rating)


# oxygen_generator_rating = int(bin_epsilon_rate,2)


life_support_rating = oxygen_generator_rating * CO2_scrubber_rating
print(life_support_rating)