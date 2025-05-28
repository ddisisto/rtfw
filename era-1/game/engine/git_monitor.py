"""
Git Monitor - Tracks agent git activity and messages
"""

import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple, List


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