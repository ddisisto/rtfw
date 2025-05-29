#!/bin/bash
# Formatted git log with timestamps and aligned columns

git log --pretty=format:'%h %ad %s' --date=format:'%m-%d %H:%M' -n "${1:-20}" | \
awk '{
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
    if (length(rest) > 50) rest = substr(rest, 1, 49) "..."
    
    # Print formatted
    printf "%s %s %s  %-8s %-15s %s\n", hash, date, time, agent, state, rest
}'