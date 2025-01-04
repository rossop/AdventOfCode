# Advent of Code Solutions
| Year | Days Badge | Stars Badge |
|------|------------|-------------|
| 2019 | ![2019 Days](https://img.shields.io/badge/days%20completed-7-red) | ![2019 Stars](https://img.shields.io/badge/stars%20⭐-15-yellow) |
| 2020 | ![2020 Days](https://img.shields.io/badge/days%20completed-10-red) | ![2020 Stars](https://img.shields.io/badge/stars%20⭐-22-yellow) |
| 2021 | ![2021 Days](https://img.shields.io/badge/days%20completed-18-red) | ![2021 Stars](https://img.shields.io/badge/stars%20⭐-38-yellow) |
| 2022 | ![2022 Days](https://img.shields.io/badge/days%20completed-14-red) | ![2022 Stars](https://img.shields.io/badge/stars%20⭐-29-yellow) |
| 2023 | ![2023 Days](https://img.shields.io/badge/days%20completed-25-red) | ![2023 Stars](https://img.shields.io/badge/stars%20⭐-50-yellow) |
| 2024 | ![2024 Days](https://img.shields.io/badge/days%20completed-25-red) | ![2024 Stars](https://img.shields.io/badge/stars%20⭐-50-yellow) |

This repository contains my solutions for the Advent of Code (AoC) challenges, specifically for the year 2024. The structure is designed to organize inputs, solutions, and tests efficiently, facilitating quick access and understanding of each day's challenge.

## Structure

The repository is organized as follows:

```
AdventOfCode/
├── 2024/
│   ├── in/
│   │   ├── 1.in            # Actual input for Day 1
│   │   ├── 1pt1.test       # Test input for Day 1, Part 1
│   │   ├── 1pt2.test       # Test input for Day 1, Part 2
│   ...
│   ├── solutions/
│       ├── 1.py            # Solution script for Day 1
│   ...
│
├── env/                    # Requirements for different venvs
├── templates/
├── utils/
│   ├── fetch.py            # Fetch data from aoc (using aocd)
│
├── README.md
├── .gitignore
```

## Quickstart

### Installation

Ensure you have Python installed on your system. This project uses the `advent-of-code-data` package to fetch puzzle data, making data retrieval straightforward and efficient.

To install the required package, run:

```bash
pip install advent-of-code-data
```

For Jupyter notebook users:

```bash
pip install 'advent-of-code-data[nb]'
```

### Configuration

Puzzle inputs are unique to each user and require your AoC session token for access. To set up your environment:

```bash
export AOC_SESSION=your_session_token_here
```

Windows users should use `set` instead of `export`.

### Using `advent-of-code-data`

Fetch today's puzzle data:

```python
from aocd import data
```

Or, fetch data for a specific day and year:

```python
from aocd import get_data
day_data = get_data(day=1, year=2024)
```

To save data directly to a file:

```bash
aocd > in/day01.in
```

### Running Solutions

Each day's solution can be executed individually. For example, to run the solution for Day 1:

```bash
python solutions/day01.py
```

## Automated Submission

The `advent-of-code-data` package supports automated submission of your solutions:

```python
from aocd import submit
submit(my_answer, part='a', day=1, year=2024)
```

## Feedback

If you have feedback, suggestions or improvements, feel free to open an issue or submit a pull request.
