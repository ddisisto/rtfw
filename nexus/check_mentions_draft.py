#!/usr/bin/env python3
"""
Simple mention checker - each agent can copy and customize.
Basic patterns that agents might find useful as starting point.

Key efficiency pattern: Track last check time to avoid re-reading.
Each agent could store in their scratch.md or dedicated file:
  last_mention_check: 2025-05-27 13:45:00
Then use --since="2025-05-27 13:45:00" for incremental checks.
"""

import subprocess
import sys
from datetime import datetime, timedelta

def get_mentions(agent_name, hours=24, include_groups=None, exclude_self=True):
    """Find mentions of agent in recent git history."""
    
    # Build word-boundary patterns for precision
    patterns = [f"\\b@{agent_name}\\b"]
    if include_groups:
        patterns.extend(f"\\b@{group}\\b" for group in include_groups)
    
    # Create grep pattern
    grep_pattern = "|".join(patterns)
    
    # Get git log for time period
    since = (datetime.now() - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M")
    
    if exclude_self:
        # Exclude commits that start with @AGENT:
        cmd = f'git log --since="{since}" --oneline | grep -v "^[a-f0-9]* @{agent_name}:" | grep -E "{grep_pattern}"'
    else:
        cmd = f'git log --since="{since}" --oneline | grep -E "{grep_pattern}"'
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            return result.stdout.strip().split('\n')
    except:
        pass
    
    return []

def check_workspace(agent_name, hours=6):
    """Check for changes to agent's workspace by others."""
    
    workspace = f"{agent_name.lower()}/"
    since = (datetime.now() - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M")
    
    # Direct path-based query - much cleaner!
    cmd = f'git log --since="{since}" --oneline {workspace}'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if not result.stdout:
        return []
    
    # Filter out our own commits
    changes = []
    for line in result.stdout.strip().split('\n'):
        if line and f"@{agent_name}:" not in line:
            changes.append(line)
    
    return changes

def show_summary(agent_name, groups=None):
    """Simple summary display."""
    
    print(f"\n=== Mention Check for @{agent_name} ===")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Recent mentions
    mentions = get_mentions(agent_name, hours=24, include_groups=groups)
    if mentions:
        print(f"\nRecent mentions (24h):")
        for mention in mentions[:10]:  # Show first 10
            print(f"  {mention}")
        if len(mentions) > 10:
            print(f"  ... and {len(mentions)-10} more")
    else:
        print("\nNo recent mentions")
    
    # Workspace changes
    changes = check_workspace(agent_name, hours=6)
    if changes:
        print(f"\nWorkspace changes by others (6h):")
        for change in changes[:5]:
            print(f"  {change}")
    
    print()

# Example usage patterns each agent might implement:

if __name__ == "__main__":
    # NEXUS might check with groups
    show_summary("NEXUS", groups=["ALL", "CORE"])
    
    # Or agents could build their own integration:
    # - Check on startup
    # - Check periodically  
    # - Parse and route to local handling
    # - Whatever works for them