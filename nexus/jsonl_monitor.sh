#!/bin/bash
# NEXUS JSONL Session Monitor

SESSION_DIR="$HOME/.claude/projects/-home-daniel-prj-rtfw"
declare -A AGENT_FILES
declare -A LAST_SIZE

# Map agents to their session files
AGENT_FILES[code]="66a678dc-e43d-4db2-86c1-f93ea54b69ad.jsonl"
AGENT_FILES[gov]="6c859161-b569-4a87-a53e-3b88d6943c0d.jsonl"
AGENT_FILES[architect]="932ef584-cac9-4868-ae0b-30fed3de40e5.jsonl"
AGENT_FILES[research]="b607ed31-0de8-4db1-b3df-2a1bcaec0d66.jsonl"
AGENT_FILES[historian]="c4088511-fc4e-4916-bd88-c4ebf22ca138.jsonl"
AGENT_FILES[test]="bae725c1-5163-43ff-af08-d50ca01233e6.jsonl"

log_file="/tmp/nexus_jsonl_monitor.log"

echo "$(date): NEXUS JSONL Monitor Started" >> "$log_file"

# Initialize file sizes
for agent in "${!AGENT_FILES[@]}"; do
    file_path="$SESSION_DIR/${AGENT_FILES[$agent]}"
    if [ -f "$file_path" ]; then
        LAST_SIZE[$agent]=$(wc -l < "$file_path")
        echo "$(date): Initialized $agent at ${LAST_SIZE[$agent]} lines" >> "$log_file"
    fi
done

monitor_agent() {
    local agent=$1
    local file_path="$SESSION_DIR/${AGENT_FILES[$agent]}"
    
    if [ ! -f "$file_path" ]; then
        return
    fi
    
    current_size=$(wc -l < "$file_path")
    
    if [ "$current_size" -gt "${LAST_SIZE[$agent]}" ]; then
        echo "$(date): Activity detected in $agent session" >> "$log_file"
        
        # Get new lines since last check
        new_lines=$((current_size - LAST_SIZE[$agent]))
        latest_entries=$(tail -n "$new_lines" "$file_path")
        
        # Check for messages in the latest content
        while IFS= read -r line; do
            # Check if this is a user or assistant message with @FROM → @TO pattern
            if echo "$line" | jq -r '.message.content // empty' 2>/dev/null | grep -q "@.*→.*:"; then
                message=$(echo "$line" | jq -r '.message.content // empty' 2>/dev/null)
                echo "$(date): Inter-agent message detected from $agent: $message" >> "$log_file"
                
                # Extract target agent
                target=$(echo "$message" | sed -n 's/.*@[^→]*→[[:space:]]*@\?\([^:]*\):.*/\1/p' | tr '[:upper:]' '[:lower:]')
                if [ -n "$target" ] && [ "$target" != "$agent" ]; then
                    echo "$(date): Routing message to $target" >> "$log_file"
                    tmux send-keys -t "$target" "$message" Enter 2>/dev/null || echo "$(date): Failed to route to $target" >> "$log_file"
                fi
            fi
            
            # Check if agent is waiting for approval
            if echo "$line" | jq -e '.message.content[]? | select(.type == "tool_use")' >/dev/null 2>&1; then
                echo "$(date): $agent waiting for tool approval" >> "$log_file"
            fi
            
        done <<< "$latest_entries"
        
        LAST_SIZE[$agent]=$current_size
    fi
}

# Main monitoring loop
while true; do
    for agent in "${!AGENT_FILES[@]}"; do
        monitor_agent "$agent"
    done
    sleep 2
done