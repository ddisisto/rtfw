"""
Git-based messaging implementation
"""

import subprocess
import re
from datetime import datetime
from typing import List, Optional

from interfaces import MessageBus, Message


class GitMessageBus(MessageBus):
    """
    Real messaging via git commits
    
    Following patterns from protocols/messaging.md
    """
    
    def __init__(self, repo_root: str = "/home/daniel/prj/rtfw"):
        self.repo_root = repo_root
        self.mention_pattern = re.compile(r'@([A-Z][A-Z0-9-]+)')
    
    def send_message(self, from_agent: str, to_agent: str, content: str) -> str:
        """Send message via git commit, return commit hash"""
        # Format message according to protocol
        message = f"@{from_agent}: {content} @{to_agent}"
        
        # Create empty commit with message
        result = subprocess.run(
            ["git", "commit", "--allow-empty", "-m", message],
            cwd=self.repo_root,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise Exception(f"Git commit failed: {result.stderr}")
        
        # Get the commit hash
        hash_result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=self.repo_root,
            capture_output=True,
            text=True
        )
        
        return hash_result.stdout.strip()
    
    def get_recent_messages(self, count: int = 20) -> List[Message]:
        """Get recent messages from git log"""
        # Get commits with @ mentions
        result = subprocess.run(
            ["git", "log", f"-{count}", "--oneline", "--grep=@"],
            cwd=self.repo_root,
            capture_output=True,
            text=True
        )
        
        messages = []
        for line in result.stdout.splitlines():
            if line:
                message = self._parse_commit_line(line)
                if message:
                    messages.append(message)
        
        return messages
    
    def get_messages_for_agent(self, agent_name: str, count: int = 10) -> List[Message]:
        """Get messages mentioning specific agent"""
        # Search for @AGENT mentions
        result = subprocess.run(
            ["git", "log", f"-{count * 2}", "--oneline", f"--grep=@{agent_name}"],
            cwd=self.repo_root,
            capture_output=True,
            text=True
        )
        
        messages = []
        for line in result.stdout.splitlines():
            if line and f"@{agent_name}" in line:
                message = self._parse_commit_line(line)
                if message:
                    messages.append(message)
                    if len(messages) >= count:
                        break
        
        return messages
    
    def _parse_commit_line(self, line: str) -> Optional[Message]:
        """Parse git log --oneline output into Message"""
        parts = line.split(" ", 1)
        if len(parts) != 2:
            return None
        
        hash_str, content = parts
        
        # Extract author from content if it starts with @AUTHOR:
        author = "Unknown"
        if content.startswith("@"):
            match = re.match(r'@([A-Z][A-Z0-9-]+):', content)
            if match:
                author = match.group(1)
        
        # Extract all mentions
        mentions = self.mention_pattern.findall(content)
        
        # For now, use a simple timestamp (could enhance with full git log later)
        timestamp = datetime.now()  # Placeholder
        
        return Message(
            hash=hash_str,
            author=author,
            content=content,
            timestamp=timestamp,
            mentions=mentions
        )