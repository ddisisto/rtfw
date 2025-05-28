#!/usr/bin/env python3
"""
Core Game Architecture Interfaces

Design Principles:
1. Clean separation between data sources and UI
2. Pluggable components for ERA-2+ extensions  
3. Observable state changes for reactive UIs
4. Async-ready for future enhancements
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# Core Domain Models

class AgentState(Enum):
    """Agent lifecycle states per protocol"""
    BOOTSTRAP = "bootstrap"
    INBOX = "inbox"
    DISTILL = "distill"
    DEEP_WORK = "deep_work"
    IDLE = "idle"
    LOGOUT = "logout"
    DIRECT_IO = "direct_io"  # Admin override

@dataclass
class AgentStatus:
    """Complete agent status snapshot"""
    name: str
    state: AgentState
    thread: Optional[str]
    session_id: str
    context_tokens: int
    context_percent: float
    last_write_commit: str
    last_write_time: datetime
    last_read_commit: str
    last_read_time: datetime
    unread_messages: int
    context_lines: int
    
    @property
    def is_active(self) -> bool:
        return self.state in [AgentState.DEEP_WORK, AgentState.INBOX, AgentState.DISTILL]
    
    @property
    def needs_attention(self) -> bool:
        return self.context_percent > 85 or self.unread_messages > 10

# Core Interfaces

class StateObserver(ABC):
    """Observer pattern for state changes"""
    
    @abstractmethod
    def on_agent_state_changed(self, agent_name: str, old_state: AgentState, new_state: AgentState):
        """Called when agent transitions states"""
        pass
    
    @abstractmethod
    def on_context_threshold(self, agent_name: str, percent: float):
        """Called when context usage crosses thresholds"""
        pass

class StateProvider(ABC):
    """Interface for accessing system state"""
    
    @abstractmethod
    def get_agent_status(self, agent_name: str) -> Optional[AgentStatus]:
        """Get current status for specific agent"""
        pass
    
    @abstractmethod
    def get_all_agents(self) -> List[AgentStatus]:
        """Get status for all agents"""
        pass
    
    @abstractmethod
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get aggregate system metrics"""
        pass
    
    @abstractmethod
    def subscribe(self, observer: StateObserver):
        """Subscribe to state changes"""
        pass

class MessageProvider(ABC):
    """Interface for message operations"""
    
    @abstractmethod
    def send_message(self, from_agent: str, to_agent: str, content: str) -> str:
        """Send message via git commit, return commit hash"""
        pass
    
    @abstractmethod
    def get_messages_since(self, commit_hash: str, for_agent: Optional[str] = None) -> List[Dict]:
        """Get messages after given commit"""
        pass
    
    @abstractmethod
    def inject_to_inbox(self, agent_name: str, message: str):
        """Admin injection to agent inbox"""
        pass

class SessionManager(ABC):
    """Interface for session management"""
    
    @abstractmethod
    def get_session_id(self, agent_name: str) -> Optional[str]:
        """Get current session ID for agent"""
        pass
    
    @abstractmethod
    def update_session(self, agent_name: str, session_id: str):
        """Update session mapping"""
        pass
    
    @abstractmethod
    def get_session_metrics(self, session_id: str) -> Dict[str, Any]:
        """Get metrics from session JSONL"""
        pass

class StateManager(ABC):
    """Interface for managing agent state transitions"""
    
    @abstractmethod
    def transition_state(self, agent_name: str, new_state: AgentState, 
                        thread: Optional[str] = None, max_tokens: Optional[int] = None):
        """Execute state transition with validation"""
        pass
    
    @abstractmethod
    def update_checkpoint(self, agent_name: str, commit_hash: str):
        """Update agent's last read checkpoint"""
        pass
    
    @abstractmethod
    def force_logout(self, agent_name: str, reason: str):
        """Force agent to logout state"""
        pass

# UI Layer Interfaces

class UIAdapter(ABC):
    """Base interface for different UI paradigms"""
    
    @abstractmethod
    def render(self, state: Dict[str, Any]):
        """Render current state in UI-specific way"""
        pass
    
    @abstractmethod
    def handle_input(self, input_data: Any) -> Optional[Dict]:
        """Process UI-specific input, return command if any"""
        pass

class TerminalUI(UIAdapter):
    """ERA-1 terminal interface"""
    pass

class WebUI(UIAdapter):
    """ERA-2 web interface (future)"""
    pass

class NeuralUI(UIAdapter):
    """ERA-3 neural interface (future)"""
    pass

# Command Pattern for User Actions

@dataclass
class Command:
    """User command representation"""
    name: str
    args: List[str]
    source: str  # Which UI/agent initiated
    timestamp: datetime = None
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now()

class CommandHandler(ABC):
    """Base command handler"""
    
    @abstractmethod
    def can_handle(self, command: Command) -> bool:
        """Check if this handler can process the command"""
        pass
    
    @abstractmethod
    def execute(self, command: Command, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute command and return result"""
        pass

# Main Game Engine Interface

class GameEngine:
    """
    Central game engine coordinating all components.
    This is what ERA-1 implements and ERA-2+ extends.
    """
    
    def __init__(self,
                 state_provider: StateProvider,
                 message_provider: MessageProvider,
                 session_manager: SessionManager,
                 state_manager: StateManager):
        self.state = state_provider
        self.messages = message_provider
        self.sessions = session_manager
        self.state_mgr = state_manager
        self.uis: List[UIAdapter] = []
        self.handlers: List[CommandHandler] = []
        self.running = False
    
    def register_ui(self, ui: UIAdapter):
        """Add UI adapter (multiple UIs can coexist)"""
        self.uis.append(ui)
    
    def register_handler(self, handler: CommandHandler):
        """Add command handler"""
        self.handlers.append(handler)
    
    def start(self):
        """Start game engine"""
        self.running = True
        # Main game loop would go here
        # For now, just a placeholder
    
    def stop(self):
        """Stop game engine"""
        self.running = False
    
    def process_command(self, command: Command) -> Dict[str, Any]:
        """Route command to appropriate handler"""
        for handler in self.handlers:
            if handler.can_handle(command):
                context = {
                    'state': self.state,
                    'messages': self.messages,
                    'sessions': self.sessions,
                    'state_mgr': self.state_mgr
                }
                return handler.execute(command, context)
        
        return {'error': f'No handler for command: {command.name}'}

# Integration with Agent Lifecycle

class LifecycleMonitor(StateObserver):
    """
    Monitors agent lifecycle transitions and updates game state.
    This is the bridge between agent conversations and game state.
    """
    
    def __init__(self, state_manager: StateManager, parser):
        self.state_mgr = state_manager
        self.parser = parser  # StateParser from earlier
    
    def process_conversation_end(self, agent_name: str, final_message: str):
        """
        Called when agent conversation ends.
        Parses final message and updates state accordingly.
        """
        decision = self.parser.parse_conversation_end(final_message)
        if decision:
            # Map to AgentState enum
            state_map = {
                'deep_work': AgentState.DEEP_WORK,
                'idle': AgentState.IDLE,
                'logout': AgentState.LOGOUT,
                'inbox': AgentState.INBOX,
                'distill': AgentState.DISTILL
            }
            
            new_state = state_map.get(decision.next_state)
            if new_state:
                self.state_mgr.transition_state(
                    agent_name, 
                    new_state,
                    thread=decision.thread,
                    max_tokens=decision.max_tokens
                )
            
            if decision.last_read_commit:
                self.state_mgr.update_checkpoint(agent_name, decision.last_read_commit)
    
    def on_agent_state_changed(self, agent_name: str, old_state: AgentState, new_state: AgentState):
        """React to state changes"""
        print(f"{agent_name}: {old_state.value} -> {new_state.value}")
    
    def on_context_threshold(self, agent_name: str, percent: float):
        """React to context thresholds"""
        if percent > 90:
            print(f"WARNING: {agent_name} at {percent}% context usage!")


"""
This architecture provides:

1. Clean separation of concerns
2. Multiple UI support (ERA-1 terminal, ERA-2 web, etc)
3. Observable state for reactive updates
4. Extensible command handling
5. Integration with agent lifecycle protocol

ERA-2 can build a completely different UI on top of the same
interfaces without touching the core game logic.
"""