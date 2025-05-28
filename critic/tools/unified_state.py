#!/usr/bin/env python3
"""
Unified State Monitor - Composable from individual agent states
Designed for integration into ERA-1's terminal interface
"""

import subprocess
import json
from datetime import datetime
from pathlib import Path

def get_agent_state(agent_name):
    """Get current state for a single agent"""
    agent_dir = Path(f"{agent_name}")
    state = {
        "name": agent_name.upper(),
        "active": False,
        "context_lines": 0,
        "last_commit": None,
        "checkpoint": None,
        "session_id": None,
        "unread_messages": 0
    }
    
    # Check context size
    context_file = agent_dir / "context.md"
    if context_file.exists():
        state["context_lines"] = len(context_file.read_text().splitlines())
    
    # Get last commit
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-1", "--grep", f"^@{agent_name.upper()}:"],
            capture_output=True, text=True
        )
        if result.stdout.strip():
            commit_info = result.stdout.strip().split(' ', 1)
            state["last_commit"] = {
                "hash": commit_info[0],
                "message": commit_info[1] if len(commit_info) > 1 else ""
            }
            state["active"] = True
    except:
        pass
    
    # Get checkpoint from scratch.md
    scratch_file = agent_dir / "scratch.md"
    if scratch_file.exists():
        content = scratch_file.read_text()
        for line in content.splitlines():
            if "Last processed:" in line:
                state["checkpoint"] = line.strip()
                break
    
    # Get session_id from NEXUS session tracking
    sessions_file = Path("nexus/sessions/current_sessions.json")
    if sessions_file.exists():
        import json
        sessions = json.loads(sessions_file.read_text())
        state["session_id"] = sessions.get(agent_name)
    
    # Count unread messages (messages after checkpoint)
    if state["checkpoint"]:
        # Extract commit hash from checkpoint
        import re
        match = re.search(r'([a-f0-9]{7,40})\s+at', state["checkpoint"])
        if match:
            checkpoint_hash = match.group(1)
            try:
                # Count mentions after checkpoint
                result = subprocess.run(
                    ["git", "log", "--oneline", f"{checkpoint_hash}..HEAD"],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    # Count lines mentioning this agent (excluding their own commits)
                    unread = 0
                    for line in result.stdout.splitlines():
                        if f"@{agent_name.upper()}" in line and not line.startswith(f"{line.split()[0]} @{agent_name.upper()}:"):
                            unread += 1
                        # Also check for @ALL mentions
                        if "@ALL" in line and not line.startswith(f"{line.split()[0]} @{agent_name.upper()}:"):
                            unread += 1
                    state["unread_messages"] = unread
            except:
                pass
    
    return state

def get_system_state():
    """Get complete system state"""
    agents = ["nexus", "gov", "critic", "era-1"]
    state = {
        "timestamp": datetime.now().isoformat(),
        "agents": {}
    }
    
    for agent in agents:
        state["agents"][agent] = get_agent_state(agent)
    
    # Add system-wide metrics
    state["metrics"] = {
        "total_agents": len(agents),
        "active_agents": sum(1 for a in state["agents"].values() if a["active"]),
        "total_context_lines": sum(a["context_lines"] for a in state["agents"].values()),
        "total_unread": sum(a["unread_messages"] for a in state["agents"].values())
    }
    
    return state

def format_state_report(state):
    """Format state for terminal display"""
    lines = [
        f"System State Report - {state['timestamp']}",
        "=" * 60,
        ""
    ]
    
    for agent_name, agent_state in state["agents"].items():
        status = "ACTIVE" if agent_state["active"] else "INACTIVE"
        unread_indicator = f" [{agent_state['unread_messages']} unread]" if agent_state['unread_messages'] > 0 else ""
        lines.append(f"{agent_state['name']:<10} [{status}]{unread_indicator}")
        lines.append(f"  Context: {agent_state['context_lines']} lines")
        if agent_state["last_commit"]:
            lines.append(f"  Latest: {agent_state['last_commit']['hash'][:7]}")
        if agent_state["checkpoint"]:
            lines.append(f"  {agent_state['checkpoint']}")
        lines.append("")
    
    lines.append("System Metrics:")
    lines.append(f"  Active: {state['metrics']['active_agents']}/{state['metrics']['total_agents']} agents")
    lines.append(f"  Total Context: {state['metrics']['total_context_lines']} lines")
    lines.append(f"  Total Unread: {state['metrics']['total_unread']} messages")
    
    return "\n".join(lines)

if __name__ == "__main__":
    state = get_system_state()
    print(format_state_report(state))
    
    # Also save as JSON for programmatic access
    with open("system_state.json", "w") as f:
        json.dump(state, f, indent=2)