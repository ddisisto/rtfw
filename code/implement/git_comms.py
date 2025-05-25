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
        # Discover active agents from @AGENT.md files
        self.active_agents = self._discover_agents()
        
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
    
    def _discover_agents(self) -> List[str]:
        """Discover active agents from @AGENT.md files."""
        agents = []
        for path in Path('.').glob('*.md'):
            if path.stem.isupper() and path.stem not in ['ADMIN', 'NEXUS', 'STATE', 'CLAUDE']:
                agents.append(path.stem)
        return agents
    
    def extract_messages(self, commit: Dict) -> List[Dict]:
        """Extract routable messages from commit."""
        messages = []
        msg = commit['message']
        
        # Pattern 1: @FROM → @TO [TOPIC]: Message (single recipient)
        pattern1 = r'@(\w+)\s*→\s*@(\w+)\s*\[([^\]]+)\](.*):\s*(.+)'
        match = re.match(pattern1, msg, re.DOTALL)
        if match:
            topic = match.group(3)
            # Handle priority flags after topic
            priority_flags = match.group(4).strip()
            content = match.group(5)
            messages.append({
                'from': match.group(1),
                'to': match.group(2),
                'topic': topic + priority_flags,
                'content': content,
                'commit': commit['hash']
            })
            return messages
        
        # Pattern 2: @FROM → @TO1, @TO2 [TOPIC]: Message (multi-recipient)
        pattern2 = r'@(\w+)\s*→\s*@([\w,\s]+)\s*\[([^\]]+)\](.*):\s*(.+)'
        match = re.match(pattern2, msg, re.DOTALL)
        if match:
            from_agent = match.group(1)
            recipients = [r.strip() for r in match.group(2).split(',')]
            topic = match.group(3)
            priority_flags = match.group(4).strip()
            content = match.group(5)
            
            # Expand @ALL to active agents
            for recipient in recipients:
                if recipient == 'ALL':
                    for agent in self.active_agents:
                        messages.append({
                            'from': from_agent,
                            'to': agent,
                            'topic': topic + priority_flags,
                            'content': content,
                            'commit': commit['hash'],
                            'original_to': 'ALL'  # Track expansion
                        })
                else:
                    messages.append({
                        'from': from_agent,
                        'to': recipient,
                        'topic': topic + priority_flags,
                        'content': content,
                        'commit': commit['hash']
                    })
            return messages
        
        # Pattern 3: @AGENT: Simple message (no routing required per protocol)
        # These are just informational signatures, not communications
        
        return messages
    
    def format_nexus_message(self, msg: Dict) -> str:
        """Format message for NEXUS routing."""
        # Show original message format, expanding @ALL in display
        to_display = msg['to']
        if msg.get('original_to') == 'ALL':
            to_display = f"{msg['to']} (via @ALL)"
        return f"@{msg['from']} → @{to_display} [{msg['topic']}]: {msg['content']} [commit: {msg['commit']}]"
    
    def process_new_commits(self, show_all: bool = True) -> List[str]:
        """Process new commits and return formatted messages.
        
        Args:
            show_all: If True, show all → messages. If False, filter by target.
        """
        commits = self.get_commits_since(self.last_processed)
        if not commits:
            return []
        
        all_messages = []
        for commit in commits:
            messages = self.extract_messages(commit)
            for msg in messages:
                # For NEXUS, show all → messages regardless of target
                if show_all or msg['to'] in self.active_agents:
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