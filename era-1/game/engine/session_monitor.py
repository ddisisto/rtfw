"""
Simplified Session Monitor - Only tracks known agent symlinks
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

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
        Check if any JSONL files are newer than our symlinks
        
        Raises:
            RuntimeError: If newer files detected
        """
        newer_files = []
        
        for file_path in self.sessions_dir.glob("*.jsonl"):
            # Skip our known symlinks
            if file_path.name in self.AGENT_SYMLINKS.values():
                continue
                
            # Check if this file is newer
            if file_path.stat().st_mtime > newest_symlink_mtime:
                newer_files.append(file_path.name)
        
        if newer_files:
            raise RuntimeError(
                f"Found {len(newer_files)} JSONL files newer than current symlinks:\n"
                + "\n".join(f"  - {f}" for f in newer_files[:5])
                + ("\n  ..." if len(newer_files) > 5 else "")
                + "\n\nThis likely means new sessions have started. "
                + "Please update symlinks or handle new session discovery."
            )