from functools import reduce


def common_chars(*strings):
  # Convert each string to a set of its characters
  sets = map(set, strings)
  # Compute the intersection of all sets
  common = reduce(set.intersection, sets)
  return ''.join(common)


# First set of strings
strings1 = ("vJrwpWtwJgWrhcsFMMfFFhFp", "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
            "PmmdzqPrVvPwwTWBwg")

# Second set of strings
strings2 = ("wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn", "ttgJtRGJQctTZtZT",
            "CrZsJsPPZsGzwwsLwLmpwMDw")

print(common_chars(*strings1))
print(common_chars(*strings2))
