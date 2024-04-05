def triangular(x):
    return abs(x)*(abs(x)+1)*0.5

if __name__ == '__main__':
    with open("./input/day07.txt", 'r') as f:
        crabs_positions = [*map(int,f.read().split(','))]

    lower_bound = min(crabs_positions)
    upper_bound = max(crabs_positions)

    # Part 1
    fuel_cost_estimations = []
    for ii in range(lower_bound,upper_bound+1):
        fuel_cost = [abs(x-ii) for x in crabs_positions]
        fuel_cost_estimations.append(sum(fuel_cost))

    # fuel_cost_arr = np.array(fuel_cost_estimations)
    min_fuel = min(fuel_cost_estimations)
    print(min_fuel)

    
    # Part 2
    fuel_cost_estimations = []
    for ii in range(lower_bound,upper_bound+1):
        fuel_cost = [triangular(x-ii) for x in crabs_positions]
        fuel_cost_estimations.append(sum(fuel_cost))

    min_fuel = min(fuel_cost_estimations)
    print(min_fuel)