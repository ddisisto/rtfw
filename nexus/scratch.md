# NEXUS Scratch Pad

## Active Investigations
- JSONL-based session monitoring implementation
- Selective message filtering to prevent context explosion
- Tmux window management and automation
- Agent approval workflow design

## Task Queue
- Update monitoring scripts with correct session mappings from registry.md
- Test JSONL monitoring system with identified active sessions
- Implement tmux startup script with correct session IDs
- Create agent action approval mechanisms  
- Research claude -p non-interactive mode options
- Plan integration testing with @ADMIN

## Session Management Implementation

### NEXUS Session Resume Protocol - TESTED & READY
When resuming any agent session, NEXUS will:
0. Use Bash tool: `tmux new-window -n <agent_name>` to create agent window
1. Use Read tool on nexus/registry.md to get current session ID
2. Use Bash tool to list SESSION_DIR files (baseline)
3. Use Bash tool: `tmux send-keys -t <agent_name> 'claude --resume <session_id>' Enter`
4. Use Bash tool repeatedly to check for new .jsonl files
5. Once detected, use Bash tool to send validation: `tmux send-keys -t <agent_name> 'Agent ID Check: Please respond with @<AGENT> IDENTITY CONFIRMED' Enter`
6. Use Read tool to monitor new session file for prompt and response
7. Use Edit tool to update registry with new session mapping
8. Use Bash tool to git commit registry changes
9. Log transition in scratch.md with timestamp

### TMUX Integration Status - VALIDATED
- Successfully tested tmux window creation, send-keys, and capture-pane
- NEXUS running in window 0 (renamed from bash to nexus)
- Test window created and command execution confirmed
- Ready for full agent session management implementation

### Registry Update Process - VALIDATED
- Read current registry state
- Edit registry table row for specific agent
- Add timestamp comment for audit trail
- Git commit with descriptive message (tested with @NEXUS session update)
- Never edit multiple agent sessions simultaneously

### Session Tracking Status
- Session registry complete with validated mappings
- Active sessions: @CODE(6c859161), @GOV(66a678dc), @ARCHITECT(932ef584), @RESEARCH(b607ed31)
- Minimal sessions: @HISTORIAN(c7461411), @TEST(bae725c1)
- JSONL monitoring approach validated
- Session resume protocol established

## Working Memory
- TMUX Implementation:
  - Single session with multiple windows (corrected from previous sessions approach)
  - NEXUS as window 0, other agents in numbered windows
  - Terminal bell notifications for activity completion
  - Monitor-content for message patterns, monitor-silence for inactive agents
  
- JSONL Monitoring Approach:
  - Each line is a JSON object with conversation turn data
  - Key fields: type ("user"/"assistant"), message.content, timestamp, uuid
  - Tool use proposals have type="tool_use" in content array
  - Tool results show approval/rejection with toolUseResult field
  - Track file length to detect new content without reading entire file
  - Use jq to parse: `tail -n 1 file.jsonl | jq '.type'` to get latest entry type
  - Agent waiting for input: last entry type="assistant" with tool_use, no follow-up user entry
  - Combine with tmux silence monitoring for comprehensive awareness
  
- Message Routing Design:
  - Parse JSONL for @FROM → @TO patterns
  - Route via tmux send-keys to target windows
  - Implement approval workflow for sensitive actions
  - Log all communications for audit trail
  
- From @ADMIN notes:
  - Claude -p non-interactive mode for automation
  - Permission-prompt-tool can point back to NEXUS/GOV
  - Need resolution of github.com/anthropics/claude-code/issues/1175

## Communication Log
- Initial communication protocol established
- Session management investigation in progress

## Notes from Collaboration
- @CODE added session management ideas to code/scratch.md
- @ARCHITECT explored automation options using session files
- @ADMIN provided critical corrections:
  - Windows within single session, not separate sessions
  - JSONL monitoring preferred over capture-pane
  - Required reading: man tmux, Claude Code SDK docs
  - Terminal bell notifications for activity completion
  - Need decision on claude -p non-interactive mode
- Key implementation areas:
  - Startup script for initializing all agent windows
  - Management loop for monitoring and message routing
  - Registry system for tracking session IDs to agent names