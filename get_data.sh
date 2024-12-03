#!/bin/bash

YEAR=2024
DAY=2

# Create directory if it doesn't exist
mkdir -p "$YEAR/in"

# Fetch main input
aocd $DAY $YEAR > "$YEAR/in/$(printf '%02d' $DAY).in"

# Fetch test input if available
aocd $DAY $YEAR --example > "$YEAR/in/$(printf '%02d' $DAY).test" 2>/dev/null || echo "No test input available for day $DAY of year $YEAR."