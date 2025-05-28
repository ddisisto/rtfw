"""
Session Monitor - Discovers and tracks agent sessions in _sessions/
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from .models import SessionInfo, EngineState
from .jsonl_parser import JSONLParser


class SessionMonitor:
    """
    Monitors _sessions/ directory for agent session files
    
    Responsibilities:
    - Discover new session files
    - Map sessions to agents
    - Track session staleness
    - Manage agent-current.jsonl symlinks
    """
    
    def __init__(self, sessions_dir: Path):
        self.sessions_dir = sessions_dir
        self.parser = JSONLParser()
        self.state = EngineState()
        
        # Ensure sessions directory exists
        self.sessions_dir.mkdir(exist_ok=True)
    
    def scan_sessions(self) -> List[SessionInfo]:
        """
        Scan _sessions/ directory and return all session info
        
        Returns:
            List of SessionInfo objects for all JSONL files
        """
        sessions = []
        
        for file_path in self.sessions_dir.glob("*.jsonl"):
            # Skip symlinks
            if file_path.is_symlink():
                continue
            
            # Get file stats
            stat = file_path.stat()
            session_id = file_path.stem
            
            # Create SessionInfo
            info = SessionInfo(
                session_id=session_id,
                file_path=str(file_path),
                last_modified=datetime.fromtimestamp(stat.st_mtime),
                file_size=stat.st_size
            )
            
            # Quick check if this is a new file
            if session_id not in self.state.seen_sessions:
                # New file - need to parse to determine if new agent or continuation
                parsed = self.parser.parse_session_file(file_path)
                info.agent_name = parsed.get('agent_name')
                info.first_timestamp = parsed.get('first_timestamp')
                info.last_timestamp = parsed.get('last_timestamp')
                info.line_count = parsed.get('line_count', 0)
                
                # Heuristic for continuation vs new session
                # TODO: Validate these thresholds based on actual usage patterns
                if info.file_size > 10000 and info.line_count > 50:
                    info.is_continuation = True
                elif info.first_timestamp and info.last_modified:
                    # If first message is much older than file creation, likely continuation
                    age_diff = info.last_modified - info.first_timestamp
                    if age_diff.total_seconds() > 3600:  # 1 hour
                        info.is_continuation = True
            else:
                # Seen before - just update timestamps
                info.agent_name = self._get_agent_for_session(session_id)
                last_ts, _ = self.parser.extract_last_activity(file_path)
                info.last_timestamp = last_ts
            
            sessions.append(info)
            self.state.seen_sessions[session_id] = datetime.now()
        
        return sessions
    
    def map_agents_to_sessions(self, sessions: List[SessionInfo]) -> Dict[str, str]:
        """
        Determine current active session for each agent
        
        Rules:
        - Most recent activity wins
        - Only consider non-stale sessions
        - Handle multiple sessions per agent gracefully
        
        Returns:
            Dict of agent_name -> session_id
        """
        # Group sessions by agent
        agent_sessions: Dict[str, List[SessionInfo]] = {}
        
        for session in sessions:
            if session.agent_name and not session.is_stale:
                if session.agent_name not in agent_sessions:
                    agent_sessions[session.agent_name] = []
                agent_sessions[session.agent_name].append(session)
        
        # Pick most recent for each agent
        current_mapping = {}
        
        for agent_name, agent_session_list in agent_sessions.items():
            # Sort by last activity (most recent first)
            agent_session_list.sort(
                key=lambda s: s.last_timestamp or s.last_modified,
                reverse=True
            )
            
            # Take the most recent
            current_session = agent_session_list[0]
            current_mapping[agent_name] = current_session.session_id
            
            # Log if multiple active sessions detected
            if len(agent_session_list) > 1:
                # TODO: Handle this edge case - possibly needs manual intervention
                other_sessions = [s.session_id for s in agent_session_list[1:]]
                print(f"WARNING: Multiple active sessions for {agent_name}: "
                      f"using {current_session.session_id}, ignoring {other_sessions}")
        
        # Update internal state
        self.state.agent_sessions = current_mapping
        
        return current_mapping
    
    def update_symlinks(self, agent_mapping: Dict[str, str]) -> None:
        """
        Update agent-current.jsonl symlinks based on current mapping
        
        Args:
            agent_mapping: Dict of agent_name -> session_id
        """
        # Remove all existing agent symlinks
        for symlink in self.sessions_dir.glob("*-current.jsonl"):
            if symlink.is_symlink():
                symlink.unlink()
        
        # Create new symlinks
        for agent_name, session_id in agent_mapping.items():
            source = self.sessions_dir / f"{session_id}.jsonl"
            target = self.sessions_dir / f"{agent_name}-current.jsonl"
            
            if source.exists():
                # Create relative symlink
                target.symlink_to(source.name)
    
    def get_stale_sessions(self, sessions: List[SessionInfo]) -> List[SessionInfo]:
        """
        Get sessions that haven't been updated in 60+ seconds
        
        These are candidates for state transition checks
        """
        return [s for s in sessions if s.is_stale and s.agent_name]
    
    def _get_agent_for_session(self, session_id: str) -> Optional[str]:
        """Get agent name for a known session ID"""
        for agent, sid in self.state.agent_sessions.items():
            if sid == session_id:
                return agent
        return None
    
    def find_orphaned_sessions(self, sessions: List[SessionInfo]) -> List[SessionInfo]:
        """
        Find sessions with no identifiable agent
        
        These might need manual review or special handling
        """
        orphaned = []
        
        for session in sessions:
            if not session.agent_name:
                # Try parsing again in case we missed it
                parsed = self.parser.parse_session_file(Path(session.file_path))
                if not parsed.get('agent_name'):
                    orphaned.append(session)
                else:
                    # Update with found name
                    session.agent_name = parsed['agent_name']
        
        return orphaned
    
    def write_current_sessions_json(self, mapping: Dict[str, str]) -> None:
        """
        Write current session mapping to current_sessions.json
        
        This maintains compatibility with existing code that expects this file
        """
        output_path = self.sessions_dir / "current_sessions.json"
        
        with open(output_path, 'w') as f:
            json.dump(mapping, f, indent=2)
            f.write('\n')  # Trailing newline