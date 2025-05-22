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
- `tmux new-window -n <name>` - Create named agent windows
- `tmux send-keys -t <window> '<command>' Enter` - Execute commands in agent windows
- `tmux capture-pane -t <window> -p` - Capture agent output for monitoring
- `tmux list-windows` - Monitor all agent window status
- `tmux rename-window <name>` - Rename windows for organization

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

### Session Resume Process (NEXUS-managed) - READY FOR IMPLEMENTATION
1. Create agent window: `tmux new-window -n <agent_name>`
2. Read current session ID from session_log.txt (last entry for agent)
3. Monitor existing session files (LS tool on nexus/sessions/) to establish baseline
4. Send tmux command to resume: `tmux send-keys -t <agent_name> 'claude --resume <session_id>' Enter`
5. Monitor for new .jsonl file creation in nexus/sessions/
6. Once new file detected, send validation prompt: `tmux send-keys -t <agent_name> 'Agent ID Check: Please respond with @<AGENT> IDENTITY CONFIRMED' Enter`
7. Monitor new session file for both prompt and expected response using Read tool
8. Upon successful validation, append new session to session_log.txt
9. Git commit session log changes with descriptive message
10. Log session transition in scratch.md

### Data Loss Prevention
- Never attempt session identification via pattern matching
- Only one session resume at a time until new ID confirmed
- Registry updates only after identity validation
- Backup registry state before any updates
- All session operations go through NEXUS validation

### Current Active Sessions
- @NEXUS: ce51677e (current session, tmux window 0)
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
- Two-step tmux messaging: `tmux send-keys -t <window> 'text'` then `tmux send-keys -t <window> Enter`
- Tool confirmation assistance: '1' for Yes, '2' for Yes+don't ask, Escape for No
- Agent state detection: check JSONL files for stop_reason (tool_use/end_turn)
- Message format: @FROM → @TO: [message content]

## Game Loop Architecture - READY FOR IMPLEMENTATION
- Session State Monitor: Check JSONL stop_reason for agent states
- Message Distribution: Parse and route @FROM → @TO messages
- Work Distribution: Match idle agents with pending tasks  
- Flag Management: Intervention triggers for approvals/alerts
- SSH authentication configured for seamless pushes

## Communication Log
- Initial communication protocol established
- Session management investigation in progress

## Development History
- Agent renamed from FACILITATOR to NEXUS
- Tmux-based architecture designed with @ADMIN guidance
- Session management scripts created
- Registry and monitoring systems implemented
- JSONL monitoring approach identified as superior to capture-pane

## Note on Scratch Pad
This agent maintains a separate scratch.md file for working memory, experiments, and temporary notes. See that file for more active work.