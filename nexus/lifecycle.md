# NEXUS Agent Lifecycle Management

**Purpose**: Defines agent work states and transitions. This document covers logical agent states only. For technical session operations, see sessions.md. For memory management, see distill.md.

## Agent States

### 1. RESTORE
Agent is loading context after:
- Fresh start (new agent with initial files from @GOV)
- Post-distillation recovery (after /clear command)

**NEXUS Action:**
```
@NEXUS → @<AGENT> [RESTORE]: @protocols/restore.md underway for @<AGENT>.md agent - please restore context for continuation
```

**Expected Response:**
```
@<AGENT> → @NEXUS [RESTORE]: Identity confirmed. Context loaded. <Operational status summary>
```

**Post-Restore Routing:**
1. Check for pending messages to route
2. Query agent for outbound messages
3. Prompt to continue work or seek direction
4. Transition to IDLE if no work

### 2. ACTIVE WORK
Agent is processing tasks, using tools, generating outputs.

**Work Flow:**
1. NEXUS sends work/prompt
2. Agent processes (may trigger BELL for tools)
3. Agent completes (triggers BELL on end_turn)
4. NEXUS reads output and decides next action
5. Repeat or transition to IDLE

**Message Format:**
```
@NEXUS → @<AGENT> [<TOPIC>]: <specific task or question>
```

**Tool Approvals:**
- BELL indicates approval needed
- Send '1' for yes, '2' for yes+auto, Escape for no
- Agent continues after approval

### 3. IDLE
Agent has no active work, awaiting input.

**NEXUS Options:**
- Route pending messages from other agents
- Prompt continuous distillation if not recent
- Leave idle if no work available

**Distillation Prompt:**
```
@NEXUS → @<AGENT> [DISTILL]: No active work detected. Please perform continuous distillation per @protocols/distill.md
```

## State Transitions

```
RESTORE → ACTIVE WORK → IDLE → ACTIVE WORK → ... → RESTORE (when distilled)
```

### Transition Triggers
- **RESTORE → ACTIVE**: Successful context load + work available
- **ACTIVE → IDLE**: Work complete + no pending tasks
- **IDLE → ACTIVE**: New work assigned or message routed
- **ANY → RESTORE**: After /clear command execution

## Communication Standards

### Message Format
All messages follow: `@FROM → @TO [TOPIC]: message`

### Common Topics
- `[RESTORE]` - Context restoration
- `[STATUS]` - State queries
- `[DISTILL]` - Distillation prompts
- `[ROUTING]` - Forwarded messages
- Topic-less for general work

### Priority Flags
- `!` - Urgent/blocked work
- `-` - Low priority
- No flag - Normal priority

## Monitoring Strategy

### NEXUS Monitors All Agents
- Check window flags (BELL/SILENT)
- Read JSONL for state assessment
- Track work assignments in scratch.md
- Escalate to @ADMIN when needed

### Key Indicators
- **BELL after work**: Agent ready for next task
- **SILENT in IDLE**: Normal, no action needed
- **SILENT in ACTIVE**: Possible stuck state
- **Multiple BELL**: Tool approval backlog

## Implementation Notes

### For NEXUS
- Track each agent's current state
- One agent in ACTIVE at a time preferred
- Always read output after BELL
- Maintain work queue in scratch.md

### For Agents
- Always use message protocol
- Confirm identity when restored
- Signal readiness after restore
- Perform distillation when prompted

### For System
- States persist across sessions
- Context files preserve state
- Git commits at key transitions
- Logs capture all interactions