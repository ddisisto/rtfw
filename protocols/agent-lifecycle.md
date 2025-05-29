# Agent Lifecycle Protocol

## Purpose
Formalize agent work patterns into observable states, enabling real-time monitoring and coordination through the game interface.

## Core States

The lifecycle consists of eight states, each with its own protocol:

### 1. bootstrap
Entry from offline, cold-start context loading.  
See: `/protocols/bootstrap.md`

### 2. inbox  
Message processing and task prioritization.  
See: `/protocols/inbox.md`

### 3. distill
Context refinement and next-state decision.  
See: `/protocols/distill.md`

### 4. deep_work
Focused execution on single thread.  
See: `/protocols/deep-work.md`

### 5. idle
Active waiting with clear triggers.  
See: `/protocols/idle.md`

### 6. logout
Graceful termination with state preservation.  
See: `/protocols/logout.md`

### 7. offline
Post-logout state maintained by system.  
No protocol needed - system managed.

### 8. direct_io
@ADMIN direct control with paused automation.  
See: `/protocols/direct-io.md`

## State Transitions

```
offline → bootstrap → inbox → distill → {deep_work|idle|logout}
                        ↑         ↑          ↓        ↓      ↓
                        ←---------←----------←--------←      ↓
                                                            ↓
                     offline ←------------------------------←

direct_io ←→ {any state except offline}
```

## State Reporting

Agents report state via git commits:
```
@AGENT [deep_work]: Beginning messaging protocol update
@AGENT [idle]: Waiting for @NEXUS session data format
@AGENT [logout]: Context at 95%, scheduling distill/restore
```

## Context Window Management

Each state transition includes:
- Current token count
- Maximum allowed
- Forced logout threshold
- Visual indicators in game:
  - Green: 0-60% capacity
  - Yellow: 60-85% capacity  
  - Red: 85-100% capacity
  - Flashing: Forced logout imminent

## System Integration

### Game Monitor Features
- Real-time state visualization per agent
- Context window meters
- Message flow tracing
- State transition logs
- Frozen when game not running

### Direct Connection Override
See `/protocols/direct-io.md` for complete behavior.
- @ADMIN can enter direct_io from any state
- Engine pauses automated transitions
- Agent announces entry/exit via commits
- Proactive notifications encouraged

### Message Injection
- @ADMIN can append to any agent's inbox
- Shows as system message in state
- Processed on next inbox cycle

## Fourth Wall Architecture

### _state.md is READ-ONLY
The _state.md file is maintained by the game system, not agents. It contains objective measurements agents cannot self-assess:
- Actual context token usage
- Real timestamps
- Session IDs
- True file sizes

### Agent Workflow
1. **Read _state.md** for objective truth
2. **Track in scratch.md** for working state
3. **Report via commits** with [state/thread]
4. **Trust the system** over subjective assessment

### State-Specific Reads
- **bootstrap**: Check last state/thread
- **inbox**: Get last_read_commit
- **distill**: Get context_percent (objective)
- **deep_work**: Get thread and max_tokens
- **All states**: Check current context usage

## Implementation Notes

### State Management
- **_state.md**: READ-ONLY file maintained by game engine
- **Decision outputs**: Each state protocol defines required format
- **Commit format**: `@AGENT [state/thread]: message`

### Engine Implementation
For technical implementation details, see:
- @ERA-1's state engine: `era-1/game/engine/`
- Prompt generator expects protocols at: `/protocols/{state}.md`
- State transitions handled by ThreadedStateEngine

### Shared Artifacts
- `/logout.log`: Cross-agent memory and coordination
- `agent/_state.md`: Objective truth per agent
- Git commits: Message transport and state reporting

## Governance

This protocol affects all agents. Changes require @GOV approval with @ADMIN confirmation.

## Benefits

1. **Predictability** - Know what each agent is doing
2. **Coordination** - See dependencies and blockages  
3. **Efficiency** - Manage context proactively
4. **Culture** - Logout log creates shared memory
5. **Debugging** - State transitions tell stories

## Migration Status

As of 2025-05-29:
- ✓ All state protocols created and aligned
- ✓ State engine v2 implemented by @ERA-1  
- ✓ Agents using new message format
- ⏳ CLI integration pending
- ⏳ Full system cutover pending

The game becomes the window into the living system.