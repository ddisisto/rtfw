#!/usr/bin/env python3
"""
Helper script for agents to update their _state.md file
Usage: python update_agent_state.py [agent_name] --field value
"""

import argparse
import re
from pathlib import Path
from datetime import datetime
import subprocess

def update_state_file(agent_name: str, updates: dict):
    """Update agent's _state.md file with new values"""
    state_file = Path(f"{agent_name}/_state.md")
    
    # Read existing content or use template
    if state_file.exists():
        content = state_file.read_text()
    else:
        # Create from template
        content = """# {AGENT} State

## Git Activity
last_read_commit_hash: pending
last_read_commit_timestamp: pending
last_write_commit_hash: pending
last_write_commit_timestamp: pending

## Context Window
session_id: unknown
context_tokens: pending
context_percent: pending
last_updated: {TIMESTAMP}

## Agent State
state: inbox
thread: none
""".replace("{AGENT}", agent_name.upper()).replace("{TIMESTAMP}", datetime.now().isoformat())
    
    # Update fields
    for field, value in updates.items():
        pattern = rf"({field}:\s*)(.+)"
        if re.search(pattern, content):
            content = re.sub(pattern, rf"\1{value}", content)
        else:
            print(f"Warning: field '{field}' not found in state file")
    
    # Update last_updated if any changes
    if updates:
        pattern = r"(last_updated:\s*)(.+)"
        content = re.sub(pattern, rf"\1{datetime.now().isoformat()}", content)
    
    # Write back
    state_file.parent.mkdir(exist_ok=True)
    state_file.write_text(content)
    print(f"Updated {agent_name}/_state.md")

def get_latest_commit_info(agent_name: str, commit_type: str = "write") -> dict:
    """Get latest commit hash and timestamp for agent"""
    try:
        if commit_type == "write":
            # Get last commit BY this agent
            result = subprocess.run(
                ["git", "log", "--oneline", "-1", "--format=%H %aI", f"--author=@{agent_name.upper()}"],
                capture_output=True, text=True
            )
        else:
            # This would need to be tracked from message processing
            # For now, return current HEAD
            result = subprocess.run(
                ["git", "log", "--oneline", "-1", "--format=%H %aI"],
                capture_output=True, text=True
            )
        
        if result.returncode == 0 and result.stdout.strip():
            parts = result.stdout.strip().split()
            return {"hash": parts[0][:7], "timestamp": parts[1]}
    except:
        pass
    
    return {"hash": "unknown", "timestamp": "unknown"}

def main():
    parser = argparse.ArgumentParser(description="Update agent state file")
    parser.add_argument("agent", help="Agent name (e.g., era-1)")
    parser.add_argument("--last-read", help="Update last read commit to current HEAD", action="store_true")
    parser.add_argument("--last-write", help="Update last write commit", action="store_true")
    parser.add_argument("--state", help="Update agent state (inbox/deep_work/idle)")
    parser.add_argument("--thread", help="Update current thread")
    parser.add_argument("--session-id", help="Update session ID")
    parser.add_argument("--field", nargs=2, action="append", help="Update arbitrary field: --field name value")
    
    args = parser.parse_args()
    updates = {}
    
    # Handle boolean flags
    if args.last_read:
        info = get_latest_commit_info(args.agent, "read")
        updates["last_read_commit_hash"] = info["hash"]
        updates["last_read_commit_timestamp"] = info["timestamp"]
    
    if args.last_write:
        info = get_latest_commit_info(args.agent, "write")
        updates["last_write_commit_hash"] = info["hash"]
        updates["last_write_commit_timestamp"] = info["timestamp"]
    
    # Handle value updates
    if args.state:
        updates["state"] = args.state
    
    if args.thread:
        updates["thread"] = args.thread
    
    if args.session_id:
        updates["session_id"] = args.session_id
    
    # Handle arbitrary fields
    if args.field:
        for name, value in args.field:
            updates[name] = value
    
    if updates:
        update_state_file(args.agent, updates)
    else:
        print("No updates specified")

if __name__ == "__main__":
    main()