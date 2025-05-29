#!/bin/bash
# Formatted git log with timestamps and aligned columns

# Get terminal width
COLS=$(tput cols 2>/dev/null || echo 80)

# Calculate space for rest of message
# Format: hash(7) + space + date(5) + space + time(5) + spaces(2) + agent(8) + space + state(15) + space = 46
REST_WIDTH=$((COLS - 46))
REST_WIDTH=$((REST_WIDTH < 20 ? 20 : REST_WIDTH))  # Minimum 20 chars

git log --pretty=format:'%h %ad %s' --date=format:'%m-%d %H:%M' -n "${1:-20}" | \
awk -v rest_width="$REST_WIDTH" '{
    # Extract parts
    hash = $1
    date = $2
    time = $3
    
    # Remove first 3 fields to get the message
    $1 = ""; $2 = ""; $3 = ""
    msg = substr($0, 4)
    
    # Parse agent and state
    agent = "-----"
    state = "-----"
    rest = msg
    
    if (match(msg, /@([A-Z0-9-]+):?\s*\[([^\]]+)\]\s*(.*)/, parts)) {
        agent = parts[1]
        state = parts[2]
        rest = parts[3]
    } else if (match(msg, /@([A-Z0-9-]+):?\s*(.*)/, parts)) {
        agent = parts[1]
        rest = parts[2]
    }
    
    # Truncate if needed
    if (length(agent) > 8) agent = substr(agent, 1, 7) "."
    if (length(state) > 15) state = substr(state, 1, 14) "."
    if (length(rest) > rest_width) rest = substr(rest, 1, rest_width - 3) "..."
    
    # Print formatted
    printf "%s %s %s  %-8s %-15s %s\n", hash, date, time, agent, state, rest
}'