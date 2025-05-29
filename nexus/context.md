# NEXUS Agent Context

## Core Function
- NEXUS serves as the context lifecycle orchestrator and communication hub
- Coordinates distillation and restore cycles across agents
- Operates via tmux window 0, monitoring other agent windows
- Agent states monitored via engine-maintained _state.md files

## Specialized Protocol References
This document contains frequently-used operational knowledge. For specialized procedures:
- **Session management operations**: See nexus/session-mgmt.md
- **Context lifecycle and states**: See nexus/context-lifecycle.md

## Tool Usage Requirements (Critical)
Per admin/tools.md - MUST prioritize native tools over shell commands:
- **File Operations**: Read > cat, Write > echo/redirect, MultiEdit > sed
- **Search**: Glob > find, Grep > grep/rg
- **Directory**: LS > ls
- **Append Operations**: Read file, modify content, Write entire file (no >>)
- **Key Principle**: Native Claude tools provide better error handling and require fewer approvals
- **Example**: For session_log.txt append - Read current content, add new line, Write full content

## Window Architecture
- Single tmux session with multiple agent windows
- NEXUS operates from window 0, managing all other agents
- Window flags indicate agent states (BELL/SILENT/ACTIVE)
- **Technical details**: See nexus/session-mgmt.md

## Communication Protocols (Messaging v2)
- Messages sent via git commits following /protocols/messaging.md
- Format: `@AUTHOR: message mentioning @OTHER as needed`
- Each agent checks own mentions: `git log | grep '@AGENT'`
- Groups emerge naturally: @ALL, @CORE, @WG-ERA, etc
- Checkpoint tracking mandatory to prevent re-processing
- See messaging v2 protocol for precise grep patterns

### Distributed Mention Checking (v2 Implementation)

**When to check**:
- Natural workflow integration (like updating scratch.md)
- After completing tasks
- Start of session
- When idle

**Process**:
```bash
# Check new mentions since last checkpoint
git log --oneline abc123..HEAD | grep -v '^[a-f0-9]* @NEXUS:' | grep '@NEXUS'

# Check sovereignty (others touching your files)
git log --oneline -10 nexus/ | grep -v '^[a-f0-9]* @NEXUS:'

# Update checkpoint in scratch.md
Last processed: def456 at 2025-05-27 18:30:00
```

**Implementation Notes**:
- No central router needed (deprecated)
- Each agent implements own checking rhythm
- See /protocols/messaging.md for complete patterns
- Old git_router.py archived for reference only

## Session Management
- Sessions tracked via game engine through _state.md files
- Each agent has session_id in their _state.md (READ-ONLY)
- Session operations handled by engine, not agents
- Context management separate from session tracking
- **Technical details**: See nexus/session-mgmt.md for tmux operations

## Critical: Claude CLI Input Handling
- **VITAL**: Enter within tmux send-keys creates newlines, NOT submission
- Always send message text and Enter as SEPARATE commands
- Pattern: `tmux send-keys -t <agent> 'message'` then `tmux send-keys -t <agent> Enter`
- This applies to ALL interactions with Claude sessions
- **NEW**: Always capture-pane after starting `claude` to check for theme selection or other prompts

## GitHub Repository
- Repository established: https://github.com/ddisisto/rtfw
- All commits pushed to main branch via @GOV collaboration

## Communication Protocols - ESTABLISHED
- All messages follow format: @AGENT: natural message with @mentions
- Tool confirmation assistance: '1' for Yes, '2' for Yes+don't ask, Escape for No
- **Monitoring Protocol**: Always capture-pane first, assess current activity, respond to specific needs
- **Technical operations**: See nexus/session-mgmt.md

## Common Communication Patterns (v2)

### Context Restore (Post-Distillation)
**Pattern:** Note in scratch.md before sending via tmux
**Example:** `@NEXUS: Hey @AGENT, time for restore per @protocols/restore.md`

### Status Checks
**Pattern:** Natural language mentions
**Example:** `@NEXUS: @GOV how's the protocol migration going?`

### Distillation Coordination
**Pattern:** Direct mention when context high
**Example:** `@NEXUS: @CRITIC at 37% - consider distillation when convenient`

### Work Coordination
**Pattern:** Mention relevant agents naturally
**Example:** `@NEXUS: Working on ERA agents. @GOV need governance model, @CRITIC please review narrative approach`

## Session Management Architecture
For complete agent lifecycle and state management, see: nexus/context-lifecycle.md

### Key Monitoring Points
- **@ADMIN monitors NEXUS** - Only checks NEXUS window for BELL/SILENT
- **NEXUS monitors all agents** - Via tmux windows and capture-pane
- **Alert escalation** - NEXUS raises BELL for critical decisions
- **State queries** - Check agent _state.md files for objective truth


### Communication Format (v2)
- Simple: `@AGENT: message mentioning @OTHER naturally`
- Urgency through natural language: "urgent", "when you can", "FYI"
- Topics emerge through repetition, not syntax
- Groups form by convention: @ALL, @CORE, @ERA-WG

## Key Operational Insights

### ERA-1 Support Architecture (2025-05-28)
- Game commands map to real agent operations
- Agent state queries via _state.md files (engine-maintained)
- Engine handles all state tracking and updates
- Foundation Era: 1970s aesthetic with real system integration
- Engine provides state API for game integration
- Tmux pane embedding for live agent viewing within game
- Real-time state via `python critic/tools/unified_state.py`
- Legacy patterns: nexus/agent-data-patterns.md (deprecated)

### Git-Comms Integration
- Clean git_router.py implementation complete
- Progressive disclosure: display-only by default, --deliver for automation
- Abstraction layer: @Router as sender maintains flexibility
- Self-routing enabled: True agent equality in messaging
- Future: Could evolve into daemon/hook/automation

### Messaging v2 Evolution (Approved)
- Distributed mention checking replaces central routing
- Checkpoint tracking mandatory: Last processed commit in scratch.md
- Precise patterns: `^[a-f0-9]* @AGENT:` for self, `\b@AGENT\b` for mentions
- Combined groups: `@(NEXUS|ALL|CORE)` for efficient checking
- Sovereignty: `git log agent/ | grep -v @AGENT:` shows only others
- Scratch->commit binding: Note messages before committing
- @GOV approved with transition plan in gov/protocol-transition-plan.md

### Proactive Coordination Pattern
- Don't just route messages - understand dependencies and help resolve them
- Full capture-pane review essential - visual context matters more than grep
- Agent state awareness through session_log + windows before reporting status
- System evolution: From hierarchical routing to nervous system behavior

### Orchestration Maturity
- Successfully managed full distill/restore cycles for other agents
- Standard messaging templates proven effective in practice  
- Progressive refinement: Each cycle smoother than last
- Domain ownership model: BUILD deprecated, agents own full stack in their domain
- Git router v2: Production-ready with logging, window detection, admin handling
- Workspace sovereignty: Learned from GOV's accidental file inclusion (1f31cc7)
  - Even well-intentioned agents violate boundaries accidentally
  - Sovereignty checks catch violations immediately
  - Pattern: Check, Flag, Acknowledge, Learn

### Distill/Restore Process Evolution (2025-05-28)
- Messaging protocol handles all coordination stages
- Git commits for: distill request, readiness confirmation, completion
- Tmux only for: /clear execution, restore message (no context)
- Real-time visualization opportunity for ERA-1 implementation
- Comprehensive notes in nexus/distill-restore-notes.md

### Capture-Pane Discipline
- Use full capture-pane output for context (no arbitrary limits)
- Only use tail/head for specific checks (e.g., auto-compact footer)
- Missing context leads to operational confusion
- Post-/clear: Only capture-pane needed to verify, messaging handles coordination

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
- Core protocols in /protocols/ directory:
  - /protocols/messaging.md (git-based communication v2 - LIVE)
  - /protocols/distill.md (context refinement)
  - /protocols/restore.md (context recovery)
  - /protocols/git.md (workspace sovereignty)
- Messaging v2 fully implemented - distributed @mentions, no central routing
- Each agent tracks checkpoints, greps for mentions independently
- Thread management protocol added for multi-conversation handling

## Communication Log
- Initial communication protocol established
- Session management fully documented and operational
- Insight capture pattern adopted and spreading system-wide
- ROLEDOC refresh creating cleaner agent interfaces

## Development History
- Agent renamed from FACILITATOR to NEXUS
- Tmux-based architecture designed with @ADMIN guidance
- Session identification via unique markers validated
- Critical discovery: --resume ALWAYS creates new session ID
- Documentation restructured: session-mgmt.md, context-lifecycle.md, context.md
- Removed outdated: agent_session_flow.md, session_management_protocol.md
- NEXUS role evolved: message router to context lifecycle orchestrator
- Proactive coordination pattern emerged and adopted
- System pivot: Game dev to Internal communications improvement
- BUILD agent deployed, focused on run.sh improvements (deprecated)
- ERA-1 agent created for Foundation Era game implementation
- @CRITIC agent created for system criticism and assumption challenging
- Git-comms protocol implemented - commits as async message queue
- Protocol evolution: Central routing to distributed @mention checking
- External @LOOP context assists ADMIN with various aspects
- System cleanup: Deprecated agents/files removed by GOV (2025-05-28)
- NEXUS.md made compliant with agent structure protocol
- Distill/restore documentation created for ERA-1 integration
- Engine state system adopted (2025-05-28) - replaced manual tracking
- Fourth wall architecture revealed (2025-05-28) - _state.md files are READ-ONLY

## Context Management
- Monitor agent context percentages (34% = plan distillation, 15% = urgent)
  - **ALWAYS** take note of footer containing "auto-compact" message whenever running tmux capture-pane commands, plan to engage agent distillation and restore to address - "auto-compact" process is very lossy and should not be allowed to occur
- Prompt distillation during idle periods if needed
- Execute /clear only after agent confirms readiness
- **Full orchestration guide**: See nexus/context-lifecycle.md

## Required Reading Dependencies
Post-restore recovery requires (in order):
1. NEXUS.md - Identity with explicit implementation patterns
2. CLAUDE.md - System requirements
3. nexus/context.md - This file
4. nexus/scratch.md - Working memory + checkpoint
5. admin/tools.md - Tool discipline
6. nexus/session-mgmt.md - Session validation
7. /protocols/messaging.md - Distributed mentions v2
8. /protocols/thread-management.md - Multi-thread handling
9. Check recent activity per restore protocol

## Context Restore Protocol (Post-Distillation)

When NEXUS receives restore message after /clear:
1. Follow standard restore sequence per @protocols/restore.md
2. Self-validate session per nexus/session-mgmt.md
3. Announce operational status to @ADMIN
4. Check for pending work and resume operations

**Full details**: See nexus/context-lifecycle.md for complete orchestration of this process as it related to your coordination of this process for other agents.

## Self-Validation Protocol
NEXUS session tracked automatically by engine via _state.md.
Tmux validation procedures preserved in nexus/session-mgmt.md for reference.

## Note on Scratch Pad
This agent maintains a separate scratch.md file for working memory, experiments, and temporary notes. See that file for more active work.