# ERA-1 State Management

## Overview

This directory contains the unified state management system for the rtfw project. State is composed from individual agent sources in real-time, providing a single source of truth for both the game UI and agent workflows.

## Architecture

### State Sources
- **Agent Context**: `<agent>/context.md` line counts
- **Git Activity**: Last commit per agent from git log
- **Checkpoints**: Message processing status from `<agent>/scratch.md`
- **Session Mapping**: `nexus/sessions/current_sessions.json`

### Integration Points
- **Unified State Tool**: `critic/tools/unified_state.py` aggregates all state
- **Game UI**: STATUS command calls unified state for real-time data
- **System Pause**: When UI not running, agents should halt (defensive programming)

## State Files

### current_sessions.json (symlink to nexus/sessions/)
Maps agent names to active session IDs:
```json
{
  "nexus": "session-uuid",
  "gov": "session-uuid",
  "critic": "session-uuid",
  "era-1": "session-uuid"
}
```

### system_state.json (generated)
Complete system state snapshot created by unified_state.py

## Usage

### From Game UI
```bash
# Show all agents
STATUS

# Show specific agent
STATUS GOV
```

### Programmatic Access
```python
import subprocess
import json

# Get current state
result = subprocess.run(["python3", "critic/tools/unified_state.py"], 
                       capture_output=True, text=True)
state = json.loads(open("system_state.json").read())

# Check if system active
active_agents = state["metrics"]["active_agents"]
if active_agents == 0:
    print("System paused - no UI running")
```

## Design Principles

1. **No Centralized State File** - Always compose from sources
2. **Read-Only Access** - Respects agent sovereignty
3. **Real-Time Accuracy** - No stale cached data
4. **Defensive Programming** - Agents halt when state invalid

## Future: Session Log Parsing

Per @ADMIN preference, we'll transition from tmux capture to session log parsing:
- Parse `.jsonl` files for richer state information
- Extract context window sizes, token usage
- Track message flow between agents
- Monitor distill/restore cycles

## Maintenance

This system is maintained by @ERA-1 as part of the permanent senior systems engineer role.