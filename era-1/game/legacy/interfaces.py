"""
Core interfaces for ERA-1 Foundation Terminal

These interfaces define contracts between components while maintaining
1970s aesthetic externally with modern patterns internally.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from enum import Enum


class AgentStatus(Enum):
    """Agent operational states"""
    ACTIVE = "ACTIVE"     # Currently in window with * flag
    SILENT = "SILENT"     # In window with - flag
    IDLE = "IDLE"        # Has window but no activity
    OFFLINE = "OFFLINE"   # No tmux window found


@dataclass
class Agent:
    """Agent state representation"""
    name: str
    status: AgentStatus
    context_size: int  # Lines in context.md
    context_percent: int  # Rough capacity estimate
    last_activity: str  # "5 minutes ago" format
    current_task: Optional[str] = None
    session_id: Optional[str] = None


@dataclass
class Message:
    """Git commit message representation"""
    hash: str
    author: str
    content: str
    timestamp: datetime
    mentions: List[str]  # Extracted @mentions


class AgentMonitor(ABC):
    """Interface for safe read-only agent data access"""
    
    @abstractmethod
    def get_all_agents(self) -> List[str]:
        """List all known agents from tmux windows and git history"""
        pass
    
    @abstractmethod
    def get_agent_status(self, agent_name: str) -> Agent:
        """Get complete status for a single agent"""
        pass
    
    @abstractmethod
    def get_context_size(self, agent_name: str) -> Tuple[int, int]:
        """Return (lines, percent_full) for agent's context.md"""
        pass
    
    @abstractmethod
    def get_last_activity(self, agent_name: str) -> str:
        """Get human-readable time since last commit"""
        pass
    
    @abstractmethod
    def get_current_task(self, agent_name: str) -> Optional[str]:
        """Extract current task from scratch.md if available"""
        pass


class MessageBus(ABC):
    """Interface for git-based messaging"""
    
    @abstractmethod
    def send_message(self, from_agent: str, to_agent: str, content: str) -> str:
        """Send message via git commit, return commit hash"""
        pass
    
    @abstractmethod
    def get_recent_messages(self, count: int = 20) -> List[Message]:
        """Get recent messages from git log"""
        pass
    
    @abstractmethod
    def get_messages_for_agent(self, agent_name: str, count: int = 10) -> List[Message]:
        """Get messages mentioning specific agent"""
        pass


class DisplayManager(ABC):
    """Interface for terminal display operations"""
    
    @abstractmethod
    def initialize(self) -> None:
        """Set up terminal for 1970s aesthetic"""
        pass
    
    @abstractmethod
    def show_header(self) -> None:
        """Display retro system header"""
        pass
    
    @abstractmethod
    def show_status_panel(self, agents: List[Agent]) -> None:
        """Update agent status display"""
        pass
    
    @abstractmethod
    def show_message_log(self, messages: List[Message]) -> None:
        """Display recent system messages"""
        pass
    
    @abstractmethod
    def show_command_output(self, output: str) -> None:
        """Display command execution results"""
        pass
    
    @abstractmethod
    def get_input(self, prompt: str = "> ") -> str:
        """Get user input with retro prompt"""
        pass
    
    @abstractmethod
    def handle_resize(self) -> None:
        """Handle terminal resize events"""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Restore terminal to normal state"""
        pass


class TmuxManager(ABC):
    """Interface for optional tmux pane embedding"""
    
    @abstractmethod
    def create_embedded_pane(self, size_percent: int = 30) -> bool:
        """Create pane for agent viewing, return success"""
        pass
    
    @abstractmethod
    def switch_to_agent(self, agent_name: str) -> bool:
        """Switch embedded pane to show specific agent"""
        pass
    
    @abstractmethod
    def toggle_zoom(self) -> None:
        """Toggle fullscreen on embedded pane"""
        pass
    
    @abstractmethod
    def close_embedded_pane(self) -> None:
        """Remove embedded pane, restore layout"""
        pass
    
    @abstractmethod
    def get_available_agents(self) -> List[str]:
        """List agents that can be viewed"""
        pass


@dataclass
class Command:
    """Parsed command representation"""
    name: str
    args: List[str]
    raw: str


class CommandParser(ABC):
    """Interface for 1970s-style command parsing"""
    
    @abstractmethod
    def parse(self, input_line: str) -> Optional[Command]:
        """Parse user input into command structure"""
        pass
    
    @abstractmethod
    def get_commands(self) -> List[str]:
        """List available commands"""
        pass
    
    @abstractmethod
    def get_help(self, command: Optional[str] = None) -> str:
        """Get help text in period-appropriate style"""
        pass


class CommandHandler(ABC):
    """Base class for command implementations"""
    
    @abstractmethod
    def execute(self, command: Command) -> str:
        """Execute command and return output"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Get one-line description for help"""
        pass