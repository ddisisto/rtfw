#!/bin/bash
# NEXUS Session Management - Safe Resume and Tracking
# Prevents data loss by validating session IDs before use

SESSION_DIR="$HOME/.claude/projects/-home-daniel-prj-rtfw"
REGISTRY_FILE="/home/daniel/prj/rtfw/nexus/registry.md"

# Get current session ID for an agent from registry
get_current_session() {
    local agent=$1
    # Extract session ID from registry table
    grep "@${agent}" "$REGISTRY_FILE" | grep -v "NOT FOUND" | awk '{print $3}' | head -1
}

# Monitor for new session file creation
wait_for_new_session() {
    local timeout=${1:-30}
    local start_time=$(date +%s)
    local initial_files=$(ls -1 "$SESSION_DIR"/*.jsonl 2>/dev/null | wc -l)
    
    echo "Monitoring for new session file (timeout: ${timeout}s)..."
    
    while true; do
        current_files=$(ls -1 "$SESSION_DIR"/*.jsonl 2>/dev/null | wc -l)
        if [ "$current_files" -gt "$initial_files" ]; then
            # Find the newest file
            newest_file=$(ls -t "$SESSION_DIR"/*.jsonl | head -1)
            new_session_id=$(basename "$newest_file" .jsonl)
            echo "New session detected: $new_session_id"
            echo "$new_session_id"
            return 0
        fi
        
        current_time=$(date +%s)
        if [ $((current_time - start_time)) -gt $timeout ]; then
            echo "Timeout waiting for new session"
            return 1
        fi
        
        sleep 1
    done
}

# Validate agent identity in session
validate_agent_identity() {
    local session_id=$1
    local expected_agent=$2
    local session_file="$SESSION_DIR/${session_id}.jsonl"
    
    if [ ! -f "$session_file" ]; then
        echo "Session file not found: $session_file"
        return 1
    fi
    
    echo "Validating agent identity for session $session_id..."
    
    # Send identity check via tmux
    local window_name=$(echo "$expected_agent" | tr '[:upper:]' '[:lower:]')
    tmux send-keys -t "$window_name" "Agent ID Check: Please respond with '@${expected_agent} IDENTITY CONFIRMED'" Enter
    
    # Wait for response to appear in session file
    local timeout=15
    local start_time=$(date +%s)
    
    while true; do
        # Check if our prompt and response are in the file
        if tail -10 "$session_file" | grep -q "Agent ID Check" && \
           tail -10 "$session_file" | grep -q "@${expected_agent} IDENTITY CONFIRMED"; then
            echo "Agent identity confirmed: @${expected_agent}"
            return 0
        fi
        
        current_time=$(date +%s)
        if [ $((current_time - start_time)) -gt $timeout ]; then
            echo "Timeout waiting for agent identity confirmation"
            return 1
        fi
        
        sleep 1
    done
}

# Resume agent session safely
resume_agent_session() {
    local agent=$1
    local window_name=$(echo "$agent" | tr '[:upper:]' '[:lower:]')
    
    echo "=== Resuming @${agent} Session ==="
    
    # Get current session ID from registry
    local current_session=$(get_current_session "$agent")
    if [ -z "$current_session" ]; then
        echo "ERROR: No current session found for @${agent} in registry"
        return 1
    fi
    
    echo "Current session for @${agent}: $current_session"
    
    # Start monitoring for new session file
    echo "Starting claude resume in tmux window: $window_name"
    tmux send-keys -t "$window_name" "claude --resume $current_session" Enter &
    
    # Wait for new session file
    new_session=$(wait_for_new_session 30)
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to detect new session for @${agent}"
        return 1
    fi
    
    echo "New session created: $new_session"
    
    # Validate agent identity
    if validate_agent_identity "$new_session" "$agent"; then
        echo "SUCCESS: @${agent} session resumed and validated"
        echo "Old session: $current_session"
        echo "New session: $new_session"
        
        # Update registry via NEXUS
        echo "REGISTRY_UPDATE_NEEDED:$agent:$current_session:$new_session"
        return 0
    else
        echo "ERROR: Failed to validate agent identity for $new_session"
        return 1
    fi
}

# Main function
case "$1" in
    "resume")
        if [ -z "$2" ]; then
            echo "Usage: $0 resume <AGENT>"
            echo "Example: $0 resume CODE"
            exit 1
        fi
        resume_agent_session "$2"
        ;;
    "get-session")
        if [ -z "$2" ]; then
            echo "Usage: $0 get-session <AGENT>"
            exit 1
        fi
        get_current_session "$2"
        ;;
    *)
        echo "Usage: $0 {resume|get-session} <AGENT>"
        echo "  resume <AGENT>     - Safely resume agent session"
        echo "  get-session <AGENT> - Get current session ID for agent"
        exit 1
        ;;
esac