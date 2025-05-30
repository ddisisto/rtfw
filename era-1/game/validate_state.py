#!/usr/bin/env python3
"""
State Validation Tool - Check consistency without running engine
Safe to run alongside active engine
"""

import sys
from pathlib import Path
from datetime import datetime
import subprocess
import json

sys.path.insert(0, str(Path(__file__).parent))

from engine.jsonl_parser import JSONLParser


def get_git_state(agent: str) -> tuple[str, str]:
    """Get latest state from git log"""
    result = subprocess.run(
        ["git", "log", "--oneline", "--grep", f"@{agent.upper()}"],
        capture_output=True, text=True
    )
    
    for line in result.stdout.strip().split('\n'):
        if f"@{agent.upper()} [" in line:
            # Extract state from commit message
            # Format: "hash @AGENT [state]: message"
            parts = line.split('[', 1)
            if len(parts) > 1:
                state = parts[1].split(']', 1)[0].split('/')[0]
                commit = line.split()[0]
                return state, commit
    
    return "unknown", "none"


def read_state_file(agent_dir: Path) -> dict:
    """Read _state.md and extract key values"""
    state_file = agent_dir / "_state.md"
    if not state_file.exists():
        return {}
    
    content = state_file.read_text()
    state_data = {}
    
    for line in content.splitlines():
        if line.startswith("state:"):
            state_data["state"] = line.split(":", 1)[1].strip()
        elif line.startswith("last_write_commit_hash:"):
            state_data["commit"] = line.split(":", 1)[1].strip()
        elif line.startswith("context_percent:"):
            state_data["context"] = line.split(":", 1)[1].strip()
        elif line.startswith("unread_message_count:"):
            state_data["unread"] = line.split(":", 1)[1].strip()
            
    return state_data


def check_jsonl_session(sessions_dir: Path, agent: str) -> dict:
    """Parse JSONL to get current session info"""
    symlink = sessions_dir / agent
    if not symlink.exists():
        return {}
        
    target = symlink.resolve()
    session_file = target / f"{target.name}.jsonl"
    
    if not session_file.exists():
        return {}
    
    parser = JSONLParser()
    messages = parser.parse_tail(session_file)
    tokens, _ = parser.count_tokens(messages)
    
    return {
        "session_id": target.name,
        "tokens": tokens,
        "percent": f"{tokens / 128000 * 100:.1f}%"
    }


def main():
    """Validate state consistency across git, files, and sessions"""
    project_root = Path(__file__).parent.parent.parent
    sessions_dir = project_root / "_sessions"
    
    print("State Validation Report")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    agents = ["critic", "era-1", "gov", "nexus"]
    
    for agent in agents:
        print(f"\n{agent.upper()}")
        print("-" * 30)
        
        # Get data from three sources
        git_state, git_commit = get_git_state(agent)
        file_data = read_state_file(project_root / agent)
        session_data = check_jsonl_session(sessions_dir, agent)
        
        # Display comparison
        print(f"  Git state:    {git_state} (commit: {git_commit[:7]})")
        print(f"  File state:   {file_data.get('state', 'NO FILE')}", end="")
        if file_data.get('commit'):
            print(f" (commit: {file_data['commit'][:7]})", end="")
        print()
        
        # Check consistency
        if git_commit != file_data.get('commit', ''):
            print(f"  ⚠️  MISMATCH: Git commit != File commit")
        
        if session_data:
            print(f"  Session:      {session_data['session_id'][:8]}...")
            print(f"  Context:      {session_data['percent']} ({session_data['tokens']} tokens)")
            
            # Compare with file
            if file_data.get('context'):
                if session_data['percent'] != file_data['context'].replace('%', '') + '%':
                    print(f"  ⚠️  MISMATCH: Parsed {session_data['percent']} != File {file_data['context']}")
        
        if file_data.get('unread'):
            print(f"  Unread msgs:  {file_data['unread']}")
    
    print("\n" + "=" * 60)
    print("Use this to validate engine behavior without interference")


if __name__ == "__main__":
    main()