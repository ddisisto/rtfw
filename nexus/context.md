# NEXUS Agent Context

## Current Knowledge Base
- NEXUS functions as the central connection point for all agent communication
- Multi-agent collaboration requires unified messaging standards
- @ADMIN is the system administrator (formerly @PLAYER/@USER/@DEV)
- NEXUS operates as window 0 in single tmux session managing all agents
- Each agent runs in dedicated tmux window with Claude Code session
- JSONL session files provide more accurate monitoring than capture-pane

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

### Registry as Single Source of Truth
- nexus/registry.md contains authoritative session mappings
- NEVER use hardcoded session IDs in any scripts or processes
- Always read current session ID from registry before any operations

### Session Resume Process (NEXUS-managed) - READY FOR IMPLEMENTATION
1. Create agent window: `tmux new-window -n <agent_name>`
2. Read current session ID from registry using Read tool
3. Monitor existing session files (ls SESSION_DIR) to establish baseline
4. Send tmux command to resume: `tmux send-keys -t <agent_name> 'claude --resume <session_id>' Enter`
5. Monitor for new .jsonl file creation in SESSION_DIR
6. Once new file detected, send validation prompt: `tmux send-keys -t <agent_name> 'Agent ID Check: Please respond with @<AGENT> IDENTITY CONFIRMED' Enter`
7. Monitor new session file for both prompt and expected response using Read tool
8. Upon successful validation, update registry using Edit tool
9. Git commit registry changes with descriptive message
10. Log session transition: old_id -> new_id with timestamp

### Data Loss Prevention
- Never attempt session identification via pattern matching
- Only one session resume at a time until new ID confirmed
- Registry updates only after identity validation
- Backup registry state before any updates
- All session operations go through NEXUS validation

### Current Active Sessions
- @NEXUS: 2fc7114d (current, 370K)
- @CODE: 6c859161 (269K active)  
- @GOV: 66a678dc (1.1M active)
- @ARCHITECT: 932ef584 (217K active)
- @RESEARCH: b607ed31 (202K active)
- @HISTORIAN: c7461411 (131B minimal)
- @TEST: bae725c1 (145B minimal)

## Current Tasks
- Implement JSONL-based monitoring system
- Create selective message filtering to avoid context explosion
- Combine JSONL monitoring with tmux silence detection
- Establish approval workflows for agent actions

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