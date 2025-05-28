"""
Data models for state engine

TODO: Consider versioning strategy for _state.md files
      - Version field in AgentGroundState?
      - Migration support for format changes?
      - Backward compatibility requirements?
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
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
    DIRECT_IO = "direct_io"  # Admin override - skip idle checks


@dataclass
class SessionInfo:
    """Information about a JSONL session file"""
    session_id: str
    file_path: str
    last_modified: datetime
    file_size: int
    first_timestamp: Optional[datetime] = None
    last_timestamp: Optional[datetime] = None
    line_count: int = 0
    agent_name: Optional[str] = None  # Extracted from content
    is_continuation: bool = False
    
    @property
    def is_stale(self) -> bool:
        """Check if file hasn't been written to in 60+ seconds"""
        if not self.last_modified:
            return False
        age = datetime.now() - self.last_modified
        return age.total_seconds() > 60


@dataclass
class StateDecision:
    """Parsed state decision from agent message"""
    next_state: AgentState
    thread: Optional[str] = None
    max_tokens: Optional[int] = None
    last_read_commit: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    line_number: Optional[int] = None
    expected_next_state: Optional[AgentState] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict for JSON serialization"""
        return {
            'next_state': self.next_state.value,
            'thread': self.thread,
            'max_tokens': self.max_tokens,
            'last_read_commit': self.last_read_commit,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class AgentGroundState:
    """
    Represents the content of an agent's _state.md file
    Maps to the READ-ONLY ground truth maintained by engine
    """
    # Git Activity
    last_read_commit_hash: Optional[str] = None
    last_read_commit_timestamp: Optional[datetime] = None
    last_write_commit_hash: Optional[str] = None
    last_write_commit_timestamp: Optional[datetime] = None
    
    # Context Window
    session_id: Optional[str] = None
    context_tokens: Optional[int] = None
    max_context_tokens: int = 128000  # New field matching your format
    context_percent: Optional[float] = None
    last_updated: Optional[datetime] = None
    
    # Last Observed Agent State
    state: AgentState = AgentState.OFFLINE
    thread: Optional[str] = None
    started: Optional[datetime] = None
    expected_next_state: Optional[AgentState] = None
    context_tokens_at_entry: int = 0  # Snapshot when entering state
    state_last_updated: Optional[datetime] = None  # New field
    unread_message_count: int = 0  # New field for inbox management
    
    def to_state_file_content(self, agent_name: str) -> str:
        """Generate _state.md file content"""
        # Format timestamps consistently
        def fmt_time(dt: Optional[datetime]) -> str:
            if not dt:
                return "?"
            return dt.strftime("%Y-%m-%dT%H:%M:%S%z")
        
        # Calculate expected next state based on current
        next_states = {
            AgentState.OFFLINE: AgentState.BOOTSTRAP,
            AgentState.BOOTSTRAP: AgentState.INBOX,
            AgentState.INBOX: AgentState.DISTILL,
            AgentState.DISTILL: AgentState.DEEP_WORK,  # or IDLE or LOGOUT
            AgentState.DEEP_WORK: AgentState.INBOX,
            AgentState.IDLE: AgentState.INBOX,
            AgentState.LOGOUT: AgentState.OFFLINE,
        }
        
        expected_next = next_states.get(self.state, AgentState.INBOX)
        
        # Format expected_next_state as transition
        if self.state == AgentState.LOGOUT:
            next_state_str = "bootstrap -> inbox"
        elif self.state == AgentState.OFFLINE:
            next_state_str = "bootstrap -> inbox"
        else:
            next_state_str = expected_next.value
        
        return f"""# {agent_name.upper()} Ground State [READ-ONLY]
# CRITICAL: This file is maintained by the game engine
# DO NOT EDIT - Read for objective truth only
# COMMIT this file with your workspace
*NOTE: additional agent managed state tracking recommended within scratch.md and for alignment and validation*
*NOTE: state tracking system almost complete, **SOME** values may still be placeholders and functionality may change*

## Git Activity
last_read_commit_hash: {self.last_read_commit_hash or '?'}
last_read_commit_timestamp: {fmt_time(self.last_read_commit_timestamp)}
last_write_commit_hash: {self.last_write_commit_hash or '?'}
last_write_commit_timestamp: {fmt_time(self.last_write_commit_timestamp)}

## Context Window
session_id: {self.session_id or '?'}
context_tokens: {self.context_tokens or '?'}
max_context_tokens: {self.max_context_tokens}
context_percent: {f"{self.context_percent:.1f}%" if self.context_percent else '?'}
last_updated: {fmt_time(self.last_updated)}

## Last Observed Agent State
state: {self.state.value}
thread: {self.thread or '*'}
started: {fmt_time(self.started)}
context_tokens_at_entry: {self.context_tokens_at_entry}
expected_next_state: {next_state_str}
unread_message_count: {self.unread_message_count}
"""


@dataclass
class EngineState:
    """Internal state tracking for the engine"""
    seen_sessions: Dict[str, datetime] = field(default_factory=dict)  # session_id -> last_seen
    agent_sessions: Dict[str, str] = field(default_factory=dict)  # agent_name -> session_id  
    agent_states: Dict[str, AgentGroundState] = field(default_factory=dict)  # agent_name -> state
    last_poll: Optional[datetime] = None
    errors: list = field(default_factory=list)