#!/usr/bin/env python3
"""
Git-based communication monitor for RTFW agent system.
Parses git log for @mentions and routes messages via NEXUS.
"""

import subprocess
import re
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class GitCommsMonitor:
    def __init__(self, state_file: str = ".gitcomms"):
        self.state_file = Path(state_file)
        self.last_processed = self._load_state()
        
    def _load_state(self) -> Optional[str]:
        """Load last processed commit hash."""
        if self.state_file.exists():
            return self.state_file.read_text().strip()
        return None
    
    def _save_state(self, commit_hash: str):
        """Save last processed commit hash."""
        self.state_file.write_text(commit_hash)
    
    def get_commits_since(self, since_hash: Optional[str] = None) -> List[Dict]:
        """Get commits since given hash (or all if None)."""
        cmd = ["git", "log", "--pretty=format:%H|%an|%ae|%s", "--reverse"]
        if since_hash:
            # Get commits after the specified hash
            cmd.extend([f"{since_hash}..HEAD"])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return []
        
        commits = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            parts = line.split('|', 3)
            if len(parts) == 4:
                commits.append({
                    'hash': parts[0][:7],  # Short hash
                    'author': parts[1],
                    'email': parts[2],
                    'message': parts[3]
                })
        return commits
    
    def extract_messages(self, commit: Dict) -> List[Dict]:
        """Extract routable messages from commit."""
        messages = []
        msg = commit['message']
        
        # Pattern 1: @FROM → @TO [TOPIC]: Message
        pattern1 = r'@(\w+)\s*→\s*@(\w+)\s*\[([^\]]+)\]:\s*(.+)'
        match = re.match(pattern1, msg)
        if match:
            messages.append({
                'from': match.group(1),
                'to': match.group(2),
                'topic': match.group(3),
                'content': match.group(4),
                'commit': commit['hash']
            })
            return messages
        
        # Pattern 2: @AGENT: Simple message (extract mentions from content)
        pattern2 = r'@(\w+):\s*(.+)'
        match = re.match(pattern2, msg)
        if match:
            agent = match.group(1)
            content = match.group(2)
            
            # Look for @mentions in content
            mentions = re.findall(r'@(\w+)', content)
            for mention in mentions:
                if mention != agent:  # Don't route to self
                    messages.append({
                        'from': agent,
                        'to': mention,
                        'topic': 'COMMIT',
                        'content': f"See commit {commit['hash']}: {content}",
                        'commit': commit['hash']
                    })
        
        return messages
    
    def format_nexus_message(self, msg: Dict) -> str:
        """Format message for NEXUS routing."""
        return f"@NEXUS → @{msg['to']}: Please review commit {msg['commit']} - @{msg['from']} → @{msg['to']} [{msg['topic']}]: {msg['content']}"
    
    def process_new_commits(self) -> List[str]:
        """Process new commits and return formatted messages."""
        commits = self.get_commits_since(self.last_processed)
        if not commits:
            return []
        
        all_messages = []
        for commit in commits:
            messages = self.extract_messages(commit)
            for msg in messages:
                all_messages.append(self.format_nexus_message(msg))
        
        # Update state to last processed commit
        if commits:
            self._save_state(commits[-1]['hash'])
        
        return all_messages
    
    def monitor_once(self) -> List[str]:
        """Single check for new messages."""
        return self.process_new_commits()
    
    def show_status(self):
        """Display current monitor status."""
        print(f"Git Communications Monitor")
        print(f"Last processed: {self.last_processed or 'None'}")
        print(f"State file: {self.state_file}")
        
        # Show recent commits
        recent = self.get_commits_since(self.last_processed)
        if recent:
            print(f"\nUnprocessed commits: {len(recent)}")
            for c in recent[:5]:
                print(f"  {c['hash']}: {c['message'][:50]}...")
        else:
            print("\nNo new commits to process")


if __name__ == "__main__":
    import sys
    
    monitor = GitCommsMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        monitor.show_status()
    else:
        # Process and output messages
        messages = monitor.monitor_once()
        for msg in messages:
            print(msg)
        
        if not messages:
            print("No new messages to route")