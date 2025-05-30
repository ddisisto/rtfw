"""
Simplified Session Monitor - Only tracks known agent symlinks
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import json

from .models import SessionInfo
from .jsonl_parser import JSONLParser


class SessionMonitor:
    """
    Monitors agent session symlinks in _sessions/
    
    Only tracks:
    - CRITIC_current.jsonl
    - ERA-1_current.jsonl  
    - GOV_current.jsonl
    - NEXUS_current.jsonl
    
    Throws exceptions for any unexpected conditions.
    """
    
    # Known agents and their symlink names
    AGENT_SYMLINKS = {
        'critic': 'CRITIC_current.jsonl',
        'era-1': 'ERA-1_current.jsonl',
        'gov': 'GOV_current.jsonl',
        'nexus': 'NEXUS_current.jsonl'
    }
    
    def __init__(self, sessions_dir: Path):
        self.sessions_dir = sessions_dir
        self.parser = JSONLParser()
        
        if not self.sessions_dir.exists():
            raise FileNotFoundError(f"Sessions directory not found: {sessions_dir}")
    
    def scan_sessions(self) -> Dict[str, SessionInfo]:
        """
        Read current state from agent symlinks
        
        Returns:
            Dict mapping agent_name -> SessionInfo
            
        Raises:
            FileNotFoundError: If expected symlink missing
            ValueError: If symlink points to non-existent file
            RuntimeError: If newer files detected than symlinks point to
        """
        sessions = {}
        
        # Get modification time of newest symlink target
        newest_symlink_target_mtime = 0.0
        
        for agent_name, symlink_name in self.AGENT_SYMLINKS.items():
            symlink_path = self.sessions_dir / symlink_name
            
            if not symlink_path.exists():
                raise FileNotFoundError(
                    f"Expected symlink not found: {symlink_path}\n"
                    f"Run 'ln -s <session-file> {symlink_path}' to create it"
                )
            
            if not symlink_path.is_symlink():
                raise ValueError(f"Expected symlink but found regular file: {symlink_path}")
            
            # Get the target file
            target_path = symlink_path.resolve()
            
            if not target_path.exists():
                raise ValueError(f"Symlink points to non-existent file: {symlink_path} -> {target_path}")
            
            # Track newest target modification time
            target_mtime = target_path.stat().st_mtime
            newest_symlink_target_mtime = max(newest_symlink_target_mtime, target_mtime)
            
            # Get just the last activity (optimized - reads only tail)
            last_ts, _ = self.parser.extract_last_activity(target_path)
            
            # Create SessionInfo
            info = SessionInfo(
                session_id=target_path.stem,
                file_path=str(target_path),
                last_modified=datetime.fromtimestamp(target_mtime),
                file_size=target_path.stat().st_size,
                agent_name=agent_name,  # Use our known mapping
                first_timestamp=None,  # Not needed for state monitoring
                last_timestamp=last_ts,
                line_count=0  # Not used by engine
            )
            
            sessions[agent_name] = info
        
        # Check for any JSONL files newer than our symlinks
        self._check_for_newer_files(newest_symlink_target_mtime)
        
        return sessions
    
    def _check_for_newer_files(self, newest_symlink_mtime: float):
        """
        Check if any JSONL files are newer than our symlinks and auto-update
        
        This handles cases where agents bootstrap/restart outside of logout flow.
        We'll try to match newer files to agents and update symlinks automatically.
        
        Raises:
            RuntimeError: Only if we can't determine which agent owns a newer file
        """
        # Group all JSONL files by agent based on content
        agent_sessions = {agent: [] for agent in self.AGENT_SYMLINKS.keys()}
        unmatched_files = []
        
        for file_path in self.sessions_dir.glob("*.jsonl"):
            # Skip our known symlinks
            if file_path.name in self.AGENT_SYMLINKS.values():
                continue
            
            # Try to determine which agent this session belongs to
            try:
                # Read first few lines to find agent name
                agent_name = self._detect_agent_from_session(file_path)
                if agent_name and agent_name in agent_sessions:
                    agent_sessions[agent_name].append(file_path)
                else:
                    unmatched_files.append(file_path)
            except Exception:
                # If we can't read the file, add to unmatched
                unmatched_files.append(file_path)
        
        # For each agent, check if there's a newer session than current symlink
        updates_made = False
        for agent_name, session_files in agent_sessions.items():
            if not session_files:
                continue
                
            # Find newest session for this agent
            newest_session = max(session_files, key=lambda p: p.stat().st_mtime)
            
            # Get current symlink target
            symlink_path = self.sessions_dir / self.AGENT_SYMLINKS[agent_name]
            current_target = symlink_path.resolve() if symlink_path.exists() else None
            
            # Update symlink if newer session exists
            if not current_target or newest_session.stat().st_mtime > current_target.stat().st_mtime:
                print(f"  Auto-updating {agent_name} symlink: {newest_session.name}")
                
                # Remove old symlink if exists
                if symlink_path.exists():
                    symlink_path.unlink()
                
                # Create new symlink
                symlink_path.symlink_to(newest_session.name)
                updates_made = True
        
        # Only raise error if we have unmatched files that are newer
        newer_unmatched = [f for f in unmatched_files 
                          if f.stat().st_mtime > newest_symlink_mtime]
        
        if newer_unmatched and not updates_made:
            raise RuntimeError(
                f"Found {len(newer_unmatched)} newer JSONL files that couldn't be matched to agents:\n"
                + "\n".join(f"  - {f.name}" for f in newer_unmatched[:5])
                + ("\n  ..." if len(newer_unmatched) > 5 else "")
                + "\n\nThese may be from unknown agents or corrupted sessions."
            )
    
    def _detect_agent_from_session(self, file_path: Path) -> Optional[str]:
        """
        Try to detect which agent owns a session file by reading content
        
        Returns:
            agent name (lowercase) or None if can't determine
        """
        try:
            # Read first 50 lines or 10KB, whichever comes first
            lines_read = 0
            bytes_read = 0
            max_lines = 50
            max_bytes = 10240
            
            with open(file_path, 'r') as f:
                while lines_read < max_lines and bytes_read < max_bytes:
                    line = f.readline()
                    if not line:
                        break
                    
                    lines_read += 1
                    bytes_read += len(line.encode())
                    
                    # Try to parse as JSON and look for assistant messages
                    try:
                        data = json.loads(line)
                        
                        # Check if this is an assistant message
                        if data.get('message', {}).get('role') == 'assistant':
                            # Get the content - could be in different formats
                            content = ''
                            msg_content = data.get('message', {}).get('content', [])
                            
                            if isinstance(msg_content, str):
                                content = msg_content
                            elif isinstance(msg_content, list):
                                # Extract text content from list format
                                for item in msg_content:
                                    if isinstance(item, dict) and item.get('type') == 'text':
                                        content += item.get('text', '')
                            
                            # Check for our known agents in the content
                            for agent_lower, agent_upper in [
                                ('critic', 'CRITIC'),
                                ('era-1', 'ERA-1'),
                                ('gov', 'GOV'),
                                ('nexus', 'NEXUS')
                            ]:
                                # Check various patterns
                                if any(pattern in content for pattern in [
                                    f'@{agent_upper}',
                                    f'I am {agent_upper}',
                                    f"I'm {agent_upper}",
                                    f'{agent_upper}.md',
                                    f'agent/{agent_lower}/',
                                    f'bootstrap protocol for @{agent_upper}',
                                ]):
                                    return agent_lower
                    except:
                        # If JSON parsing fails, continue to next line
                        pass
            
            return None
            
        except Exception:
            return None