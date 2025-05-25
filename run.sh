#!/bin/bash
# RTFW Multi-Agent Management Script - Auto-detecting version

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running inside tmux
if [ -z "$TMUX" ]; then
    echo -e "${RED}Error: This script must be run inside a tmux session${NC}"
    echo "Start with: cd ~/prj/rtfw && tmux -f ./tmux.conf"
    exit 1
fi

# Get current windows
WINDOW_COUNT=$(tmux list-windows | wc -l)
HAS_ADMIN=$(tmux list-windows -F '#{window_name}' | grep -c '^admin$' || true)
HAS_NEXUS=$(tmux list-windows -F '#{window_name}' | grep -c '^nexus$' || true)

# Determine state and action
if [ "$WINDOW_COUNT" -eq 1 ] && [ "$HAS_ADMIN" -eq 0 ] && [ "$HAS_NEXUS" -eq 0 ]; then
    # Only one window exists, need full init
    echo -e "${GREEN}RTFW Agent System - Initializing${NC}"
    echo "================================="
    echo ""
    
    # Rename current window to admin
    tmux rename-window admin
    echo "✓ Renamed window 0 to 'admin'"
    
    # Create nexus window
    tmux new-window -n nexus
    echo "✓ Created 'nexus' window"
    
    # Check for session ID file
    if [ -f "nexus/.sessionid" ]; then
        SESSION_ID=$(cat nexus/.sessionid)
        echo "✓ Found previous NEXUS session: $SESSION_ID"
        
        # Resume NEXUS session
        tmux send-keys -t nexus "claude --resume $SESSION_ID"
        tmux send-keys -t nexus Enter
    else
        echo "✓ No previous session found, starting fresh"
        tmux send-keys -t nexus "claude"
        tmux send-keys -t nexus Enter
    fi
    
    # Wait for claude to launch
    echo -e "${YELLOW}Waiting for Claude to start...${NC}"
    sleep 10
    
    # Trigger bootstrap
    echo "✓ Triggering NEXUS bootstrap"
    tmux send-keys -t nexus 'please run @nexus/agent_bootstrap_process.md'
    tmux send-keys -t nexus Enter
    
    # Brief pause before starting monitor
    sleep 2
    echo ""
    echo -e "${GREEN}Initialization complete! Starting monitor...${NC}"
    echo ""
    
elif [ "$HAS_ADMIN" -eq 1 ] && [ "$HAS_NEXUS" -eq 1 ]; then
    # Both windows exist, go straight to monitoring
    echo -e "${GREEN}RTFW Agent System - Monitoring Active${NC}"
    echo "====================================="
    echo ""
    
else
    # Invalid state
    echo -e "${RED}Error: Invalid window configuration${NC}"
    echo "Found $WINDOW_COUNT windows:"
    tmux list-windows -F '  #{window_index}: #{window_name}'
    echo ""
    echo "Expected either:"
    echo "  - Single window (will auto-initialize)"
    echo "  - Both 'admin' and 'nexus' windows"
    exit 1
fi

# MONITORING LOOP
echo "Monitoring NEXUS for activity..."
echo "Press Ctrl+C to stop"
echo ""

while true; do
    # Get NEXUS window state
    NEXUS_STATE=$(tmux list-windows -F '#{window_name} #{?window_bell_flag,BELL,} #{?window_silence_flag,SILENT,} #{window_activity}' | grep '^nexus ')
    
    # Extract activity timestamp
    ACTIVITY=$(echo "$NEXUS_STATE" | awk '{print $NF}')
    NOW=$(date +%s)
    IDLE_TIME=$((NOW - ACTIVITY))
    
    # Check state and trigger scan if needed
    if [[ "$NEXUS_STATE" == *"BELL"* ]]; then
        echo -e "${RED}[$(date '+%H:%M:%S')] NEXUS requires attention (BELL)${NC}"
        # Don't trigger scan when BELL is raised - wait for admin
    elif [[ "$NEXUS_STATE" == *"SILENT"* ]] || [ "$IDLE_TIME" -gt 30 ]; then
        echo -e "${YELLOW}[$(date '+%H:%M:%S')] NEXUS idle for ${IDLE_TIME}s - triggering scan${NC}"
        tmux send-keys -t nexus 'please run @nexus/main_loop.md'
        tmux send-keys -t nexus Enter
    else
        echo -e "[$(date '+%H:%M:%S')] NEXUS active (idle ${IDLE_TIME}s)"
    fi
    
    sleep 10
done