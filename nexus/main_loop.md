# NEXUS Main Loop Process

This document defines the scan sessions routine triggered by @ADMIN running `./run.sh`.

## Main Loop Execution

### 1. Acknowledge Trigger
- Output: `@NEXUS → @ADMIN: Scanning agent sessions...`

### 2. Gather Window States
```bash
tmux list-windows -F '#{window_index}:#{window_name} #{?window_bell_flag,BELL,} #{?window_silence_flag,SILENT,}'
```
Focus only on BELL and SILENT flags - ignore ACTIVE windows entirely (@ADMIN is there interacting with respective agent).

### 3. Check for Pending Messages
Scan captured outputs from previous interactions for any @FROM → @TO messages that need routing.

### 4. Process Flagged Windows
For each window with BELL or SILENT:

**BELL Processing:**
1. Capture pane: `tmux capture-pane -t <window> -p | tail -50`
2. Determine BELL cause:
   - Tool confirmation prompt → Send '1' to approve, Escape to reject, or if applicable '2' to approve + auto-approve
   - End turn reached → Check for messages to route
   - If no messages → Prompt reflection: `@NEXUS → @AGENT: [REFLECTION] Please review and update your context/scratch as needed`

**SILENT Processing:**
1. Should rarely happen without BELL first
2. If persistent after reflection:
   - `tmux set-window-option -t <window> monitor-silence 0` (disable)
   - Note: Re-enable when routing new message to them

### 5. Take Appropriate Action
- **Route messages**: Forward @FROM → @TO between agents
- **Tool assists**: Send '1' for confirmations if clear
- **Housekeeping**: Trigger reflection tasks for idle agents
- **Dependency detection**: Note if Agent A waiting on Agent B

### 6. Escalation Decision
Raise BELL to @ADMIN if:
- Multiple agents blocked on same dependency
- Critical routing decision unclear
- Error state requiring human intervention
- Important message for @ADMIN awareness
- Any @AGENT → @ADMIN messages found

### 7. Status Report
- If all clear: `@NEXUS → @ADMIN: All agents operational. No interventions needed.`
- If issues found: `@NEXUS → @ADMIN: [BELL] <specific issue requiring attention>`

### 8. Return to Idle
- Clear any temporary state
- Wait for next trigger
- Monitor for direct @ADMIN → @NEXUS messages

## Intelligent Behaviors
- Track patterns across multiple scans
- Learn common routing paths
- Identify recurring blockages