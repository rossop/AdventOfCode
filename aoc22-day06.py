
import matplotlib.pyplot as plt
import numpy as np

def reproduction(school: np.array) -> np.array:
    school = laternfish_school - 1
    new_fish = [8]
    reproducing_fish = np.where(school == -1)[0]
    new_school = np.append(school, new_fish*len(reproducing_fish))
    new_school[new_school==-1] = 6
    return new_school

# Preprocessing part 2
def frequency_count(school: np.array) -> np.array:
    unique_school, frequency_school = np.unique(school, return_counts = True)
    school_frequency = np.zeros(9)
    
    for ii, val in enumerate(frequency_school):
        school_frequency[unique_school[ii]] = val

    return school_frequency

def reproduction_ver2(school_frequency) -> np.array:
    pregnant_lanterfish = school_frequency[0]

    old_fish = school_frequency[0:7]
    young_fish = school_frequency[7:9]
    
    old_fish = np.roll(old_fish,-1)
    old_fish[-1] += young_fish[0]
    young_fish = np.roll(young_fish,-1)
    young_fish[-1] = pregnant_lanterfish
    
    return np.concatenate([old_fish,young_fish])



if __name__ == '__main__':
    with open("./input/day06.txt", 'r') as f:
        laternfish_school = [*map(int,f.read().split(','))]

    laternfish_school = np.array(laternfish_school)
    laternfish_school_initial = laternfish_school.copy()
    end_time = 80 # days 80, 256

    for val in range(end_time):
        laternfish_school = reproduction(laternfish_school)

    #Part 2
    f_laternfish_school = frequency_count(laternfish_school_initial)
    for ii in range(256):
        f_laternfish_school = reproduction_ver2(f_laternfish_school)

    print(f_laternfish_school.sum())