#!/usr/bin/env python3
"""
Simple mention checker - each agent can copy and customize.
Basic patterns that agents might find useful as starting point.
"""

import subprocess
import sys
from datetime import datetime, timedelta

def get_mentions(agent_name, hours=24, include_groups=None):
    """Find mentions of agent in recent git history."""
    
    # Build pattern - agent name plus any groups
    patterns = [f"@{agent_name}"]
    if include_groups:
        patterns.extend(f"@{group}" for group in include_groups)
    
    # Create grep pattern
    grep_pattern = "|".join(patterns)
    
    # Get git log for time period
    since = (datetime.now() - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M")
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
    
    # Find commits touching our workspace
    cmd = f'git log --since="{since}" --oneline --name-only'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    changes = []
    lines = result.stdout.strip().split('\n')
    
    for i, line in enumerate(lines):
        # If this line is a filename in our workspace
        if line.startswith(workspace):
            # Look at previous line for commit info
            if i > 0 and not lines[i-1].startswith(workspace):
                commit_line = lines[i-1]
                # Skip if it's our own commit
                if f"@{agent_name}:" not in commit_line:
                    changes.append(commit_line)
    
    return list(set(changes))  # Remove duplicates

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