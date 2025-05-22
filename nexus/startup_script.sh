#!/bin/bash
# NEXUS Agent Management Startup Script

# Map session IDs to agent names
declare -A SESSIONS
SESSIONS[code]="66a678dc-e43d-4db2-86c1-f93ea54b69ad"
SESSIONS[gov]="6c859161-b569-4a87-a53e-3b88d6943c0d"
SESSIONS[architect]="932ef584-cac9-4868-ae0b-30fed3de40e5"
SESSIONS[research]="b607ed31-0de8-4db1-b3df-2a1bcaec0d66"
SESSIONS[historian]="c4088511-fc4e-4916-bd88-c4ebf22ca138"
SESSIONS[test]="bae725c1-5163-43ff-af08-d50ca01233e6"

# Configure terminal bell notifications
claude config set --global preferredNotifChannel terminal_bell

echo "@NEXUS Startup: Initializing agent management system"

# Create windows for each agent
for agent in code gov architect research historian test; do
    echo "Creating window for @${agent^^}"
    tmux new-window -n "$agent" /bin/bash
    
    # Start Claude with appropriate session
    tmux send-keys -t "$agent" "claude --resume ${SESSIONS[$agent]}" Enter
    
    # Set up monitoring
    tmux set-window-option -t "$agent" monitor-content "@*→*"
    tmux set-window-option -t "$agent" monitor-silence 300
done

echo "@NEXUS Startup complete. All agent windows initialized."
echo "Use 'tmux list-windows' to see all active agents."