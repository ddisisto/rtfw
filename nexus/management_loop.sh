#!/bin/bash
# NEXUS Agent Management Loop

log_file="/tmp/nexus_activity.log"

echo "$(date): @NEXUS Management Loop Started" >> "$log_file"

while true; do
    # Check for agent activity
    active_windows=$(tmux list-windows -f '#{window_bell_flag}' | grep -v "nexus")
    
    if [ -n "$active_windows" ]; then
        echo "$(date): Activity detected:" >> "$log_file"
        echo "$active_windows" >> "$log_file"
        
        # Process each active window
        while IFS= read -r window; do
            window_name=$(echo "$window" | cut -d: -f2 | tr -d ' ')
            
            # Capture recent output
            recent_output=$(tmux capture-pane -t "$window_name" -p | tail -5)
            
            # Check for messages in format @FROM → @TO
            if echo "$recent_output" | grep -q "@.*→.*:"; then
                message=$(echo "$recent_output" | grep "@.*→.*:" | tail -1)
                echo "$(date): Message detected from $window_name: $message" >> "$log_file"
                
                # Parse message and route
                target=$(echo "$message" | sed 's/.*→\s*@\?\([^:]*\):.*/\1/')
                if [ "$target" != "$window_name" ]; then
                    echo "$(date): Routing message to $target" >> "$log_file"
                    tmux send-keys -t "$target" "$message" Enter
                fi
            fi
            
        done <<< "$active_windows"
    fi
    
    # Check for silent agents
    silent_windows=$(tmux list-windows -f '#{?window_silence_flag,#{window_name},}' | grep -v "nexus")
    if [ -n "$silent_windows" ]; then
        echo "$(date): Silent agents: $silent_windows" >> "$log_file"
    fi
    
    sleep 5
done