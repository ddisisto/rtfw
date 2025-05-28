# Deep Work Protocol

## Purpose

Execute focused work on a single thread with progress tracking and context awareness.

## Entry Conditions

Agents enter deep_work from distill when:
- Complex task queued in inbox
- Continuing existing thread
- Starting new implementation
- Context tokens allow (check _state.md)

## Deep Work Process

1. **Declare thread** - Commit with `@AGENT [deep_work/thread-name]: Starting X`
2. **Focus single thread** - One task, clear goal
3. **Progress updates** - Regular commits showing advancement
4. **Monitor context** - Check _state.md periodically for token usage
5. **Respect max_tokens** - Exit before limit (set in distill)
6. **Handle interrupts** - Only critical @mentions break focus
7. **Complete or pause** - Clear endpoint or blocking issue
8. **Exit to inbox** - Always return to message processing

## Decision Inputs

From distill state output:
```
next_state: deep_work
thread: implementation-v2
max_tokens: 30000
```

## Progress Tracking

- Commit frequently with state: `@AGENT [deep_work/thread]: Progress update`
- Update scratch.md with insights during work
- Note blocking issues immediately
- Track token usage against max_tokens limit

## Interruption Handling

Critical interrupts only:
- Safety issues
- System-wide blocks  
- @ADMIN direct priority
- Context approaching max_tokens

Non-critical messages wait for next inbox cycle.

## Exit Conditions

- Task complete → inbox
- Blocked on dependency → inbox (will go idle)
- Context at max_tokens → inbox (will distill)
- Critical interrupt → inbox

## Fourth Wall Integration

Read _state.md for:
- `thread` - Current focus area
- `max_tokens` - Allocated budget
- `context_tokens` - Current usage
- `started` - Time in deep work

## Example Flow

```
[distill] → [deep_work]: Begin focused task
[deep_work] → [inbox]: Task complete or blocked
[inbox] → [distill]: Process and decide next
```

## Governance

Protocol maintained by @GOV. Deep work is sacred focus time.