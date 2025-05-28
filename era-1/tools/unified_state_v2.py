#!/usr/bin/env python3
"""
Unified State Monitor v2 - Reads from agent _state.md files
Enhances with real-time data from git and session files
"""

import subprocess
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional

def parse_state_file(agent_name: str) -> Dict[str, Any]:
    """Parse agent's _state.md file"""
    state_file = Path(f"{agent_name}/_state.md")
    if not state_file.exists():
        return {}
    
    state = {}
    content = state_file.read_text()
    
    # Parse key-value pairs
    patterns = {
        'last_read_commit_hash': r'last_read_commit_hash:\s*(\w+)',
        'last_read_commit_timestamp': r'last_read_commit_timestamp:\s*(.+)',
        'last_write_commit_hash': r'last_write_commit_hash:\s*(\w+)',
        'last_write_commit_timestamp': r'last_write_commit_timestamp:\s*(.+)',
        'session_id': r'session_id:\s*(.+)',
        'context_tokens': r'context_tokens:\s*(\d+|pending)',
        'context_percent': r'context_percent:\s*(\d+%|pending)',
        'state': r'state:\s*(\w+)',
        'thread': r'thread:\s*(.+)'
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, content)
        if match:
            state[key] = match.group(1).strip()
    
    return state

def get_context_from_session(session_id: str) -> Dict[str, int]:
    """Extract context window usage from session jsonl file"""
    session_file = Path(f"nexus/sessions/{session_id}.jsonl")
    if not session_file.exists():
        return {"tokens": 0, "percent": 0}
    
    # Get last line of jsonl file
    try:
        with open(session_file, 'rb') as f:
            # Seek to end and read backwards to find last complete line
            f.seek(0, 2)  # Go to end
            file_size = f.tell()
            
            # Read last ~4KB to ensure we get the full last line
            read_size = min(4096, file_size)
            f.seek(max(0, file_size - read_size))
            last_chunk = f.read().decode('utf-8', errors='ignore')
            
            # Get last complete line
            lines = last_chunk.strip().split('\n')
            if lines:
                last_line = lines[-1]
                data = json.loads(last_line)
                
                # Extract token usage
                if 'message' in data and 'usage' in data['message']:
                    usage = data['message']['usage']
                    cache_read = usage.get('cache_read_input_tokens', 0)
                    cache_create = usage.get('cache_creation_input_tokens', 0)
                    total_tokens = cache_read + cache_create
                    
                    # Estimate percentage (assuming ~150k context window)
                    percent = int((total_tokens / 150000) * 100)
                    
                    return {"tokens": total_tokens, "percent": percent}
    except:
        pass
    
    return {"tokens": 0, "percent": 0}

def format_age(timestamp_str: str) -> str:
    """Convert timestamp to age format (e.g., '2h 15m ago')"""
    try:
        # Parse various timestamp formats
        for fmt in ["%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d %H:%M:%S %z", "%Y-%m-%d"]:
            try:
                ts = datetime.strptime(timestamp_str.replace(" at ", " "), fmt)
                break
            except:
                continue
        else:
            return timestamp_str  # Return as-is if can't parse
        
        # Calculate age
        now = datetime.now(timezone.utc)
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        
        age = now - ts
        days = age.days
        hours = age.seconds // 3600
        minutes = (age.seconds % 3600) // 60
        
        if days > 0:
            return f"{days}d {hours}h ago"
        elif hours > 0:
            return f"{hours}h {minutes}m ago"
        else:
            return f"{minutes}m ago"
            
    except:
        return timestamp_str

def get_unread_count(agent_name: str, last_read_hash: str) -> int:
    """Count unread messages since last read commit"""
    if not last_read_hash or last_read_hash == "pending":
        return 0
        
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", f"{last_read_hash}..HEAD"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            unread = 0
            for line in result.stdout.splitlines():
                # Count mentions (excluding own commits)
                if f"@{agent_name.upper()}" in line and not line.startswith(f"{line.split()[0]} @{agent_name.upper()}:"):
                    unread += 1
                if "@ALL" in line and not line.startswith(f"{line.split()[0]} @{agent_name.upper()}:"):
                    unread += 1
            return unread
    except:
        pass
    return 0

def get_agent_state(agent_name: str) -> Dict[str, Any]:
    """Get comprehensive state for a single agent"""
    # Start with parsed state file
    state = parse_state_file(agent_name)
    
    # Basic info
    agent_state = {
        "name": agent_name.upper(),
        "active": False,
        "state_machine": state.get("state", "unknown"),
        "thread": state.get("thread", "none"),
        "session_id": state.get("session_id", "unknown")
    }
    
    # Git activity
    if state.get("last_write_commit_hash"):
        agent_state["last_write"] = {
            "hash": state["last_write_commit_hash"],
            "timestamp": state.get("last_write_commit_timestamp", ""),
            "age": format_age(state.get("last_write_commit_timestamp", ""))
        }
        agent_state["active"] = True
    
    if state.get("last_read_commit_hash"):
        agent_state["last_read"] = {
            "hash": state["last_read_commit_hash"],
            "timestamp": state.get("last_read_commit_timestamp", ""),
            "age": format_age(state.get("last_read_commit_timestamp", ""))
        }
    
    # Context window from session file
    if state.get("session_id") and state["session_id"] != "unknown":
        context_info = get_context_from_session(state["session_id"])
        agent_state["context_tokens"] = context_info["tokens"]
        agent_state["context_percent"] = context_info["percent"]
    else:
        agent_state["context_tokens"] = 0
        agent_state["context_percent"] = 0
    
    # Unread messages
    if state.get("last_read_commit_hash"):
        agent_state["unread_messages"] = get_unread_count(agent_name, state["last_read_commit_hash"])
    else:
        agent_state["unread_messages"] = 0
    
    # Context size (legacy - still useful)
    context_file = Path(f"{agent_name}/context.md")
    if context_file.exists():
        agent_state["context_lines"] = len(context_file.read_text().splitlines())
    else:
        agent_state["context_lines"] = 0
    
    return agent_state

def get_system_state() -> Dict[str, Any]:
    """Get complete system state"""
    agents = ["nexus", "gov", "critic", "era-1", "admin"]
    state = {
        "timestamp": datetime.now().isoformat(),
        "agents": {}
    }
    
    for agent in agents:
        if Path(agent).exists():  # Only include agents with directories
            state["agents"][agent] = get_agent_state(agent)
    
    # System metrics
    active_agents = sum(1 for a in state["agents"].values() if a["active"])
    state["metrics"] = {
        "total_agents": len(state["agents"]),
        "active_agents": active_agents,
        "total_context_lines": sum(a["context_lines"] for a in state["agents"].values()),
        "total_context_tokens": sum(a["context_tokens"] for a in state["agents"].values()),
        "total_unread": sum(a["unread_messages"] for a in state["agents"].values()),
        "agents_working": sum(1 for a in state["agents"].values() if a.get("state_machine") == "deep_work"),
        "agents_idle": sum(1 for a in state["agents"].values() if a.get("state_machine") == "idle")
    }
    
    return state

def format_state_report(state: Dict[str, Any]) -> str:
    """Format state for terminal display"""
    lines = [
        f"System State Report - {state['timestamp']}",
        "=" * 70,
        ""
    ]
    
    for agent_name, agent in state["agents"].items():
        status = "ACTIVE" if agent["active"] else "INACTIVE"
        state_info = f"[{agent['state_machine']}]" if agent.get('state_machine') != 'unknown' else ""
        unread = f" [{agent['unread_messages']} unread]" if agent['unread_messages'] > 0 else ""
        
        lines.append(f"{agent['name']:<10} [{status}]{state_info}{unread}")
        
        if agent.get("last_write"):
            lines.append(f"  Last Write: {agent['last_write']['hash'][:7]} ({agent['last_write']['age']})")
        
        if agent.get("last_read"):
            lines.append(f"  Last Read:  {agent['last_read']['hash'][:7]} ({agent['last_read']['age']})")
        
        if agent["context_tokens"] > 0:
            lines.append(f"  Context: {agent['context_tokens']:,} tokens ({agent['context_percent']}%)")
        
        if agent.get("thread") and agent["thread"] != "none":
            lines.append(f"  Thread: {agent['thread']}")
            
        lines.append("")
    
    lines.append("System Metrics:")
    lines.append(f"  Active: {state['metrics']['active_agents']}/{state['metrics']['total_agents']} agents")
    lines.append(f"  Working: {state['metrics']['agents_working']} | Idle: {state['metrics']['agents_idle']}")
    lines.append(f"  Context: {state['metrics']['total_context_tokens']:,} tokens total")
    lines.append(f"  Unread: {state['metrics']['total_unread']} messages")
    
    return "\n".join(lines)

if __name__ == "__main__":
    state = get_system_state()
    print(format_state_report(state))
    
    # Save as JSON for programmatic access
    with open("system_state_v2.json", "w") as f:
        json.dump(state, f, indent=2)