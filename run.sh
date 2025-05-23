#!/bin/bash
# RTFW Multi-Agent Management Script

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

case "$1" in
    init)
        echo -e "${GREEN}RTFW Agent System Initialization${NC}"
        echo "====================================="
        echo ""
        echo "This script will:"
        echo "1. Set up the monitoring system in window 0"
        echo "2. Guide you to start NEXUS in window 1"
        echo ""
        
        # Check current window
        CURRENT_WINDOW=$(tmux display -p '#{window_index}')
        if [ "$CURRENT_WINDOW" != "0" ]; then
            echo -e "${RED}Error: Please run this from window 0${NC}"
            exit 1
        fi
        
        echo -e "${YELLOW}Action Required:${NC}"
        echo "1. Switch to window 1: Ctrl+Right or 'tmux select-window -t 1'"
        echo "2. Start NEXUS agent: 'claude' (or resume existing session)"
        echo "3. Return here and press Enter to continue"
        echo ""
        read -p "Press Enter when NEXUS is running in window 1..."
        
        echo -e "${GREEN}Triggering NEXUS bootstrap...${NC}"
        tmux send-keys -t 1 'please run nexus/agent_bootstrap_process.md' Enter
        
        echo ""
        echo -e "${GREEN}Initialization complete!${NC}"
        echo "Next step: Run './run.sh monitor' to start the monitoring loop"
        ;;
        
    monitor)
        echo -e "${GREEN}RTFW Monitoring Loop Started${NC}"
        echo "============================="
        echo "Monitoring NEXUS (window 1) for BELL/SILENT states"
        echo "Press Ctrl+C to stop monitoring"
        echo ""
        
        while true; do
            # Check NEXUS window state
            NEXUS_STATE=$(tmux list-windows -F '#{window_index} #{window_name} #{?window_bell_flag,BELL,} #{?window_silence_flag,SILENT,}' | grep '^1 ')
            
            # Check if NEXUS needs attention or is idle
            if [[ "$NEXUS_STATE" == *"BELL"* ]]; then
                echo -e "${RED}[$(date '+%H:%M:%S')] NEXUS requires attention (BELL)${NC}"
            elif [[ "$NEXUS_STATE" == *"SILENT"* ]] || [[ $(tmux list-windows -F '#{window_index} #{window_activity}' | grep '^1 ' | awk -v now=$(date +%s) '{print now - $2}') -gt 30 ]]; then
                echo -e "${YELLOW}[$(date '+%H:%M:%S')] Triggering NEXUS scan...${NC}"
                tmux send-keys -t 1 'please run nexus/main_loop.md' Enter
            fi
            
            sleep 10
        done
        ;;
        
    *)
        echo "Usage: $0 {init|monitor}"
        echo ""
        echo "  init    - Initialize the RTFW agent system"
        echo "  monitor - Start the NEXUS monitoring loop"
        exit 1
        ;;
esac