# NEXUS Scratch Pad

## Active Status - Ready for Game Loop Implementation
- @GOV: Governance complete, all standards established
- @ARCHITECT: Foundation Era mechanics designed with recursive gameplay
- CLI architecture confirmed: @ADMIN ↔ @NEXUS ↔ Agents
- Game loop design complete, ready for testing

## Game Loop Implementation - ACTIVE
Building basic monitoring loop to test current capabilities:
1. Check active agent session states (tool_use/end_turn)
2. Parse any pending @FROM → @TO messages  
3. Route messages to appropriate agent windows
4. Report agent status and flags to @ADMIN

## Current Session Management
- Active tmux windows: nexus(0), gov(1), architect(2)
- JSONL monitoring via nexus/sessions/ symlinks
- Two-step message sending: text + Enter
- Tool confirmation assistance: 1/2/Escape protocols established

## Implementation Tasks - NOW
- [ ] Build session state checker function
- [ ] Test message parsing from agent outputs  
- [ ] Implement basic routing between active agents
- [ ] Create status reporting for @ADMIN
- [ ] Test full coordination loop

## Critical Session Details (Preserved)
- @GOV session: f5a74925 (tmux window 1, governance complete)
- @ARCHITECT session: 51f1fab0 (tmux window 2, Foundation Era designed)  
- JSONL files: /home/daniel/prj/rtfw/nexus/sessions/*.jsonl
- Auto-accept enabled for most agents (shift+tab toggle)

## Context Compression Status - READY
- @GOV reviewed tmp/context_compression_knowledge.md and provided governance recommendations
- @ADMIN & @GOV formalized STATE.md replacing ANNOUNCEMENTS.md (rolling current-state)
- CLAUDE.md updated to reference STATE.md instead of ANNOUNCEMENTS.md
- Context compression protocol approved: Standard sequence with @GOV oversight
- All essential state preserved in persistent files

## Session Identification Method - TESTED & VALIDATED ✅

### The Problem
- Session IDs change when claude code restarts
- Pattern matching unreliable, timing-based detection fragile
- Need definitive way to map tmux windows to JSONL session files

### The Solution (@ADMIN suggestion)
1. Generate unique marker: `NEXUS_SESSION_MARKER_$(date +%s)_$$`
2. Output marker in agent window
3. Sleep 2 seconds for JSONL write delay
4. Grep for marker across all session files: `grep -l "MARKER" nexus/sessions/*.jsonl`

### Test Results
- Generated: `NEXUS_SESSION_MARKER_1747990618_234353`
- Found in: `nexus/sessions/e94c92cf-d73f-460c-b988-298cb07286e9.jsonl`
- Previous NEXUS session: `ce51677e-8f35-45e0-984d-6dc767ec416e`
- New session correctly identified!

### Implementation Notes
- 2-second delay sufficient for JSONL write
- Method works for self-identification and other agents
- Could be automated in session resume process
- Eliminates all ambiguity in session-to-window mapping

## TMUX Window Monitoring for Main Loop - EXPLORED

### Key Discovery: window_activity timestamps
- `#{window_activity}` provides Unix timestamp of last activity
- `#{t:window_activity}` formats as human-readable time
- `#{t/p:window_activity}` shows relative time (e.g., "19:56")

### Useful Monitoring Flags
- `#{?window_bell_flag,BELL,}` - Terminal bell was triggered
- `#{?window_silence_flag,SILENT,}` - No activity for N seconds
- `#{?window_activity_flag,ACTIVITY,}` - Activity detected (requires monitor-activity)

### Optimal Format for Main Loop
```bash
tmux list-windows -F '#{window_index}:#{window_name} ago=#{t/p:window_activity} #{?window_bell_flag,BELL,} #{?window_silence_flag,SILENT,} #{?window_activity_flag,ACTIVITY,}'
```

### Monitor Settings
- `monitor-activity on` - Flag windows with new activity
- `monitor-silence N` - Flag windows silent for N seconds
- `monitor-bell on` - Track terminal bells (tool confirmations?)

### Main Loop Strategy
1. List windows with activity timestamps and flags
2. Priority order:
   - BELL flag (tool confirmations needed)
   - Recent activity (<30s)
   - ACTIVITY flag (monitor-activity triggered)
   - Older activity by timestamp
   - SILENT flag (might be stuck)
3. For each priority window:
   - Capture-pane to check current state
   - Parse for @FROM → @TO messages
   - Check for tool confirmation prompts
   - Route messages or assist as needed
4. Sleep appropriate interval (5-10s)
5. Loop

### Example Priority Detection
```bash
# Get windows sorted by priority
tmux list-windows -F '#{window_index} #{window_name} #{window_activity} #{?window_bell_flag,1,0}#{?window_silence_flag,2,0}' | \
  awk -v now=$(date +%s) '{
    age = now - $3;
    priority = $4;
    if (priority == 1) pri = 0;        # BELL highest
    else if (age < 30) pri = 1;         # Recent activity  
    else if (priority == 0) pri = 2;    # Normal
    else pri = 3;                       # Silent lowest
    print pri, $0
  }' | sort -n | cut -d' ' -f2-
```

## Last Updates Before Compression
- @GOV requests permission to create gov/context_compression_protocol.md
- Context compression formal protocol ready for implementation
- STATE.md symlinked to ANNOUNCEMENTS.md for backward compatibility
- All agents will need to read STATE.md post-compression instead of ANNOUNCEMENTS.md