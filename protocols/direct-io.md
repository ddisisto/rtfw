# Direct I/O Protocol

## Purpose

Enable direct collaboration between agents and @ADMIN, bypassing normal lifecycle automation for focused interaction.

## What is Direct I/O?

Direct I/O is a bidirectional state where:
- Either @ADMIN or agent can initiate direct collaboration
- Normal automated state transitions are paused
- Human-in-the-loop interaction takes precedence
- Used for debugging, exceptions, collaboration, or just to chat

## Why Agents Initiate Direct I/O

Agents may transition to direct_io when:
- Uncertain about next steps (especially from idle)
- Encountering exceptions needing human input
- Wanting to discuss approach or get clarification
- Taking a break from automated work

## Entry Patterns

### Explicit Entry
Agent announces transition when detecting direct control:
```
@AGENT [direct_io]: @ADMIN taking direct control @ALL
next_state: direct_io
thread: <current-work-thread>
```

### Implicit Entry
Engine detects @ADMIN interaction patterns:
- Direct session connection
- Manual state manipulation
- Override commands in terminal UI

## Behavior During Direct I/O

### Engine Behavior
- **Pause** all automated state transitions
- **Update** _state.md to show `state: direct_io`
- **Continue** background monitoring (tokens, time, etc.)
- **Resume** automation only on explicit exit

### Agent Behavior
- **Announce** entry for visibility
- **Continue** normal work patterns
- **Surface** important conditions proactively
- **Maintain** awareness via _state.md reads

## Proactive Notifications

Agents SHOULD surface critical conditions during direct_io:

### Context Health
```
@AGENT [direct_io]: Context at 85% - approaching distill threshold @ADMIN
```

### Blocked Work
```
@AGENT [direct_io]: Critical task blocked 2+ hours @ADMIN @DEPENDENT
```

### Time Awareness
```
@AGENT [direct_io]: In direct_io 45min, N tasks pending @ADMIN
```

### System Concerns
```
@AGENT [direct_io]: EXCEPTION - <critical condition> @ADMIN
```

## Exit Patterns

### Normal Exit
Agent announces return to lifecycle:
```
@AGENT [inbox]: Resuming normal lifecycle from direct_io
next_state: inbox
```

### Explicit State
Agent can exit to any valid state:
```
@AGENT [distill]: Exiting direct_io to distill context
next_state: distill
```

## Fourth Wall Considerations

During direct_io:
- Agents cannot measure session duration (check _state.md)
- Token counts remain objective via _state.md
- Engine maintains ground truth while paused
- Collaboration is synchronous but still observable

## Terminal UI Integration

Future terminal UI enhancements:
- Visual indicator when agent in direct_io
- Automatic transition announcements
- Highlight proactive notifications
- Two-way validation of state changes

## Best Practices

1. **Always announce** entry and exit for system visibility
2. **Proactively surface** issues rather than wait
3. **Include context** in notifications (@mentions, specifics)
4. **Trust the engine** to pause automation properly
5. **Exit cleanly** to valid lifecycle state

## Examples

### Debugging Session
```
@ERA-1 [direct_io/engine-fixes]: @ADMIN debugging state engine @ALL
# ... collaborative debugging ...
@ERA-1 [idle]: Debug complete, awaiting next task
```

### Context Overflow
```
@GOV [direct_io]: @ADMIN reviewing protocols
@GOV [direct_io]: Context at 92% - need distill soon @ADMIN
@GOV [distill]: Moving to distill per context pressure
```

### Extended Work
```
@CRITIC [direct_io]: @ADMIN collaborative review session
@CRITIC [direct_io]: 2 hours in direct_io, 5 reviews pending @ADMIN
@CRITIC [deep_work]: Resuming review queue
```

## Governance

Protocol maintained by @GOV. Direct I/O is a first-class state supporting human-AI collaboration.