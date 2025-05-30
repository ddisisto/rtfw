"""
State Parser v2 - Structure-aware parsing
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

from .models_v2 import AgentGroundState, GitActivity, ContextWindow, LastObservedAgentState, AgentState


class StateParserV2:
    """Parse _state.md files into structured data"""
    
    def parse_file(self, file_path: Path) -> AgentGroundState:
        """Parse a _state.md file into AgentGroundState"""
        if not file_path.exists():
            return AgentGroundState()
        
        content = file_path.read_text()
        return self.parse_content(content)
    
    def parse_content(self, content: str) -> AgentGroundState:
        """Parse _state.md content into structured format"""
        # Extract format version
        format_version = self._extract_format_version(content)
        
        # Parse into sections
        sections = self._split_into_sections(content)
        
        # Build state object
        state = AgentGroundState(format_version=format_version)
        
        # Parse each section
        if "Git Activity" in sections:
            state.git_activity = self._parse_git_activity(sections["Git Activity"])
        
        if "Context Window" in sections:
            state.context_window = self._parse_context_window(sections["Context Window"])
        
        if "Last Observed Agent State" in sections:
            state.last_observed_agent_state = self._parse_agent_state(sections["Last Observed Agent State"])
        
        return state
    
    def _extract_format_version(self, content: str) -> str:
        """Extract format version from header"""
        for line in content.split('\n'):
            if "Format Version:" in line:
                return line.split(':', 1)[1].strip()
        return "1.0"
    
    def _split_into_sections(self, content: str) -> Dict[str, str]:
        """Split content into sections by ## headers"""
        sections = {}
        current_section = None
        current_lines = []
        
        for line in content.split('\n'):
            if line.startswith("## "):
                # Save previous section
                if current_section:
                    sections[current_section] = '\n'.join(current_lines)
                
                # Start new section
                current_section = line[3:].strip()
                current_lines = []
            elif current_section:
                current_lines.append(line)
        
        # Save last section
        if current_section:
            sections[current_section] = '\n'.join(current_lines)
        
        return sections
    
    def _parse_git_activity(self, content: str) -> GitActivity:
        """Parse Git Activity section"""
        data = self._parse_key_value_section(content)
        
        return GitActivity(
            last_read_commit_hash=data.get('last_read_commit_hash'),
            last_read_commit_timestamp=self._parse_timestamp(data.get('last_read_commit_timestamp')),
            last_write_commit_hash=data.get('last_write_commit_hash'),
            last_write_commit_timestamp=self._parse_timestamp(data.get('last_write_commit_timestamp'))
        )
    
    def _parse_context_window(self, content: str) -> ContextWindow:
        """Parse Context Window section"""
        data = self._parse_key_value_section(content)
        
        # Parse percentage
        context_percent = None
        if 'context_percent' in data:
            percent_str = data['context_percent'].rstrip('%')
            try:
                context_percent = float(percent_str)
            except ValueError:
                pass
        
        return ContextWindow(
            session_id=data.get('session_id'),
            context_tokens=self._parse_int(data.get('context_tokens')),
            max_context_tokens=self._parse_int(data.get('max_context_tokens'), 128000),
            context_percent=context_percent,
            last_updated=self._parse_timestamp(data.get('last_updated'))
        )
    
    def _parse_agent_state(self, content: str) -> LastObservedAgentState:
        """Parse Last Observed Agent State section"""
        data = self._parse_key_value_section(content)
        
        # Parse state enum
        state = AgentState.OFFLINE
        if 'state' in data:
            try:
                state = AgentState(data['state'])
            except ValueError:
                pass
        
        return LastObservedAgentState(
            state=state,
            thread=data.get('thread') if data.get('thread') != '*' else None,
            started=self._parse_timestamp(data.get('started')),
            context_tokens_at_entry=self._parse_int(data.get('context_tokens_at_entry'), 0),
            expected_next_state=data.get('expected_next_state'),
            unread_message_count=self._parse_int(data.get('unread_message_count'), 0)
        )
    
    def _parse_key_value_section(self, content: str) -> Dict[str, str]:
        """Parse a section with key: value lines"""
        data = {}
        
        for line in content.strip().split('\n'):
            if ':' in line and not line.startswith('*'):
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                if value and value != '?':
                    data[key] = value
        
        return data
    
    def _parse_timestamp(self, value: Optional[str]) -> Optional[datetime]:
        """Parse timestamp string"""
        if not value or value == '?':
            return None
        
        # Try common formats
        formats = [
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        
        try:
            return datetime.fromisoformat(value)
        except:
            return None
    
    def _parse_int(self, value: Optional[str], default: int = None) -> Optional[int]:
        """Parse integer value"""
        if not value or value == '?':
            return default
        
        try:
            return int(value)
        except ValueError:
            return default