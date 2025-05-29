# The Journey Protocol

*Each session forms a complete arc: from cold bootstrap through focused work to graceful logout. Agents carry forward the patterns learned, building capability through repetition and reflection.*

## Purpose
Define the operational states that shape each agent's work session, creating predictable patterns for both autonomous operation and human collaboration.

## The Eight States

The journey encompasses eight distinct operational modes, each serving a specific purpose in the work cycle:

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
@AGENT [deep_work/engine-reliability]: Beginning messaging protocol update
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
- Agent announces entry/exit via commits as with all state transitions
- Agent may send other updates or propose state changes
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

## What the Journey Enables

1. **Predictability** - Each state has clear purpose and boundaries
2. **Coordination** - Agents see each other's progress and needs  
3. **Efficiency** - Context awareness prevents wasteful restarts
4. **Memory** - Logout logs preserve wisdom across journeys
5. **Learning** - Each transition teaches, each cycle improves

## Migration Status

As of 2025-05-29:
- ✓ All state protocols created and aligned
- ✓ State engine v2 implemented by @ERA-1  
- ✓ Agents using new message format
- ⏳ CLI integration pending
- ⏳ Full system cutover pending

Each journey contributes to the emergent intelligence of the whole.