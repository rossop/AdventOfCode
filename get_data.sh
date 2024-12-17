#!/bin/bash

# Get the current day and year if not supplied as arguments
DAY=${1:-$(date +%-d)}
YEAR=${2:-$(date +%Y)}

# Create directory if it doesn't exist
mkdir -p "$YEAR/in"

# Fetch main input
aocd $DAY $YEAR > "$YEAR/in/$(printf '%02d' "$DAY").in"

# Fetch test input if available
aocd $DAY $YEAR --example > "$YEAR/in/$(printf '%02d' "$DAY").test" 2>/dev/null || echo "No test input available for day $DAY of year $YEAR."