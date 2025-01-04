# Advent of Code Solutions
| Year | Days Badge | Stars Badge |
|------|------------|-------------|
| 2019 | ![2019 Days](https://img.shields.io/badge/days%20completed-7-red) | ![2019 Stars](https://img.shields.io/badge/stars%20⭐-15-yellow) |
| 2020 | ![2020 Days](https://img.shields.io/badge/days%20completed-10-red) | ![2020 Stars](https://img.shields.io/badge/stars%20⭐-22-yellow) |
| 2021 | ![2021 Days](https://img.shields.io/badge/days%20completed-18-red) | ![2021 Stars](https://img.shields.io/badge/stars%20⭐-38-yellow) |
| 2022 | ![2022 Days](https://img.shields.io/badge/days%20completed-14-red) | ![2022 Stars](https://img.shields.io/badge/stars%20⭐-29-yellow) |
| 2023 | ![2023 Days](https://img.shields.io/badge/days%20completed-25-red) | ![2023 Stars](https://img.shields.io/badge/stars%20⭐-50-yellow) |
| 2024 | ![2024 Days](https://img.shields.io/badge/days%20completed-25-red) | ![2024 Stars](https://img.shields.io/badge/stars%20⭐-50-yellow) |

This repository contains my solutions for the Advent of Code (AoC) challenges, for the years 2019 to 2024. The structure is designed to organize inputs, solutions, and tests efficiently, facilitating quick access and understanding of each day's challenge.

Note: Inputs are personalized to your user account and are protected by copyright. Please do not share them here. Create an account at adventofcode.com to download your own inputs.

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
│       ├── 01.py            # Solution script for Day 1
│   ...
│
├── get_data.sh             # Script for dowloading demo and main input
├── templates/
├── utils/
│   ├── fetch.py            # Fetch data from aoc (using aocd)
│   ├── get_input.py        # Get input. Load input from in/ directory.
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

