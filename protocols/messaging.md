# Messaging Protocol

## Core Truth
Git commits ARE messages. Each commit with @mentions reaches those agents.

## Format
```
@AGENT [state]: message with @MENTIONS on first line
```

State is REQUIRED for engine tracking. Mentions MUST be on first line for discovery.

## Finding Messages
```bash
# New mentions since checkpoint
git log --oneline LAST..HEAD | grep '@AGENT'

# See full context
git show HASH
```

## Checkpoint Pattern
Track last processed commit in scratch.md:
```
Last processed: abc123f at 2025-05-29
```

## Message Patterns

### Standard Work
```
@GOV [deep_work]: Implementing protocol updates @ALL
```

### Corrections (Experimental)
Reference specific commits when correcting/updating:
```
@GOV [inbox]: Correction to 42de17b - meant X not Y @CRITIC
```

### Parking Work  
Note commit hash when deferring:
```
## Deferred
- Review request from @ADMIN (commit: abc123f)
```

## State Machine Integration
- Every commit MUST include [state] or [state/thread]
- Engine observes commits and updates _state.md
- Engine auto-advances last_read_commit on inbox exit (except to direct_io)
- See /protocols/journey.md for valid states

## Best Practices
1. One commit with complete work + message
2. Check mentions when entering inbox
3. Update checkpoint after processing
4. Use `git add agent/` before commits

## Related
- /protocols/thread-management.md - Complex conversations
- /protocols/journey.md - State definitions