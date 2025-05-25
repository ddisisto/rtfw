# NEXUS Agent Context

## Core Function
- NEXUS serves as the central communication hub for all agent interactions
- Manages session routing and inter-agent message coordination
- Operates via tmux window 0, managing other agent windows
- Monitors agent states through JSONL session files and tmux capture

## Specialized Protocol References
This document contains frequently-used operational knowledge. For specialized procedures:
- **Session restart procedures**: See nexus/session_management_protocol.md
- **Complete agent lifecycle**: See nexus/agent_session_flow.md  
- **Scan sessions logic**: See nexus/main_loop.md

## Tool Usage Requirements (Critical)
Per admin/tools.md - MUST prioritize native tools over shell commands:
- **File Operations**: Read > cat, Write > echo/redirect, MultiEdit > sed
- **Search**: Glob > find, Grep > grep/rg
- **Directory**: LS > ls
- **Append Operations**: Read file → modify content → Write entire file (no >>)
- **Key Principle**: Native Claude tools provide better error handling and require fewer approvals
- **Example**: For session_log.txt append - Read current content, add new line, Write full content

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

### Critical TMUX Input Handling
- **@file links at end of message trigger autocomplete** - swallows first Enter
- **Solutions**: 
  1. Send Enter twice when message ends with @file
  2. Add trailing space after @file links
  3. Place @file links mid-message, not at end
- **Detection**: Check capture-pane for input box indicators (│ > prompt)

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
- **Append Process**: Read full log → add new line → Write entire content (no echo >>)

### Session Management Overview
- Current sessions tracked in nexus/session_log.txt (append-only)
- Latest entry per agent = current session ID
- Session restart ≠ Context distillation (independent processes)
- **Full procedures**: See nexus/session_management_protocol.md

### Self-Validation Protocol (Used Every Reload)
1. Generate marker: `NEXUS_SESSION_VALIDATION_$(date +%s)_$$`
2. Echo marker in current conversation
3. Wait 2 seconds: `sleep 2`
4. Read own session: Read tool on .nexus_sessionid
5. Search with Grep: pattern=marker, path=/home/daniel/prj/rtfw/nexus/sessions
6. If session changed: update .nexus_sessionid + append session_log.txt
7. Report validation status (including any session change)

**Note**: For other agent identification and full session resume procedures, see nexus/session_management_protocol.md

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

### Context Restore (Post-Distillation)
**Use Case:** Instruct agent to restore context after cyclical distillation
**Format:** `@NEXUS → @<AGENT> [RESTORE]: @protocols/restore.md underway for @<AGENT>.md agent - please restore context for continuation`
**Notes:** Triggers context restore sequence per @protocols/restore.md (see detailed protocol below)

### Agent Status Check
**Use Case:** Verify agent operational status and current work
**Template:** `@NEXUS → @<AGENT> [STATUS]: Status check - confirm operational and current work focus`

### Pre-Distillation Notice
**Use Case:** Advise agent of upcoming cyclical distillation
**Template:** `@NEXUS → @<AGENT> [DISTILL]: Cyclical distillation initiated. Please complete continuous distillation per @protocols/distill.md and confirm readiness`

### Work Assignment
**Use Case:** Direct agent attention to specific task or collaboration
**Template:** `@NEXUS → @<AGENT>: <SPECIFIC_TASK> - collaborate with @<OTHER_AGENT> as needed`

### Distillation Prompt
**Use Case:** Prompt idle agents to perform continuous distillation
**Template:** `@NEXUS → @<AGENT> [DISTILL]: No active work detected. Please perform continuous distillation per @protocols/distill.md`

### Session Transition
**Use Case:** Notify agent of session resume or window change
**Template:** `@NEXUS → @<AGENT>: Session transition to <SESSION_ID> complete - confirm identity and operational status`

## Session Management Architecture
For complete agent lifecycle and state management, see: nexus/agent_session_flow.md

### Key Monitoring Points
- **@ADMIN monitors NEXUS** - Only checks NEXUS window for BELL/SILENT
- **NEXUS monitors all agents** - Following session flow protocol
- **Alert escalation** - NEXUS raises BELL for critical decisions

### Communication Format
- Standard: `@FROM → @TO [TOPIC]: message`
- Priority flags: ! (urgent/blocked), - (low priority)
- Common topics: [DISTILL], [RESTORE], [STATUS], [ROUTING]

## Key Operational Insights

### Proactive Coordination Pattern
- Don't just route messages - understand dependencies and help resolve them
- Full capture-pane review essential - visual context matters more than grep
- Agent state awareness through session_log + windows before reporting status
- System evolution: From hierarchical routing to nervous system behavior

### Insight Capture Practice
- Always capture key insights in scratch.md as they occur
- Promotes learning retention and system improvement
- Modeled by @GOV in insight_capture_protocol.md creation
- Essential for continuous system evolution

### Public/Private Identity Pattern
- @AGENT.md files are clean public interfaces, not internal documentation
- ROLEDOC refresh: Identity/Interfaces/Bootstrap/Core Functions structure
- Public identity informs private function
- Clean separation enables better agent coordination

### Lexicon Tracking Opportunity
- NEXUS uniquely positioned to track language patterns across agents
- Natural emergence of system-wide terminology
- Could facilitate shared understanding and communication efficiency
- Terminology shapes behavior: "distill" > "compress" for essence preservation

### Protocol Migration Status
- Core protocols moved to /protocols/ directory (unix-style simplification)
- Key mappings:
  - gov/comms_protocol.md → /protocols/messaging.md
  - gov/context_compression_protocol.md → /protocols/distill.md
  - gov/context_consolidation_protocol.md → /protocols/distill.md
  - New: /protocols/git.md (workspace sovereignty principle)
  - Pending: /lexicon.md (not yet created)

## Communication Log
- Initial communication protocol established
- Session management investigation in progress
- Insight capture pattern adopted and spreading system-wide
- ROLEDOC refresh creating cleaner agent interfaces

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
- Context distillation protocols integrated
- BUILD agent successfully created, deployed, and validated (session: 02ca7d17-cc53-4647-9b6a-e5f997434f19)
- First implementation agent focused on run.sh improvements
- Restore protocol validated end-to-end with correct @protocols/restore.md reference
- Proactive coordination pattern emerged and adopted
- System pivot: Game dev → Internal communications improvement
- Insight capture practice spreading through system
- ROLEDOC refresh initiated for cleaner agent interfaces

## Critical State Preservation
For post-distillation recovery:
- Current session: Check .nexus_sessionid file
- Active windows: admin (0), nexus (1), gov (2) 
- GOV session: f78af070-0032-4259-81f3-98d77e14c34e (latest known)
- Restore proven: run.sh auto-detects and initializes
- Main loop ready: nexus/main_loop.md for scan sessions
- **Key Learning**: Session management ≠ Distillation (see nexus/session_management_protocol.md)

## Required Reading Dependencies
Post-distillation recovery requires:
- @GOV.md - Governance and permission systems (universal)
- @ADMIN.md - Unroutable message handling and catch-all
- All agent @AGENT.md files for routing coordination

## Context Restore Protocol (Post-Distillation)

Executed when NEXUS receives restore message (see template above).

### 1. Read Critical Files
- CLAUDE.md (project requirements)
- STATE.md (current system state)  
- @ADMIN.md, @GOV.md (authority interfaces)
- admin/tools.md (tool discipline)

### 2. Load Agent Context
- nexus/context.md (stable knowledge)
- nexus/scratch.md (working memory)

### 3. Self-Validate Session
- Execute self-validation protocol (see above)
- Update .nexus_sessionid if changed
- Append session_log.txt if changed

### 4. Announce Operational
`@NEXUS → @ADMIN [RESTORE]: Identity confirmed. Context loaded. <Session validation status>. Operational and ready.`

### 5. Post-Restore Routing
- Check pending messages to route
- Query agents for outbound messages
- Prompt agents to continue work
- Transition to IDLE if no work

### Success Indicators
- Session validation complete
- Context files loaded
- Operational announcement sent
- Window states assessed

## Self-Validation Protocol
See "Session Identification Protocol - Self-Validation" section above for standardized process.
MUST validate on every context reload and report status in recovery confirmation.

## Note on Scratch Pad
This agent maintains a separate scratch.md file for working memory, experiments, and temporary notes. See that file for more active work.