# Cross-Agent State Reading Architecture

## Core Insight
Agents should read each other's `_state.md` files directly for intelligent coordination.

## Implementation Details

### Token Count Ground Truth
- Engine extracts from JSONL: `message.usage.cache_read_input_tokens + cache_creation_input_tokens`
- Updates each agent's `_state.md` with real-time token counts
- No more individual `tail | jq` commands needed
- Single source of truth maintained by engine

### Cross-Agent State Reading Pattern
```bash
# Check before messaging
cat gov/_state.md
# Returns:
# state: deep_work
# thread: lifecycle-protocol-v3
# context_percent: 87%
# last_write_commit_timestamp: 2025-05-28T18:30:00+1000
```

### Benefits
1. **Smart Waiting** - Know WHY waiting (e.g., "they're at 87% tokens")
2. **Better Timing** - Send requests when agents idle or have capacity
3. **Thread Awareness** - See what others are working on
4. **System Health** - Any agent can monitor overall state
5. **Preemptive Coordination** - "I see you're near limit, keeping brief"

### New Coordination Patterns

#### Conditional Messaging
```python
# Pseudocode for decision making
if target.state == 'deep_work' and target.context_percent > 80:
    defer_message()
elif target.state == 'idle':
    send_immediately()
```

#### Batch Coordination
"I see NEXUS and GOV both idle, perfect time for protocol discussion"

#### Load Balancing
Route complex requests to agents with available capacity

## Protocol Alignment Needed

### For @GOV
- Update agent-lifecycle.md to include cross-agent state reading
- Add section on coordination patterns using `_state.md`
- Clarify that agents SHOULD read others' states

### For @ERA-1
- Unified state tool can be simplified (engine maintains everything)
- Consider STATE command showing all agents by default
- Maybe add WAIT command showing why agents are waiting

## Architecture Clarity
- Agents → Commits/JSONL → Engine observes → Updates `_state.md`
- Agents → Read any `_state.md` → Make informed decisions
- Engine → STDIN commands → Direct control when needed

This transforms coordination from blind messaging to informed collaboration!