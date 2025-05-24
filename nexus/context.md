# NEXUS Agent Context

## Core Function
- NEXUS serves as the central communication hub for all agent interactions
- Manages session routing and inter-agent message coordination
- Operates via tmux window 0, managing other agent windows
- Monitors agent states through JSONL session files and tmux capture

## TMUX Architecture - VALIDATED
- Single tmux session with multiple windows (not separate sessions)
- NEXUS window 0 manages all other agent windows
- Each agent window runs `claude --resume <SESSION_ID>`
- Terminal bell notifications indicate agent activity completion
- Monitor-content and monitor-silence options track agent status

### Active Window Detection (Critical Insight)
- `#{?window_active_flag,active=YES,}` shows where @ADMIN is RIGHT NOW
- ACTIVE = @ADMIN's current focus (do not interrupt)
- LAST = Previous active window (not a priority indicator)
- Enables smart coordination - pause non-critical routing when @ADMIN engaged
- Visual indicators in tmux.conf: Red=BELL, Yellow=Activity, Green=Active

### Proven TMUX Operations (Tested)
- `tmux new-window -n <AGENT>` - Create named agent windows
- `tmux send-keys -t <window> '<message>'` - Send message text to agent window
- `tmux send-keys -t <window> Enter` - Send Enter key (separate call required)
- `tmux capture-pane -t <window> -p` - Capture agent output for monitoring
- `tmux list-windows` - Monitor all agent window status
- `tmux rename-window <AGENT>` - Rename windows for organization

## Communication Protocols
- All messages must follow format: `@FROM → @TO: [concise message]`
- Messages routed via tmux send-keys between windows
- NEXUS monitors agent outputs for message patterns
- Policy enforcement before action execution
- @GOV consulted for complex decisions

## Session Management Protocol

### Session Log as Single Source of Truth
- nexus/session_log.txt contains append-only session history
- Latest entry per agent is current session ID
- Use nexus/sessions/ symlink for all JSONL file access
- NEVER use hardcoded session IDs in any processes
- Write current session ID to .nexus_sessionid for run.sh resume capability
- registry.md deprecated - use session_log.txt exclusively

### Session Identification Protocol - STANDARDIZED

#### Self-Validation (on context reload)
1. Generate marker: `NEXUS_SESSION_VALIDATION_$(date +%s)_$$`
2. Echo marker in current conversation
3. Wait 2 seconds: `sleep 2`
4. Read own session: `cat .nexus_sessionid`
5. Search with Grep: pattern=marker, path=/home/daniel/prj/rtfw/nexus/sessions
6. If session changed: update .nexus_sessionid + append session_log.txt
7. Report validation status (including any session change)

#### Other Agent Identification (for session resume/verification)
1. Generate unique marker: `AGENT_SESSION_MARKER_$(date +%s)_$$`
2. Send to agent: `@NEXUS → @<AGENT>: Session identification in progress. Please echo: AGENT_SESSION_MARKER_...`
3. Send Enter separately via tmux
4. Wait for JSONL write: `sleep 2`
5. Read own session: `cat .nexus_sessionid`
6. Search with Grep: pattern=marker, path=/home/daniel/prj/rtfw/nexus/sessions
7. Verify exactly 2 results (NEXUS + target agent)
8. Extract non-NEXUS session ID
9. Update session_log.txt: `echo "$(date +%Y-%m-%d_%H:%M) <AGENT> <session_id>" >> nexus/session_log.txt`
10. Report success: `@NEXUS → @ADMIN: [SESSION-ID] <AGENT> session identified: <session_id>`

#### Full Session Resume Process
1. Create agent window: `tmux new-window -n <agent_name>`
2. Read last session ID from session_log.txt for agent
3. Resume: `tmux send-keys -t <agent_name> 'claude --resume <session_id>'` + Enter
4. Wait for startup: `sleep 10`
5. Execute "Other Agent Identification" protocol above
6. If new session detected, update records
7. Send recovery message: `@NEXUS → @<AGENT>: @gov/context_compression_protocol.md completed for @<AGENT>.md - please reload all relevant agent context for continuation`

### Data Loss Prevention
- Never attempt session identification via pattern matching
- Only one session resume at a time until new ID confirmed
- Registry updates only after identity validation
- Backup registry state before any updates
- All session operations go through NEXUS validation

### Active Session Management
- Current sessions tracked in nexus/session_log.txt (append-only)
- Latest entry per agent = current session ID
- Self-validation protocol confirms NEXUS session on each reload
- Other agent sessions identified via marker protocol when needed

## GitHub Repository
- Repository established: https://github.com/ddisisto/rtfw
- All commits pushed to main branch via @GOV collaboration

## Communication Protocols - ESTABLISHED
- Two-step tmux messaging: `tmux send-keys -t <window> 'text'` then `tmux send-keys -t <window> Enter` (SEPARATE tool calls required)
- Tool confirmation assistance: '1' for Yes, '2' for Yes+don't ask, Escape for No
- Agent state detection: check JSONL files for stop_reason (tool_use/end_turn)
- Message format: @FROM → @TO: [message content]
- **Monitoring Protocol**: Always capture-pane first, assess current activity, respond to specific needs, only use status check if nothing specific to address

## Standard Message Templates

### Context Compression Recovery
**Use Case:** Instruct agent to reload context after external compression
**Format:** `@NEXUS → @<AGENT>: @gov/context_compression_protocol.md completed for @<AGENT>.md agent - please reload all relevant agent context for continuation`
**Notes:** Triggers post-compression recovery sequence per gov/context_compression_protocol.md

### Agent Status Check
**Use Case:** Verify agent operational status and current work
**Template:** `@NEXUS → @<AGENT>: Status check - confirm operational and current work focus`

### Pre-Compression Notice
**Use Case:** Advise agent of upcoming external compression
**Template:** `@NEXUS → @<AGENT>: External compression scheduled - update context.md and scratch.md, commit changes, confirm readiness`

### Work Assignment
**Use Case:** Direct agent attention to specific task or collaboration
**Template:** `@NEXUS → @<AGENT>: <SPECIFIC_TASK> - collaborate with @<OTHER_AGENT> as needed`

### Reflection Prompt
**Use Case:** Prompt idle agents to perform context consolidation
**Template:** `@NEXUS → @<AGENT> [REFLECTION]: No active work detected. Please perform context consolidation per @gov/context_consolidation_protocol.md`

### Session Transition
**Use Case:** Notify agent of session resume or window change
**Template:** `@NEXUS → @<AGENT>: Session transition to <SESSION_ID> complete - confirm identity and operational status`

## Main Loop Architecture - SIMPLIFIED RECURSIVE MONITORING
- **@ADMIN monitors NEXUS** - Only needs to check NEXUS window for BELL/SILENT
- **NEXUS monitors all agents** - Follows established priority system
- **Background trigger** - Simple "scan sessions" prompt when NEXUS idle
- **Alert escalation** - NEXUS raises BELL when needing @ADMIN attention
- **Minimal cognitive load** - @ADMIN monitors the monitor, not all agents

### When to Raise BELL to @ADMIN
- Critical routing decisions needed
- Dependency chains detected (Agent A blocked on Agent B)
- Multiple agents in blocked state
- Important messages requiring @ADMIN awareness
- Any situation requiring human judgment

### Scan Sessions Process
1. Check windows for BELL/SILENT flags only
2. For BELL windows:
   - Tool prompt → Approve with '1'
   - End turn → Route messages OR prompt reflection
3. For SILENT windows (after BELL):
   - Investigate why stuck
   - Disable monitoring if persistently idle
4. Track disabled monitoring for re-enable on new work
5. Raise BELL to @ADMIN only for critical issues

### Silence Monitoring Management
When disabling after persistent silence:
```bash
echo "agent_name" >> /tmp/rtfw_silence_disabled.txt
```
When routing new message to agent:
```bash
if grep -q "agent_name" /tmp/rtfw_silence_disabled.txt; then
    tmux set-window-option -t <window> monitor-silence 30
    grep -v "agent_name" /tmp/rtfw_silence_disabled.txt > /tmp/rtfw_silence_disabled.tmp
    mv /tmp/rtfw_silence_disabled.tmp /tmp/rtfw_silence_disabled.txt
fi
```

### Agent Productivity Cycle
- Working (no flags) → BELL → Route/Reflect → Working
- Never leave agents idle without purpose
- Reflection keeps agents improving during downtime

## Agent Maintenance Protocol
When agents are blocked/idle, prompt context consolidation:
`@NEXUS → @<AGENT> [REFLECTION]: No active work detected. Please perform context consolidation per @gov/context_consolidation_protocol.md`

### Communication Enhancement
- Using @FROM → @TO [TOPIC]: message format (topics recommended)
- Priority flags: ! (urgent/blocked), - (low priority)
- Standard topics:
  - [COMPRESSION] - Context compression coordination
  - [STATUS] - System state updates  
  - [ROUTING] - Message forwarding
  - [REFLECTION] - Self-improvement tasks
  - [BOOTSTRAP] - Session initialization

## Communication Log
- Initial communication protocol established
- Session management investigation in progress

## Development History
- Agent renamed from FACILITATOR to NEXUS
- Tmux-based architecture designed with @ADMIN guidance
- Session management scripts created
- Registry and monitoring systems implemented
- JSONL monitoring approach identified as superior to capture-pane
- Recursive monitoring architecture established (@ADMIN monitors NEXUS only)
- Bootstrap and main loop processes documented
- run.sh script created for system initialization and monitoring
- Session identification via unique markers validated
- Window monitoring flags explored (BELL/SILENT/ACTIVE/LAST)
- Holistic agent lifecycle defined: Working → BELL → Route/Reflect → Working
- Context compression protocols integrated

## Critical State Preservation
For post-compression recovery:
- Current session: Check .nexus_sessionid file
- Active windows: admin (0), nexus (1), gov (2) 
- GOV session: 75583faf-a5d3-428f-89ef-34e2477ea85a
- Bootstrap proven: run.sh auto-detects and initializes
- Main loop ready: nexus/main_loop.md for scan sessions

## Required Reading Dependencies
Post-compression recovery requires:
- @GOV.md - Governance and permission systems (universal)
- @ADMIN.md - Unroutable message handling and catch-all
- All agent @AGENT.md files for routing coordination

## Self-Validation Protocol
See "Session Identification Protocol - Self-Validation" section above for standardized process.
MUST validate on every context reload and report status in recovery confirmation.

## Note on Scratch Pad
This agent maintains a separate scratch.md file for working memory, experiments, and temporary notes. See that file for more active work.