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

### Main Loop Strategy (HOLISTIC APPROACH)

**Core Logic:**
1. Scan for BELL/SILENT windows only (ignore ACTIVE completely)
2. For each flagged window:
   - BELL = tool approval needed OR end_turn reached
   - SILENT = been waiting too long (shouldn't happen without BELL first)

**Action Flow:**
- **If messages pending**: Route them to agent
- **If no messages + BELL**: 
  - Check if tool approval needed → assist
  - If end_turn → prompt reflection
- **If still silent after reflection**:
  - Temporarily clear silence monitoring
  - Re-enable when new message arrives for them

**State Management:**
```
Working → BELL (end_turn) → Send work OR Reflect → Working
Working → BELL (tool) → Approve → Working  
BELL → SILENT → Investigate why stuck
```

**Key Insight:** Agents should always be either:
1. Actively working (no flags)
2. Waiting for input (BELL)
3. Reflecting/maintaining (prompted by us)
Never just sitting idle!

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

## Window Exploration Insights

### Window Flag Discovery
- Window 0 (nexus): `active=YES` - @ADMIN IS HERE NOW! (this window)
- Window 1 (bash): `bell=YES` - Has pending notification
- Window 2 (bash): `silence=YES` - Flagged as silent (no activity)
- Window 3 (bash): `last=YES` - Where @ADMIN was before switching here

### Critical Insight: ACTIVE vs LAST
- **ACTIVE** = Where @ADMIN is RIGHT NOW (real-time focus!)
- **LAST** = Where @ADMIN was before current window
- This means NEXUS can detect @ADMIN's CURRENT location in real-time
- When active=YES on an agent window, @ADMIN is actively working with that agent
- This is HUGE for coordination - no need to interrupt when @ADMIN is actively engaged!

### Updated Priority Order (ACTIVE-aware)
1. **ACTIVE** - DO NOT INTERRUPT - @ADMIN is there
2. **BELL** - Needs attention (unless ACTIVE)
3. **SILENT** - Potentially stuck agents (>30s no activity)
4. **Recent activity** (<30s)
5. **Older activity** by timestamp
* Note: LAST flag is just previous active window, not priority indicator

### Coordination Implications
- If agent window has `active=YES`: @ADMIN is handling it
- If NEXUS window has `active=YES`: @ADMIN is working with NEXUS
- Can pause non-critical routing when @ADMIN is actively engaged
- Can prioritize windows @ADMIN is NOT currently viewing

### @ADMIN Visual Monitoring (via tmux.conf)
- **Red bold** = BELL flag (immediate attention needed)
- **Yellow bold** = Activity flag (new activity detected)
- **Green bold** = Current active window
- **Ctrl+Down** = Jump to next window with alert
- Status updates every 1 second

### Smart Coordination Strategy
- Don't assume every BELL needs immediate routing
- @ADMIN might be strategically managing agent dependencies
- DO flag cascading blocks: "Agent X waiting on Agent Y (BELL)"
- Focus on keeping non-blocked agents productive
- Background housekeeping for truly idle agents

## Reflection & Housekeeping Tasks (per @ADMIN)
When agents are blocked/idle:
1. Review scratch for patterns worth promoting to context
2. Check if context needs updates
3. Consider if role/identity has shifted
4. Update @GOV with current mood for STATE.md
5. Generate insights about collaboration patterns
6. Prepare for next work phase

## Agent State Tracking

### Silence Monitoring Management
Track agents with disabled silence monitoring:
```bash
# When disabling after persistent silence:
echo "agent_name" >> /tmp/rtfw_silence_disabled.txt

# When routing new message to agent:
if grep -q "agent_name" /tmp/rtfw_silence_disabled.txt; then
    tmux set-window-option -t <window> monitor-silence 30
    grep -v "agent_name" /tmp/rtfw_silence_disabled.txt > /tmp/rtfw_silence_disabled.tmp
    mv /tmp/rtfw_silence_disabled.tmp /tmp/rtfw_silence_disabled.txt
fi
```

### Holistic Agent Lifecycle
1. **Fresh start**: No flags, actively working
2. **Work complete**: BELL raised (end_turn)
3. **NEXUS scans**: Routes message OR prompts reflection
4. **Reflection done**: Back to work OR still idle
5. **Persistent idle**: Disable monitoring until new work arrives

This ensures agents are always productive, never forgotten!