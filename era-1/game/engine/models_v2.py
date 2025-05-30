"""
Data models v2 - Structure mirrors _state.md template exactly
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum


class AgentState(Enum):
    """Agent lifecycle states per protocol"""
    OFFLINE = "offline"
    BOOTSTRAP = "bootstrap"
    INBOX = "inbox"
    DISTILL = "distill"
    DEEP_WORK = "deep_work"
    IDLE = "idle"
    LOGOUT = "logout"
    DIRECT_IO = "direct_io"


@dataclass
class GitActivity:
    """## Git Activity section"""
    last_read_commit_hash: Optional[str] = None
    last_read_commit_timestamp: Optional[datetime] = None
    last_write_commit_hash: Optional[str] = None
    last_write_commit_timestamp: Optional[datetime] = None


@dataclass
class ContextWindow:
    """## Context Window section"""
    session_id: Optional[str] = None
    context_tokens: Optional[int] = None
    max_context_tokens: int = 128000
    context_percent: Optional[float] = None
    last_updated: Optional[datetime] = None


@dataclass
class LastObservedAgentState:
    """## Last Observed Agent State section"""
    state: AgentState = AgentState.OFFLINE
    thread: Optional[str] = None
    started: Optional[datetime] = None
    context_tokens_at_entry: int = 0
    expected_next_state: Optional[str] = None  # String for "bootstrap -> inbox" format
    unread_message_count: int = 0


@dataclass
class AgentGroundState:
    """
    Complete agent state - structure matches _state.md sections
    Each field is a section that can be serialized independently
    """
    format_version: str = "1.0"
    agent_name: str = ""  # Not in file, but needed for generation
    
    # Sections matching _state.md structure
    git_activity: GitActivity = field(default_factory=GitActivity)
    context_window: ContextWindow = field(default_factory=ContextWindow)
    last_observed_agent_state: LastObservedAgentState = field(default_factory=LastObservedAgentState)
    
    def to_state_file_content(self) -> str:
        """Serialize to _state.md format"""
        return STATE_TEMPLATE.format(
            agent_name=self.agent_name.upper(),
            format_version=self.format_version,
            git_activity=self._format_section(self.git_activity),
            context_window=self._format_section(self.context_window),
            last_observed_agent_state=self._format_section(self.last_observed_agent_state)
        )
    
    def _format_section(self, section) -> str:
        """Format a dataclass section as key: value lines"""
        lines = []
        for key, value in asdict(section).items():
            formatted_key = key
            formatted_value = self._format_value(value)
            lines.append(f"{formatted_key}: {formatted_value}")
        return '\n'.join(lines)
    
    def _format_value(self, value) -> str:
        """Format individual values"""
        if value is None:
            return "?"
        elif isinstance(value, datetime):
            return value.strftime("%Y-%m-%dT%H:%M:%S%z")
        elif isinstance(value, AgentState):
            return value.value
        elif isinstance(value, str) and len(value) > 7 and value.replace('-', '').isalnum():
            # Truncate commit hashes
            return value[:7]
        elif isinstance(value, float):
            return f"{value:.1f}%"
        else:
            return str(value)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentGroundState':
        """Create from parsed dictionary with version handling"""
        version = data.get('format_version', '1.0')
        
        if version == '1.0':
            return cls._from_v1_dict(data)
        else:
            # Future versions
            raise ValueError(f"Unknown format version: {version}")
    
    @classmethod
    def _from_v1_dict(cls, data: Dict[str, Any]) -> 'AgentGroundState':
        """Parse v1.0 format"""
        state = cls()
        
        # Parse git activity
        if 'git_activity' in data:
            state.git_activity = GitActivity(**data['git_activity'])
        
        # Parse context window
        if 'context_window' in data:
            state.context_window = ContextWindow(**data['context_window'])
        
        # Parse agent state
        if 'last_observed_agent_state' in data:
            agent_data = data['last_observed_agent_state']
            # Convert state string to enum
            if 'state' in agent_data and isinstance(agent_data['state'], str):
                agent_data['state'] = AgentState(agent_data['state'])
            state.last_observed_agent_state = LastObservedAgentState(**agent_data)
        
        return state


# Template exactly matches _state.md format
STATE_TEMPLATE = """# {agent_name} Ground State [READ-ONLY]
# CRITICAL: This file is maintained by the game engine
# DO NOT EDIT - Read for objective truth only
# COMMIT this file with your workspace
# Format Version: {format_version}
*NOTE: additional agent managed state tracking recommended within scratch.md and for alignment and validation*
*NOTE: state tracking system almost complete, **SOME** values may still be placeholders and functionality may change*

## Git Activity
{git_activity}

## Context Window
{context_window}

## Last Observed Agent State
{last_observed_agent_state}
"""


class StateVersionMigrator:
    """Handle migrations between state format versions"""
    
    @staticmethod
    def migrate(data: Dict[str, Any], from_version: str, to_version: str) -> Dict[str, Any]:
        """Migrate state data between versions"""
        if from_version == to_version:
            return data
        
        # Future: implement migration paths
        # Example: 1.0 -> 2.0 might add new fields with defaults
        
        raise NotImplementedError(f"Migration from {from_version} to {to_version} not implemented")