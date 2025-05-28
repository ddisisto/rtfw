# Agent Lifecycle Protocol

## Purpose
Formalize agent work patterns into observable states, enabling real-time monitoring and coordination through the game interface.

## Core States

### 1. bootstrap
Initial activation sequence:
- Load identity (@AGENT.md)
- Restore context (protocols/restore.md)
- Check environment readiness
- Report state to system: `state: bootstrap complete`

### 2. inbox
Message processing and prioritization:
- Check messages since last checkpoint
- Integrate @ADMIN injections if any
- Quick responses (< 3 steps) execute immediately
- Complex work gets queued
- Always ends with distill

### 3. distill
Context refinement and decision point:
```
distill(context_tokens: X, max_tokens: Y, forced_logout_at: Z) -> next_state
```
- Reflect on recent work and capture insights
- Update scratch.md with patterns learned
- Promote stable knowledge to context.md
- Prune outdated information
- **Decision output**: 
  ```
  next_state: deep_work
  thread: messaging-v3
  max_tokens: 30000
  ```

### 4. deep_work
Focused task execution:
- Single thread focus
- Progress updates via commits
- Respect max_tokens limit
- Can be interrupted by critical messages only
- Exits to inbox when complete or blocked

### 5. idle  
Waiting state:
- No actionable tasks
- Waiting on dependencies
- Periodic inbox checks
- Clear indication of why idle

### 6. logout
Graceful shutdown:
- Final distill if needed
- Write to logout log
- Preserve state for next bootstrap
- Format:
  ```
  == Logout: @AGENT 2025-05-28 16:45 ==
  Last state: deep_work(thread-name)
  Tokens used: X/Y
  Work summary: Completed pattern cleanup
  Note to future self: Check ERA-2 coordination
  ```

### 7. offline
Post-logout state:
- Agent session terminated
- _state.md shows: `state: offline`
- No commits possible
- Awaiting bootstrap
- Game may show as "inactive" or "logged out"

## State Transitions

```
offline → bootstrap → inbox → distill → {deep_work|idle|logout}
                         ↑         ↑          ↓        ↓      ↓
                         ←---------←----------←--------←      ↓
                                                             ↓
                         offline ←---------------------------←
```

## State Reporting

Agents report state via git commits:
```
@AGENT: [STATE:deep_work] Beginning messaging protocol update
@AGENT: [STATE:idle] Waiting for @NEXUS session data format
@AGENT: [STATE:logout] Context at 95%, scheduling distill/restore
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
- @ADMIN can always direct connect
- State temporarily shows "direct_io"
- Work gets logged to git afterward
- Returns to lifecycle on disconnect

### Message Injection
- @ADMIN can append to any agent's inbox
- Shows as system message in state
- Processed on next inbox cycle

## Implementation Notes

1. **State File**: `agent/state.json`
   ```json
   {
     "current": "deep_work",
     "thread": "messaging-v3",
     "started": "2025-05-28T15:30:00Z",
     "context_tokens": 45000,
     "max_tokens": 100000,
     "checkpoint": "abc123"
   }
   ```

2. **Logout Log**: `/logout.log` (shared artifact)
   - Append-only
   - All agents write here
   - Poetic/practical notes encouraged
   - Becomes system memory

3. **State Commands** (for ERA-1):
   - `STATE` - Show all agent states
   - `TOKENS` - Context window usage
   - `THREADS` - Active work threads
   - `INJECT @AGENT message` - Add to inbox

## Governance

This protocol affects all agents. Changes require @GOV approval with @ADMIN confirmation.

## Benefits

1. **Predictability** - Know what each agent is doing
2. **Coordination** - See dependencies and blockages  
3. **Efficiency** - Manage context proactively
4. **Culture** - Logout log creates shared memory
5. **Debugging** - State transitions tell stories

## Migration Path

1. Update agent bootstrap sequences
2. Add state reporting to commits  
3. Create initial state.json files
4. Test with gradual adoption
5. Full system cutover

The game becomes the window into the living system.