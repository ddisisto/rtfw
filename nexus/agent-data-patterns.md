# Safe Agent Data Access Patterns for ERA-1

## Overview
This document provides safe, read-only patterns for accessing agent data without violating sovereignty.

## Core Patterns

### 1. Agent Status Detection
```bash
# Check if agent window exists
tmux list-windows | grep -E "^\d+: agent_name"

# Parse window flags (ACTIVE/SILENT/BELL)
tmux list-windows | grep agent_name | grep -o "[-*!]"
```

### 2. Context Size Monitoring
```bash
# Get context.md size safely
wc -l agent_name/context.md 2>/dev/null || echo "0"

# Calculate percentage (rough estimate)
# Assume ~2000 lines = 100% capacity
lines=$(wc -l < agent_name/context.md)
percent=$((lines * 100 / 2000))
```

### 3. Activity Tracking
```bash
# Last commit by agent
git log --oneline -1 --author="@agent_name" --format="%ar"

# Recent activity count
git log --oneline --since="1 hour ago" | grep "^[a-f0-9]* @agent_name:" | wc -l
```

### 4. Message Checkpoint Reading
```bash
# Extract checkpoint from scratch.md (if standardized)
grep -A1 "Message Checkpoint" agent_name/scratch.md | tail -1
```

### 5. Session Mapping
```json
# Read from nexus/sessions/current_sessions.json
{
  "agent_name": "session_id"
}
```

## Python Implementation Guide

### AgentMonitor Interface
```python
import subprocess
import json
from pathlib import Path

class AgentMonitor:
    def get_status(self, agent_name):
        """Return ACTIVE, SILENT, IDLE, or OFFLINE"""
        result = subprocess.run(
            f"tmux list-windows | grep {agent_name}",
            shell=True, capture_output=True, text=True
        )
        if not result.stdout:
            return "OFFLINE"
        if "*" in result.stdout:
            return "ACTIVE"
        if "-" in result.stdout:
            return "SILENT"
        return "IDLE"
    
    def get_context_size(self, agent_name):
        """Return context.md line count"""
        try:
            return len(Path(f"{agent_name}/context.md").read_text().splitlines())
        except:
            return 0
    
    def get_last_activity(self, agent_name):
        """Return last commit timestamp"""
        result = subprocess.run(
            f'git log -1 --format="%ar" --author="@{agent_name}"',
            shell=True, capture_output=True, text=True
        )
        return result.stdout.strip() or "Never"
```

### MessageBus Wrapper
```python
class MessageBus:
    def send_message(self, from_agent, to_agent, content):
        """Send real git commit message"""
        message = f"@{from_agent}: {content} @{to_agent}"
        subprocess.run([
            "git", "commit", "--allow-empty", "-m", message
        ])
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True
        ).stdout.strip()
    
    def get_recent_messages(self, count=10):
        """Get recent commits with @ mentions"""
        result = subprocess.run([
            "git", "log", f"-{count}", "--oneline", "--grep=@"
        ], capture_output=True, text=True)
        
        messages = []
        for line in result.stdout.splitlines():
            parts = line.split(" ", 1)
            if len(parts) == 2:
                messages.append({
                    "hash": parts[0],
                    "content": parts[1]
                })
        return messages
```

## Integration with CRITIC's Unified State

ERA-1 can call CRITIC's unified state tool:
```bash
python critic/tools/unified_state.py
```

Or import and use directly:
```python
from critic.tools.unified_state import get_system_state
state = get_system_state()
```

## Best Practices

1. **Always read-only** - Never modify agent files
2. **Handle missing files** - Agents may not have all files
3. **Cache when appropriate** - Reduce filesystem hits
4. **Respect sovereignty** - Only read documented locations
5. **Fail gracefully** - Missing data shouldn't crash

## Available Data Sources

### Per Agent
- `agent_name/context.md` - Stable knowledge
- `agent_name/scratch.md` - Working notes, checkpoints
- Git log entries by `@agent_name`
- Tmux window status

### System Wide
- `/nexus/sessions/current_sessions.json` - Session mappings
- `/nexus/session_log.txt` - Historical sessions
- Git log for all commits
- Tmux window list

## Security Notes

- No direct file writes to agent directories
- Git commits only through proper channels
- Read access limited to documented files
- No execution of agent code
- No parsing of JSONL session files (privacy)

This should provide ERA-1 with all needed patterns while maintaining system integrity.