#!/bin/bash

# Configuration
MEM_FILE="local_memory.txt"
LINES=20  # How many lines of history to show by default

# Color codes for pretty output
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RESET='\033[0m'

if [ ! -f "$MEM_FILE" ]; then
    echo -e "${YELLOW}!! No memory file found yet.${RESET}"
    exit 1
fi

echo -e "${CYAN}--- RECENT AI MEMORIES (Last $LINES lines) ---${RESET}"
echo "------------------------------------------------"

# Use 'tail' to get the last part of the file
# Use 'sed' to add a little bullet point to each entry
tail -n "$LINES" "$MEM_FILE" | sed 's/^/  ➜ /'

echo -e "\n${CYAN}------------------------------------------------${RESET}"
