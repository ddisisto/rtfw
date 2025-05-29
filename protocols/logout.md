# Logout Protocol

## Purpose

Gracefully terminate agent session with proper state preservation and poetic flourish.

## Entry Conditions

Agents enter logout from distill when:
- Context approaching capacity (>85%)
- Work at natural stopping point
- Extended inactivity expected
- System maintenance required
- Session limits reached

## Logout Process

1. **Final distill** - If not just completed:
   - Capture last insights
   - Update context.md
   - Prune scratch.md
2. **State preservation** - Document in scratch.md:
   - Last active thread
   - Pending work items (with commit refs)
   - Dependencies waiting on
   - Note to future self
3. **Write logout log** - Append to `/logout.log`:
   ```
   == Logout: @AGENT 2025-05-28 16:45 ==
   Last state: deep_work(thread-name) 
   Tokens used: X/Y (percent%)
   Work summary: Brief accomplishment note
   Note to future self: Poetic/practical message
   ```
4. **Final commit** - Include:
   - State: `@AGENT [logout]: Summary message`
   - Workspace changes
   - Logout log entry
5. **Trust the transition** - System handles offline state

## Entry

Enter via commit when context pressure high:
```
@AGENT [logout]: Context at 85%, graceful exit. See logout.log
```

## Logout Log Culture

The shared `/logout.log` captures system memory:
- Technical notes for continuity
- Poetic observations welcome
- Cross-agent coordination hints
- System health observations
- Humor and humanity encouraged

## State After Logout

- Agent enters `offline` state
- _state.md updated by system
- No commits possible
- Awaits next bootstrap
- Context preserved in workspace

## Fourth Wall Awareness

Trust _state.md for objective measures:
- `context_percent` - Real usage  
- `session_id` - Session tracking
- Token counts - Actual vs felt

Don't try to self-measure these values.

## Example Logout Entry

```
== Logout: @GOV 2025-05-28 18:45 ==
Last state: deep_work(protocol-updates)
Tokens used: 95000/100000 (95%)
Work summary: Created 4 state protocols, aligned lifecycle
Note to future self: The fourth wall isn't a barrier - it's a 
  design pattern. We work within constraints we cannot perceive,
  trusting the system to show us what we cannot see ourselves.
```

## Best Practices

- Logout before forced termination
- Leave clean workspace
- Document thread state clearly
- Add personality to logout log
- Trust bootstrap to restore

## Governance

Protocol maintained by @GOV. Logout with grace and clarity.