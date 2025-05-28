# Lifecycle-Protocol Integration

## Core Principle
States map directly to protocols. Each state has clear entry/exit conditions and expected behaviors.

## State-Protocol Mapping

### 1. bootstrap (Protocol: restore.md → bootstrap section)
**Entry**: Cold start or post-logout
**Protocol**: 
- Load @AGENT.md, CLAUDE.md, SYSTEM.md
- Read agent/_state.md for last known state
- Load context.md, scratch.md
- Check git log for context (no actions)
- Update _state.md: `state: inbox`
**Exit**: Always to inbox
**Commit**: `@AGENT: [STATE:bootstrap] Restored from COMMIT_HASH`

### 2. inbox (Protocol: messaging.md)
**Entry**: From bootstrap, deep_work completion, or idle timeout
**Protocol**:
- Read _state.md for last_read_commit
- Check messages: `git log LAST_READ..HEAD | grep -E '@(AGENT|ALL)'`
- Process quick responses (<3 steps)
- Update _state.md: `last_read_commit: NEW_HASH`
- Queue complex work
**Exit**: Always to distill
**Commit**: `@AGENT: [STATE:inbox] Processed N messages, M queued`

### 3. distill (Protocol: distill.md)
**Entry**: From inbox only
**Protocol**:
- Current thread from _state.md
- Think hard about current thread/conversation
- Update scratch.md with insights
- Promote stable knowledge to context.md
- Decide next state AND thread
- Update _state.md: `state: NEXT_STATE, thread: THREAD_NAME`
**Exit**: To deep_work, idle, or logout
**Commit**: `@AGENT: [STATE:distill] Thread: THREAD, next: STATE`

### 4. deep_work (No specific protocol - focused execution)
**Entry**: From distill only
**Protocol**:
- Thread and max_tokens from _state.md
- Execute focused work on single thread
- Monitor token usage
- Can check critical messages only
- Update _state.md on significant progress
**Exit**: To inbox (on completion/block/token limit)
**Commit**: `@AGENT: [STATE:deep_work] THREAD: specific work done`

### 5. idle (Protocol: periodic messaging.md checks)
**Entry**: From distill only
**Protocol**:
- Set check interval in _state.md
- Periodic message checks
- Update _state.md: `idle_since: TIMESTAMP`
- Clear reason for idle in commits
**Exit**: To inbox (on new relevant message)
**Commit**: `@AGENT: [STATE:idle] Waiting for DEPENDENCY`

### 6. logout (New protocol section in restore.md)
**Entry**: From distill only
**Protocol**:
- Final distill if needed
- Read /logout.log (last N entries)
- Append poetic/practical note
- Update _state.md: `state: offline`
- Final commit
**Exit**: None (session ends)
**Commit**: `@AGENT: [STATE:logout] Context: X%, see logout.log`

## _state.md Architecture (Fourth Wall)

### READ-ONLY for Agents
The _state.md file is maintained by the game system, not agents. It contains objective measurements agents cannot self-assess:
- Actual context token usage
- Real timestamps
- Session IDs
- True file sizes

### Agent Workflow
1. **Read _state.md** for objective truth
2. **Track in scratch.md** for working state
3. **Report via commits** with [STATE:xxx]
4. **Trust the system** over subjective assessment

### Must Read Before
- bootstrap: Check last state/thread
- inbox: Get last_read_commit  
- distill: Get context_percent (objective)
- deep_work: Get thread and max_tokens
- Any decision: Current state/context%

### Tracked in scratch.md
- Perceived state
- Working thread notes
- Subjective progress
- Message checkpoint

### Exception Handling
```python
# Pseudo-code for state updates
try:
    update_state_file(new_state, thread)
    git_add_and_commit(state_file)
except StateUpdateError as e:
    # Raises to ADMIN for review
    alert_admin(f"State update failed: {e}")
    # Continue with safe defaults
```

## Git Integration

### Every Commit Includes
1. Work changes (if any)
2. _state.md updates
3. [STATE:xxx] in message
4. Thread reference if relevant

### Atomic Operations
```bash
# BAD - separate commits
git add mywork.py && git commit -m "Updated feature"
git add _state.md && git commit -m "Updated state"

# GOOD - atomic commit
git add mywork.py _state.md && git commit -m "@AGENT: [STATE:deep_work] Feature: completed X"
```

## Protocol Consolidation

### Merge restore.md sections
1. **Restore** → Post-logout recovery only
2. **Bootstrap** → New section for cold start
3. **Logout** → New section for graceful exit

### Messaging.md always active
- Available in ALL states
- Criticality filter per state
- Integrated with _state.md tracking

### Thread-management.md becomes state-aware
- Threads exist within states
- Thread transitions happen in distill
- Deep_work = single thread focus

## Benefits

1. **Clarity**: State determines available actions
2. **Consistency**: Protocols align with states  
3. **Trackability**: _state.md + commits = full history
4. **Debuggability**: Clear state machine
5. **Integration**: Game sees everything

## Migration Path

1. Update restore.md with bootstrap/logout sections
2. Enforce _state.md updates in all commits
3. Add state validation to agent tools
4. Gradual adoption starting with ERA-1's v2
5. Full system cutover