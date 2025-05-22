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

### NEXUS Session Resume Protocol - STREAMLINED
When resuming any agent session, NEXUS will:
0. Use Bash tool: `tmux new-window -n <agent_name>` to create agent window
1. Use Read tool on nexus/session_log.txt to get current session ID (last entry for agent)
2. Use LS tool on nexus/sessions/ files (baseline)
3. Use Bash tool: `tmux send-keys -t <agent_name> 'claude --resume <session_id>' Enter`
4. Use Bash tool to monitor for new .jsonl files in nexus/sessions/
5. Once detected, use Bash tool to send validation: `tmux send-keys -t <agent_name> 'Agent ID Check: Please respond with @<AGENT> IDENTITY CONFIRMED' Enter`
6. Use Read tool to monitor new session file for prompt and response
7. Use Edit tool to append new session to nexus/session_log.txt
8. Use Bash tool to git commit session log changes
9. Log transition in scratch.md with timestamp

### TMUX Integration Status - VALIDATED
- Successfully tested tmux window creation, send-keys, and capture-pane
- NEXUS running in window 0 (renamed from bash to nexus)
- Test window created and command execution confirmed
- Ready for full agent session management implementation

### Session Detection Issue to Address
- Current approach of "newest file" fails because other active sessions continue updating
- Need better detection method for new session files during resume
- Proposed approach: maintain list of known session IDs, scan for unknown ones
- Alternative: timestamp-based detection within resume window
- Need to discuss optimal implementation with @ADMIN

### Session Log Update Process - STREAMLINED
- Append new entry to nexus/session_log.txt in format: TIMESTAMP AGENT SESSION_ID
- Git commit with descriptive message
- Never edit multiple agent sessions simultaneously
- Prune old entries occasionally when log gets long

### Session Tracking Status - CURRENT
- @NEXUS: ce51677e-8f35-45e0-984d-6dc767ec416e (tmux window 0: nexus)
- @GOV: f5a74925-877c-4c22-9ab0-a14099daca04 (tmux window 1: gov) - VALIDATED
- Remaining legacy sessions: @CODE(6c859161), @ARCHITECT(932ef584), @RESEARCH(b607ed31), @HISTORIAN(c7461411), @TEST(bae725c1)
- JSONL monitoring approach validated
- Session resume protocol established and tested successfully

### Critical Implementation Notes
- Double Enter needed for tmux send-keys commands (newline + submit)
- Session detection: scan for unknown files in nexus/sessions/ vs known session list
- @GOV identity validation successful: prompt + "@GOV IDENTITY CONFIRMED" response
- Symlink nexus/sessions/ working perfectly for all file access

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