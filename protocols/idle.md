# Idle Protocol

## Purpose

Wait productively when blocked or without actionable tasks, while remaining responsive to system needs.

## Entry Conditions

Agents enter idle from distill when:
- No actionable tasks in queue
- Waiting on dependencies
- Blocked by external factors
- System requests pause

## Idle Process

1. **Declare reason** - Commit: `@AGENT [idle]: Waiting for X`
2. **Document blockers** - Clear in scratch.md what's needed
3. **Set check interval** - How often to poll (default: on event)
4. **Monitor mentions** - Watch for:
   - Dependency resolution
   - New priority tasks
   - @ALL broadcasts
   - State change requests
5. **Light maintenance** - Optional:
   - Review old threads
   - Clean workspace
   - Read other agents' states
   - Update documentation
   - Consider direct_io if uncertain what to do
6. **Exit on trigger** - Return to inbox when:
   - Blocker resolves
   - New message arrives
   - Timer expires
   - Context needs refresh

## Entry

Enter via commit when waiting:
```
@AGENT [idle]: Awaiting @OTHER response on thread X
```

## Idle Activities

Permitted during idle:
- Read other agents' _state.md files
- Review system documentation
- Light workspace cleanup
- Pattern recognition
- NOT: Major refactoring or new features

## Exit Triggers

- Git log shows new @mention
- Dependency becomes available
- @ADMIN injection
- Context aging (check _state.md)

## Fourth Wall Integration

Monitor _state.md for:
- `unread_message_count` - New activity
- `context_percent` - May need distill
- Other agents' states - Coordination opportunities

## Example Flow

```
[distill] → [idle]: No actionable tasks
[idle] → [inbox]: Trigger received
[inbox] → [distill]: Process and reassess
```

## Best Practices

- Always specify WHY idle
- Set clear exit conditions
- Don't idle with high context %
- Use for natural pause points

## Governance

Protocol maintained by @GOV. Idle is active waiting, not abandonment.