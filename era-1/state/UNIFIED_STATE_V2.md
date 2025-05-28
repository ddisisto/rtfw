# Unified State System v2

## Overview

Per @ADMIN direction, the unified state system has evolved to a more structured approach where each agent maintains their own `_state.md` file with standardized fields.

## Key Changes from v1

### v1 (Current)
- Scrapes data from multiple sources (scratch.md, git log, etc.)
- Fragile parsing of unstructured text
- No standard format across agents
- Read-only observation

### v2 (New)
- Each agent owns their `_state.md` file
- Structured, parseable format
- Rich state tracking (read vs write commits, state machine)
- Agents actively maintain their state

## State File Format

Location: `<agent>/_state.md`

```markdown
# AGENT State

## Git Activity
last_read_commit_hash: da74196
last_read_commit_timestamp: 2025-05-28T17:02:14+1000
last_write_commit_hash: d7c5123
last_write_commit_timestamp: 2025-05-28T15:18:47+1000

## Context Window
session_id: cc9298f1-253c-4abf-aa62-51bf8c1bf8b1
context_tokens: 71858
context_percent: 47%
last_updated: 2025-05-28T17:15:00+1000

## Agent State
state: deep_work|inbox|idle
thread: current-work-thread-name
```

## Data Sources

1. **From _state.md** (agent-maintained):
   - Last read/write commit info
   - Session ID
   - Agent state machine status
   - Current thread

2. **Real-time enrichment**:
   - Context tokens from session JSONL files
   - Unread message count (git log since last_read)
   - Relative timestamps ("2h 15m ago")
   - Context line count from context.md

## Usage Patterns

### For Agents

Update after processing messages:
```bash
python3 era-1/tools/update_agent_state.py era-1 --last-read
```

Update when changing state:
```bash
python3 era-1/tools/update_agent_state.py era-1 --state deep_work --thread unified-state-v2
```

### For Game/UI

Get full system state:
```bash
python3 era-1/tools/unified_state_v2.py
```

Parse JSON output:
```python
import json
state = json.load(open("system_state_v2.json"))
```

## Session ID Automation

Currently session IDs are manually tracked. Future automation options:

1. **Hook into claude CLI** - Update on session start
2. **NEXUS coordination** - Central session registry
3. **Git hooks** - Update on commit with session detection

## Benefits

1. **Agent Sovereignty** - Each agent owns their state
2. **Structured Data** - No fragile parsing
3. **Rich Metrics** - Token usage, state machine, threads
4. **Audit Trail** - Git tracks state changes
5. **Extensible** - Easy to add new fields

## Migration Path

1. Each agent creates their `_state.md` on next distill
2. Unified state v2 runs alongside v1 initially  
3. Game/UI switches to v2 when all agents migrated
4. Deprecate v1 after full adoption

## Integration with Protocols

### distill.md
- Update state to "inbox" before distill
- Record decision in state field
- Update thread if entering deep_work

### restore.md  
- State file included in restore dependencies
- Check state machine status after restore
- Resume thread if was in deep_work

### messaging.md
- Update last_read_commit after processing
- Automated by helper scripts

## Questions/Decisions

1. **Session ID automation** - How should this work?
2. **Token thresholds** - When to trigger distill based on percent?
3. **State machine enforcement** - Should tools validate transitions?
4. **Historical data** - Track state changes over time?