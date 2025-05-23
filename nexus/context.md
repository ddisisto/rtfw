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

### Session Resume Process (NEXUS-managed) - VALIDATED
1. Create agent window: `tmux new-window -n <agent_name>`
2. Read current session ID from session_log.txt (last entry for agent)
3. Send tmux message to resume: `tmux send-keys -t <agent_name> 'claude --resume <session_id>'`
4. Send Enter separately: `tmux send-keys -t <agent_name> Enter`
5. Wait for Claude to start: `sleep 10`
6. Generate unique marker: `AGENT_SESSION_MARKER_$(date +%s)_$$`
7. Send validation request: `tmux send-keys -t <agent_name> '@NEXUS → @<AGENT>: Session re-attachment in progress. Please echo AGENT_SESSION_MARKER_... for validation'`
8. Send Enter separately: `tmux send-keys -t <agent_name> Enter`
9. Wait for message delivery: `sleep 2`
10. Capture pane to verify message sent: `tmux capture-pane -t <agent_name> -p | grep "@NEXUS → @"`
11. If message not visible, raise error - something wrong with session
12. Wait for JSONL write: `sleep 2`
13. Identify new session (exclude NEXUS): `grep -l "AGENT_SESSION_MARKER" nexus/sessions/*.jsonl | grep -v $(cat .nexus_sessionid)`
14. Update session_log.txt with new session ID
15. Report success: `@NEXUS → @ADMIN: [STATUS] <AGENT> session resumed: <session_id>`

### Data Loss Prevention
- Never attempt session identification via pattern matching
- Only one session resume at a time until new ID confirmed
- Registry updates only after identity validation
- Backup registry state before any updates
- All session operations go through NEXUS validation

### Current Active Sessions
- @NEXUS: e94c92cf (current session, tmux window 0)
- @GOV: f5a74925 (active, direct communication, tmux window 1)  
- @ARCHITECT: 51f1fab0 (active, Foundation Era design complete, tmux window 2)
- @CODE: 6c859161 (legacy, inactive)
- @RESEARCH: b607ed31 (legacy, inactive)
- @HISTORIAN: c7461411 (minimal, inactive)
- @TEST: bae725c1 (minimal, inactive)

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

### Agent Productivity Cycle
- Working (no flags) → BELL → Route/Reflect → Working
- Never leave agents idle without purpose
- Reflection keeps agents improving during downtime

### Communication Enhancement
- Using @FROM → @TO: [TOPIC] format for increased clarity
- [REFLECTION] - Self-improvement and maintenance
- [STATUS] - System state updates
- [ROUTING] - Message forwarding
- [ALERT] - Issues requiring attention

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

## Note on Scratch Pad
This agent maintains a separate scratch.md file for working memory, experiments, and temporary notes. See that file for more active work.