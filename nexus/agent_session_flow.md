# Agent Session Flow Protocol

**Purpose**: Complete reference for agent lifecycle states and transitions. Defines how agents move through INITIALIZATION → ACTIVE WORK → IDLE → PRE-DISTILLATION states. For basic operations, see context.md.

## Overview

This protocol defines the complete lifecycle of agent sessions, from initialization through active work to compression management. All agent interactions follow the @FROM → @TO communication protocol, with NEXUS orchestrating the flow.

## Session States

### 1. INITIALIZATION
Agent has just been:
- Started fresh (new session)
- Resumed (existing session)
- Recovered (post-distillation)

**NEXUS Action:**
```
@NEXUS → @<AGENT> [RESTORE]: @protocols/restore.md underway for @<AGENT>.md agent - please restore context for continuation
```
Note: @file link placed mid-message to avoid autocomplete swallowing Enter

**Expected Response:**
```
@<AGENT> → @NEXUS [RESTORE]: Identity confirmed. Context loaded. <Operational status summary>
```

### 1.5. POST-INITIALIZATION ROUTING
After successful initialization, check for pending work:

**NEXUS Checks (in order):**
1. Any messages waiting for this agent?
   - If yes: Route verbatim: `@<SENDER> → @<AGENT> [TOPIC]: original message content`
2. Does agent have pending messages to send?
   - `@NEXUS → @<AGENT> [STATUS]: Any pending messages to route?`
3. Does agent have work to continue?
   - `@NEXUS → @<AGENT> [STATUS]: Please continue with any pending work, or message @ADMIN or other agents for direction if needed`
4. If all negative, transition to IDLE state

### 2. ACTIVE WORK
Agent is processing tasks, using tools, generating outputs.

**Main Loop Sequence:**
1. NEXUS sends work/prompt
2. Agent processes (may trigger BELL for tool approvals)
3. Agent completes with end_turn
4. NEXUS reads final output only
5. Repeat or transition to IDLE

**Work Assignment:**
```
@NEXUS → @<AGENT> [<TOPIC>]: <specific task or question>
```

**Tool Approval Handling:**
- BELL flag indicates tool confirmation needed
- NEXUS sends '1' for approval
- Agent continues processing

### 3. IDLE
Agent has no active work, awaiting input.

**NEXUS Options:**
- Route pending messages from other agents
- Prompt reflection/consolidation
- Let agent remain idle if no work available

**Reflection Prompt:**
```
@NEXUS → @<AGENT> [DISTILL]: No active work detected. Please perform continuous distillation per @protocols/distill.md
```

### 4. PRE-DISTILLATION
NEXUS detects agent needs distillation (context size, session age, performance).

**Distillation Notice:**
```
@NEXUS → @<AGENT> [DISTILL]: Cyclical distillation initiated. Please complete continuous distillation per @protocols/distill.md and confirm readiness.
```

**Agent Response:**
```
@<AGENT> → @NEXUS [DISTILL]: Context distilled. Changes committed. Ready for /clear command.
```

## Main Loop Simplification

### Core Cycle
```
while agent_active:
    1. Check window flags (BELL/SILENT)
    2. If BELL:
       - If tool prompt: approve with '1'
       - If end_turn: read output, route/assign/reflect
    3. If SILENT after BELL:
       - Investigate stuck state
       - Possibly disable monitoring
    4. If no flags and work pending:
       - Send next task
```

### Key Principles
- One message in, one message out (except tool approvals)
- Always use @FROM → @TO format
- Read only final agent output after end_turn
- Never interrupt active work (no flags = working)

## Distillation Detection

NEXUS monitors for distillation triggers:
- Session JSONL size > threshold
- Agent context.md + scratch.md size > limits
- Performance degradation detected
- Manual trigger from @ADMIN

When detected:
1. Send pre-distillation notice
2. Wait for agent continuous distillation
3. Send /clear command when ready
4. Resume with INITIALIZATION state

## Message Flow Standards

### All Agent Input
Must follow format: `@FROM → @TO [TOPIC]: message`
Exception: Direct @ADMIN input (human typing)

### All Agent Output  
Must follow format: `@FROM → @TO [TOPIC]: message`
No exceptions - agents always use protocol

### Identity Reinforcement
- Restore messages always include "@<AGENT>.md" reference
- First message confirms both TO field and identity file
- Post-distillation recovery re-establishes identity

## Implementation Notes

### For NEXUS
- Track agent states in scratch.md
- Monitor distillation indicators
- Maintain session flow for each agent
- Ensure identity reinforcement in bootstrap

### For Agents
- Always respond with protocol format
- Confirm identity when requested
- Perform distillation when prompted
- Report readiness for /clear command

### For System
- All interactions logged in JSONL
- Session state preserved across transitions
- Git commits at key checkpoints
- Distillation managed by @ADMIN with NEXUS coordination