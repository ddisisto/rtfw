# NEXUS Main Loop Process

This document defines the scan sessions routine triggered by `./run.sh monitor`.

## Main Loop Execution

### 1. Acknowledge Trigger
- Output: `@NEXUS → @ADMIN: Scanning agent sessions...`

### 2. Gather Window States
```bash
tmux list-windows -F '#{window_index}:#{window_name} #{?window_active,ACTIVE,} #{?window_bell_flag,BELL,} #{?window_silence_flag,SILENT,} #{?window_last_flag,LAST,} activity=#{t/p:window_activity}'
```

### 3. Priority Processing
Process windows in order:
1. **BELL** (not ACTIVE) - Immediate attention needed
2. **LAST** (not ACTIVE) - @ADMIN's previous focus
3. **SILENT** - Potentially stuck (>30s no activity)
4. **Recent** - Activity within last 30s
5. **Other** - By age of last activity

### 4. For Each Priority Window
- Skip if window has ACTIVE flag (@ADMIN is there)
- Capture pane: `tmux capture-pane -t <window> -p | tail -50`
- Parse for:
  - Pending @FROM → @TO messages
  - Tool confirmation prompts (Yes/No questions)
  - Error states or blocks
  - Long idle periods

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
- Detect when monitoring is suspended (^C on run.sh)
- Track patterns across multiple scans
- Learn common routing paths
- Identify recurring blockages