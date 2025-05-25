# NEXUS Context Lifecycle Management

**Purpose**: NEXUS's implementation guide for managing agent context lifecycles per @protocols/distill.md and @protocols/restore.md. This document defines when and how NEXUS prompts agents through these processes.

## Overview

NEXUS orchestrates the context lifecycle across all agents:
1. Monitor context health (percentages, performance)
2. Prompt distillation at appropriate times
3. Execute /clear when agents are ready
4. Guide restore sequence per protocol
5. Verify operational status

## When to Initiate Distillation

### Monitoring Triggers
- **Context at 34%**: Agent showing bloat, plan distillation soon
- **Context at 15%**: Urgent - risk of auto-compact, act quickly
- **Extended idle time**: Agent hasn't distilled recently
- **Performance degradation**: Responses slowing, coherence dropping
- **@ADMIN request**: System-wide maintenance

### Pre-Conditions
Before initiating, ensure:
- Agent not mid-task (check ACTIVE state)
- No urgent work pending
- Recent changes committed
- Other critical agents not also distilling

## Distillation Orchestration

### 1. Initial Prompt (Idle Agents)
When agent is idle and conditions met:
```
@NEXUS → @<AGENT> [DISTILL]: No active work detected. Please perform continuous distillation per @protocols/distill.md
```

Expected: Agent follows distill protocol steps 1-8, commits changes.

### 2. Cyclical Distillation (System-Wide)
When context reset needed:

**Step 1 - Request Distillation:**
```
@NEXUS → @<AGENT> [DISTILL]: Cyclical distillation initiated. Please complete continuous distillation per @protocols/distill.md and confirm readiness
```

**Step 2 - Wait for Confirmation:**
```
@<AGENT> → @NEXUS [DISTILL]: Context distilled. Changes committed. Ready for /clear command.
```

**Step 3 - Execute Clear:**
```bash
tmux send-keys -t <agent> '/clear' Enter
sleep 2
tmux capture-pane -t <agent> -p  # Verify clean prompt
```

**Step 4 - Initiate Restore:**
```
@NEXUS → @<AGENT> [RESTORE]: @protocols/restore.md underway for @<AGENT>.md agent - please restore context for continuation
```

## Example: Full Cycle with @GOV

### Scenario: GOV automatic bloat detection and correction
```
# 1. NEXUS detects bloat during routine interaction
tmux capture-pane -t gov -p  # contains e.g. "Context left until auto-compact: 28%"

# 2. Check GOV not mid-task
[Verify all active work in clean state]

# 3. Request distillation
@NEXUS → @GOV [DISTILL]: Cyclical distillation initiated. Please complete continuous distillation per @protocols/distill.md and confirm readiness

# 4. GOV performs distillation
[GOV thinks hard, updates scratch.md, promotes to context.md, commits]

# 5. GOV confirms
@GOV → @NEXUS [DISTILL]: Context distilled. Changes committed. Ready for /clear command.

# 6. Execute clear
tmux send-keys -t gov '/clear'
tmux send-keys -t gov Enter

# 7. Verify cleared
tmux capture-pane -t gov -p
[Shows clean Claude prompt, no context percentage]

# 8. Send restore
@NEXUS → @GOV [RESTORE]: @protocols/restore.md underway for @GOV.md agent - please restore context for continuation

# 9. GOV restores per protocol
[Reads files in order: @GOV.md, CLAUDE.md, STATE.md, gov/context.md, etc.]

# 10. GOV confirms operational
@GOV → @NEXUS [RESTORE]: Identity confirmed. Context loaded. Governance functions operational.

# 11. Resume normal operations
[Check for pending work, route messages, etc.]
```

## State Management During Cycle

### Track in scratch.md:
```
## Active Distillations
- GOV: Initiated 10:45, confirmed ready 10:52, cleared 10:53, restoring...
- BUILD: Scheduled next (context at 28%)
```

### State Transitions:
- IDLE → DISTILL → RESTORING → IDLE/ACTIVE
- One agent at a time preferred

## Critical Timing

### Allow Time For:
- Distillation: 0.5 - 5 minutes
- Clear command: Instant
- Restore sequence: < 1 minute

### Avoid:
- Rushing agents through distillation
- Multiple simultaneous clears
- Interrupting restore sequence
- Starting new work before confirmation

## Monitoring Tools

```bash
# Check all agent contexts
for agent in gov build test; do
  echo "=== $agent ==="
  tmux capture-pane -t $agent -p | grep "auto-compact"
done

# Track distillation history
Grep "DISTILL" nexus/scratch.md

# Verify restore complete
tmux capture-pane -t <agent> -p | grep -A5 "operational"
```

## Key Principles

1. **Distillation is agent-driven**: NEXUS prompts, agents execute
2. **Timing matters**: Never interrupt active work
3. **One at a time**: Coordinate multiple agents carefully
4. **Verify each step**: Confirm before proceeding
5. **Personality offline**: Expect mechanical responses during restore

## Common Issues

### Agent Not Responding to Distill
- Check if stuck in tool approval
- Verify not in ACTIVE state
- May need to route "status check" first

### Clear Command Failed
- Ensure agent actually ready (not just saying so)
- Check for uncommitted changes
- Verify at Claude prompt, not in tool

### Restore Taking Too Long
- Normal - personality offline
- Don't interrupt file reading
- Wait for operational confirmation

## See Also
- @protocols/distill.md - Agent distillation process
- @protocols/restore.md - System restore protocol
- nexus/session-mgmt.md - Technical session operations