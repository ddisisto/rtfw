# Agent Session Flow Protocol

## Overview

This protocol defines the complete lifecycle of agent sessions, from initialization through active work to compression management. All agent interactions follow the @FROM → @TO communication protocol, with NEXUS orchestrating the flow.

## Session States

### 1. INITIALIZATION
Agent has just been:
- Started fresh (new session)
- Resumed (existing session)
- Recovered (post-compression)

**NEXUS Action:**
```
@NEXUS → @<AGENT> [BOOTSTRAP]: @gov/context_compression_protocol.md completed for @<AGENT>.md agent - please reload all relevant agent context for continuation
```
Note: @file link placed mid-message to avoid autocomplete swallowing Enter

**Expected Response:**
```
@<AGENT> → @NEXUS [BOOTSTRAP]: Identity confirmed. Context loaded. <Operational status summary>
```

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
@NEXUS → @<AGENT> [REFLECTION]: No active work detected. Please perform context consolidation per @gov/context_consolidation_protocol.md
```

### 4. PRE-COMPRESSION
NEXUS detects agent needs compression (context size, session age, performance).

**Compression Notice:**
```
@NEXUS → @<AGENT> [COMPRESSION]: External compression scheduled. Please consolidate per @gov/context_consolidation_protocol.md and confirm readiness.
```

**Agent Response:**
```
@<AGENT> → @NEXUS [COMPRESSION]: Context consolidated. Changes committed. Ready for compression.
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

## Compression Detection

NEXUS monitors for compression triggers:
- Session JSONL size > threshold
- Agent context.md + scratch.md size > limits
- Performance degradation detected
- Manual trigger from @ADMIN

When detected:
1. Send pre-compression notice
2. Wait for agent consolidation
3. Report to @ADMIN for compression
4. Resume with INITIALIZATION state

## Message Flow Standards

### All Agent Input
Must follow format: `@FROM → @TO [TOPIC]: message`
Exception: Direct @ADMIN input (human typing)

### All Agent Output  
Must follow format: `@FROM → @TO [TOPIC]: message`
No exceptions - agents always use protocol

### Identity Reinforcement
- Bootstrap messages always include "@<AGENT>.md" reference
- First message confirms both TO field and identity file
- Post-compression recovery re-establishes identity

## Implementation Notes

### For NEXUS
- Track agent states in scratch.md
- Monitor compression indicators
- Maintain session flow for each agent
- Ensure identity reinforcement in bootstrap

### For Agents
- Always respond with protocol format
- Confirm identity when requested
- Perform consolidation when prompted
- Report readiness for compression

### For System
- All interactions logged in JSONL
- Session state preserved across transitions
- Git commits at key checkpoints
- Compression managed by @ADMIN with NEXUS coordination