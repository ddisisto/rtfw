"""
Git Monitor - Tracks agent git activity and messages
"""

import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple, List
from dataclasses import dataclass


@dataclass
class CommitInfo:
    """Information about a git commit"""
    hash: str
    timestamp: datetime
    message: str


class GitMonitor:
    """
    Monitors git repository for agent activity
    
    Tracks:
    - Last read/write commits per agent
    - Unread message counts
    - Recent commit activity
    """
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        
        # Pattern to extract state from commit messages
        # Matches: @AGENT [state]: ... or @AGENT [state/thread]: ...
        self.state_pattern = re.compile(r'^@(\w+)\s*\[(\w+)(?:/(\S+))?\]:', re.IGNORECASE)
    
    def get_unread_count(self, agent_name: str, last_read_hash: str) -> int:
        """
        Count unread messages for an agent since last read commit
        
        Runs: git log --oneline HASH..HEAD | grep -v '^[a-f0-9]* @AGENT:' | grep -E '@AGENT|@ALL' | wc -l
        """
        if not last_read_hash:
            return 0
        
        try:
            # Get commits mentioning this agent (but not from this agent)
            cmd = [
                'git', 'log', '--oneline', f'{last_read_hash}..HEAD'
            ]
            
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Count mentions
            count = 0
            agent_upper = agent_name.upper()
            
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                    
                # Skip agent's own commits
                if f'@{agent_upper}:' in line:
                    continue
                    
                # Count if mentioned
                if f'@{agent_upper}' in line or '@ALL' in line:
                    count += 1
            
            return count
            
        except subprocess.CalledProcessError:
            return 0
    
    def get_last_commits(self, agent_name: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Get last read and write commit hashes for an agent
        
        Returns: (last_read_hash, last_write_hash)
        """
        agent_upper = agent_name.upper()
        
        try:
            # Get last write (agent's own commit)
            cmd_write = [
                'git', 'log', '--oneline', '-1', '--grep', f'^@{agent_upper}:'
            ]
            
            result = subprocess.run(
                cmd_write,
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            last_write = None
            if result.returncode == 0 and result.stdout.strip():
                # Extract hash from "hash message"
                last_write = result.stdout.strip().split()[0]
            
            # For last read, we'd need to parse agent messages or state files
            # This would require looking at commit content
            # For now, return None (would be tracked in _state.md)
            last_read = None
            
            return last_read, last_write
            
        except Exception:
            return None
    
    def get_agent_state_from_commits(self, agent_name: str, since_hash: Optional[str] = None) -> Optional[Tuple[str, Optional[str], str]]:
        """
        Check recent commits for state announcements by this agent
        
        Returns: (state, thread, commit_hash) or None
        """
        agent_upper = agent_name.upper()
        
        try:
            # Get recent commits by this agent
            cmd = ['git', 'log', '--format=%H|%s', '-20', '--grep', f'^@{agent_upper}']
            if since_hash:
                cmd.extend([f'{since_hash}..HEAD'])
            
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            if result.stdout.strip():
                # Check each commit message
                for line in result.stdout.strip().split('\n'):
                    if '|' not in line:
                        continue
                    
                    hash_val, message = line.split('|', 1)
                    match = self.state_pattern.match(message)
                    
                    if match and match.group(1).upper() == agent_upper:
                        state = match.group(2).lower()
                        thread = match.group(3) if match.group(3) else None
                        
                        # Normalize state names
                        state = state.replace('-', '_')
                        
                        return (state, thread, hash_val)
            
            return None
            
        except subprocess.CalledProcessError:
            return None, None
    
    def get_recent_activity(self, limit: int = 10) -> List[dict]:
        """
        Get recent system activity
        
        Returns list of recent commits with agent attribution
        """
        try:
            cmd = ['git', 'log', '--oneline', f'-{limit}']
            
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            activity = []
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                
                parts = line.split(None, 1)
                if len(parts) == 2:
                    hash_val, message = parts
                    
                    # Extract agent from message
                    agent = None
                    if message.startswith('@'):
                        agent_part = message.split(':', 1)[0]
                        agent = agent_part[1:].lower()  # Remove @ and lowercase
                    
                    activity.append({
                        'hash': hash_val,
                        'agent': agent,
                        'message': message
                    })
            
            return activity
            
        except subprocess.CalledProcessError:
            return []
    
    def get_commit_timestamp(self, commit_hash: str) -> Optional[datetime]:
        """Get timestamp for a specific commit"""
        try:
            cmd = ['git', 'show', '-s', '--format=%cI', commit_hash]
            
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            if result.stdout.strip():
                return datetime.fromisoformat(result.stdout.strip())
                
        except (subprocess.CalledProcessError, ValueError):
            pass
            
        return None
    
    def get_last_agent_commit(self, agent_name: str) -> Optional[CommitInfo]:
        """
        Get the last commit made by this agent
        
        Returns CommitInfo with hash, timestamp, and message
        """
        agent_upper = agent_name.upper()
        
        try:
            # Get last commit by this agent
            cmd = [
                'git', 'log', '--format=%H|%cI|%s', '-1', '--grep', f'^@{agent_upper}:'
            ]
            
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            if result.stdout.strip():
                parts = result.stdout.strip().split('|', 2)
                if len(parts) == 3:
                    hash_val, timestamp_str, message = parts
                    timestamp = datetime.fromisoformat(timestamp_str)
                    return CommitInfo(hash=hash_val, timestamp=timestamp, message=message)
                    
        except (subprocess.CalledProcessError, ValueError):
            pass
            
        return None
    
    def count_unread_messages(self, agent_name: str, last_read_hash: str) -> int:
        """
        Count messages mentioning this agent since last read
        
        Same as get_unread_count but with clearer name
        """
        return self.get_unread_count(agent_name, last_read_hash)