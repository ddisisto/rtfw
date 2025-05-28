# Inbox Protocol

## Purpose

Process incoming messages and prioritize work when entering active duty from any other state.

## Entry Conditions

Agents enter inbox state:
- After bootstrap completion
- After deep_work completion
- After returning from idle
- When critical messages interrupt current work

## Inbox Process

1. **Update checkpoint** - Note current commit hash in scratch.md
2. **Check new messages** - Since last checkpoint:
   ```bash
   git log --oneline CHECKPOINT..HEAD | grep -v '^[a-f0-9]* @AGENT:' | grep -E '@(AGENT|ALL)'
   ```
3. **Check direct messages** - Any @ADMIN injections in _state.md
4. **Triage messages** - Classify by urgency and complexity:
   - Immediate: Safety issues, blockers, time-sensitive
   - Quick: Can complete in < 3 steps
   - Complex: Requires focused work session
5. **Execute quick tasks** - Complete immediately with commits
6. **Queue complex work** - Note in scratch.md with commit refs
7. **Always exit to distill** - No other exit path

## Decision Output

After processing, agent proceeds to distill which will determine next state.

## Message Handling

- Immediate responses: Execute and commit within inbox
- Complex requests: Queue for deep_work consideration
- Dependencies: Note blockers for idle state
- Unclear requests: Seek clarification before queuing

## Fourth Wall Integration

- Check _state.md for:
  - `last_read_commit_hash` - Start point for message scan
  - `unread_message_count` - Cross-verify your count
  - Direct injections from @ADMIN

## Example Flow

```
[bootstrap] → [inbox]: Check messages, handle quick tasks
[inbox] → [distill]: Always exit through distill
[distill] → {deep_work|idle|logout}: Based on queued work
```

## Governance

Protocol maintained by @GOV. All agents must process messages before other work.