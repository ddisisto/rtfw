"""
State Writer - Atomically updates agent _state.md files
"""

import os
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Optional

from .models import AgentGroundState


class StateWriter:
    """
    Handles atomic writes to agent _state.md files
    
    Ensures:
    - Atomic updates (no partial writes)
    - Consistent formatting
    - Backup on error
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
    
    def write_agent_state(self, agent_name: str, state: AgentGroundState) -> bool:
        """
        Atomically write agent state to _state.md file
        
        Args:
            agent_name: Name of agent (e.g., 'era-1', 'gov')
            state: Ground state to write
            
        Returns:
            True if successful, False on error
        """
        # Determine file path
        state_file = self.project_root / agent_name / "_state.md"
        
        # Ensure directory exists
        state_file.parent.mkdir(exist_ok=True)
        
        # Generate content
        content = state.to_state_file_content(agent_name)
        
        try:
            # Write atomically using temp file + rename
            with tempfile.NamedTemporaryFile(
                mode='w',
                dir=state_file.parent,
                prefix=f".{state_file.name}.",
                suffix='.tmp',
                delete=False
            ) as tmp:
                tmp.write(content)
                tmp_path = tmp.name
            
            # Atomic rename
            os.replace(tmp_path, state_file)
            
            return True
            
        except Exception as e:
            # Clean up temp file if it exists
            if 'tmp_path' in locals() and os.path.exists(tmp_path):
                os.unlink(tmp_path)
            
            # Log error (in production, would use proper logging)
            print(f"ERROR writing state for {agent_name}: {e}")
            
            # Create backup of current file if it exists
            if state_file.exists():
                backup_path = state_file.with_suffix('.md.backup')
                try:
                    state_file.rename(backup_path)
                except:
                    pass
            
            return False
    
    def read_agent_state(self, agent_name: str) -> Optional[AgentGroundState]:
        """
        Read current agent state from _state.md file
        
        Args:
            agent_name: Name of agent
            
        Returns:
            AgentGroundState or None if file doesn't exist
        """
        state_file = self.project_root / agent_name / "_state.md"
        
        if not state_file.exists():
            return None
        
        try:
            content = state_file.read_text()
            return self._parse_state_file(content)
        except Exception as e:
            print(f"ERROR reading state for {agent_name}: {e}")
            return None
    
    def _parse_state_file(self, content: str) -> AgentGroundState:
        """
        Parse _state.md file content into AgentGroundState
        
        This is somewhat fragile but matches the expected format
        """
        state = AgentGroundState()
        
        # Check for format version (default to 1.0 if not found)
        format_version = "1.0"
        for line in content.split('\n'):
            if line.startswith('# Format Version:'):
                format_version = line.split(':')[1].strip()
                break
        
        # Parse line by line looking for key: value pairs
        for line in content.split('\n'):
            line = line.strip()
            
            if ':' not in line:
                continue
            
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # Skip placeholder values
            if value == '?':
                continue
            
            # Parse based on key
            try:
                if key == 'last_read_commit_hash':
                    state.last_read_commit_hash = value
                elif key == 'last_read_commit_timestamp':
                    state.last_read_commit_timestamp = self._parse_timestamp(value)
                elif key == 'last_write_commit_hash':
                    state.last_write_commit_hash = value
                elif key == 'last_write_commit_timestamp':
                    state.last_write_commit_timestamp = self._parse_timestamp(value)
                elif key == 'session_id':
                    state.session_id = value
                elif key == 'context_tokens':
                    state.context_tokens = int(value) if value.isdigit() else None
                elif key == 'context_percent':
                    # Remove % sign and parse
                    percent_str = value.rstrip('%')
                    state.context_percent = float(percent_str) if percent_str else None
                elif key == 'max_context_tokens':
                    state.max_context_tokens = int(value) if value.isdigit() else 128000
                elif key == 'last_updated':
                    state.last_updated = self._parse_timestamp(value)
                elif key == 'state':
                    # Map string to enum
                    from .models import AgentState
                    state_map = {s.value: s for s in AgentState}
                    state.state = state_map.get(value, AgentState.OFFLINE)
                elif key == 'thread':
                    state.thread = value if value != '*' else None
                elif key == 'started':
                    state.started = self._parse_timestamp(value)
                elif key == 'expected_next_state':
                    from .models import AgentState
                    state_map = {s.value: s for s in AgentState}
                    state.expected_next_state = state_map.get(value)
                elif key == 'state_tokens':
                    state.state_tokens = int(value) if value.isdigit() else 0
                elif key == 'max_tokens':
                    state.max_tokens = int(value) if value.isdigit() else 100000
                elif key == 'unread_message_count':
                    state.unread_message_count = int(value) if value.isdigit() else 0
            except (ValueError, AttributeError):
                # Skip malformed values
                continue
        
        return state
    
    def _parse_timestamp(self, value: str) -> Optional[datetime]:
        """Parse timestamp string into datetime"""
        if not value or value == '?':
            return None
        
        # Try common formats
        formats = [
            "%Y-%m-%dT%H:%M:%S%z",  # ISO with timezone
            "%Y-%m-%dT%H:%M:%S",    # ISO without timezone
            "%Y-%m-%d %H:%M:%S",    # Simple format
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        
        # If no format worked, try fromisoformat as last resort
        try:
            return datetime.fromisoformat(value)
        except:
            return None
    
    def ensure_state_files_exist(self, agent_names: list) -> None:
        """
        Ensure all agents have _state.md files
        
        Creates default offline state for any missing files
        """
        for agent_name in agent_names:
            state_file = self.project_root / agent_name / "_state.md"
            
            if not state_file.exists():
                # Create default offline state
                default_state = AgentGroundState()
                self.write_agent_state(agent_name, default_state)