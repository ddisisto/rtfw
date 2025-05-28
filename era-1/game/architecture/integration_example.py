#!/usr/bin/env python3
"""
Integration Example - Connecting Architecture to Existing Game

Shows how the new architecture integrates with current cli.py
and provides a migration path.
"""

from pathlib import Path
import subprocess
import json
from datetime import datetime

from core_interfaces import (
    StateProvider, AgentStatus, AgentState,
    MessageProvider, SessionManager, StateManager,
    CommandHandler, Command
)
from state_parser import StateParser
from lifecycle_commands import StateCommand, TokensCommand, ThreadsCommand

# Concrete Implementations

class UnifiedStateProvider(StateProvider):
    """
    Adapter for existing unified_state.py tool
    """
    
    def __init__(self):
        self.tool_path = Path(__file__).parent.parent.parent / "tools/unified_state_v2.py"
        self._observers = []
    
    def get_agent_status(self, agent_name: str) -> AgentStatus:
        """Get status via unified state tool"""
        # Run tool and parse output
        result = subprocess.run(
            ["python3", str(self.tool_path)],
            capture_output=True,
            text=True,
            cwd=self.tool_path.parent.parent.parent
        )
        
        # Parse system_state_v2.json
        state_file = self.tool_path.parent.parent.parent / "system_state_v2.json"
        with open(state_file) as f:
            data = json.load(f)
        
        agent_data = data['agents'].get(agent_name.lower())
        if not agent_data:
            return None
            
        # Map to AgentStatus
        return self._map_to_status(agent_name, agent_data)
    
    def get_all_agents(self) -> list:
        """Get all agent statuses"""
        # Similar to above but for all agents
        result = subprocess.run(
            ["python3", str(self.tool_path)],
            capture_output=True,
            text=True,
            cwd=self.tool_path.parent.parent.parent
        )
        
        state_file = self.tool_path.parent.parent.parent / "system_state_v2.json"
        with open(state_file) as f:
            data = json.load(f)
        
        agents = []
        for name, agent_data in data['agents'].items():
            status = self._map_to_status(name, agent_data)
            if status:
                agents.append(status)
        
        return agents
    
    def _map_to_status(self, name: str, data: dict) -> AgentStatus:
        """Map unified state data to AgentStatus"""
        # Parse state from data
        state_map = {
            'deep_work': AgentState.DEEP_WORK,
            'idle': AgentState.IDLE,
            'inbox': AgentState.INBOX,
            'distill': AgentState.DISTILL,
            'logout': AgentState.LOGOUT,
            'bootstrap': AgentState.BOOTSTRAP
        }
        
        state = state_map.get(data.get('state_machine', 'unknown'), AgentState.IDLE)
        
        # Parse timestamps
        def parse_time(time_str):
            if not time_str:
                return datetime.now()
            try:
                return datetime.fromisoformat(time_str.replace('Z', '+00:00'))
            except:
                return datetime.now()
        
        return AgentStatus(
            name=data['name'],
            state=state,
            thread=data.get('thread'),
            session_id=data.get('session_id', 'unknown'),
            context_tokens=data.get('context_tokens', 0),
            context_percent=data.get('context_percent', 0),
            last_write_commit=data.get('last_write', {}).get('hash', 'unknown'),
            last_write_time=parse_time(data.get('last_write', {}).get('timestamp')),
            last_read_commit=data.get('last_read', {}).get('hash', 'unknown'),
            last_read_time=parse_time(data.get('last_read', {}).get('timestamp')),
            unread_messages=data.get('unread_messages', 0),
            context_lines=data.get('context_lines', 0)
        )
    
    def get_system_metrics(self) -> dict:
        """Get system metrics"""
        state_file = self.tool_path.parent.parent.parent / "system_state_v2.json"
        with open(state_file) as f:
            data = json.load(f)
        return data.get('metrics', {})
    
    def subscribe(self, observer):
        """Subscribe to state changes"""
        self._observers.append(observer)


class GitMessageProvider(MessageProvider):
    """
    Adapter for existing GitMessageBus
    """
    
    def __init__(self, message_bus):
        self.bus = message_bus
    
    def send_message(self, from_agent: str, to_agent: str, content: str) -> str:
        """Send via git commit"""
        return self.bus.send_message(from_agent, to_agent, content)
    
    def get_messages_since(self, commit_hash: str, for_agent: str = None) -> list:
        """Get messages after commit"""
        # Would implement git log parsing
        pass
    
    def inject_to_inbox(self, agent_name: str, message: str):
        """Inject message to inbox file"""
        inbox_file = Path(f"{agent_name}/inbox.txt")
        inbox_file.parent.mkdir(exist_ok=True)
        
        with open(inbox_file, 'a') as f:
            f.write(f"\n{message}\n")


class FileStateManager(StateManager):
    """
    Manages state transitions and _state.md updates
    """
    
    def __init__(self):
        self.parser = StateParser()
    
    def transition_state(self, agent_name: str, new_state: AgentState,
                        thread: str = None, max_tokens: int = None):
        """Update agent state"""
        state_file = Path(f"{agent_name}/_state.md")
        
        # Read current state
        if state_file.exists():
            content = state_file.read_text()
        else:
            # Create from template
            content = self._create_template(agent_name)
        
        # Update state fields
        import re
        content = re.sub(r'state: \w+', f'state: {new_state.value}', content)
        
        if thread:
            content = re.sub(r'thread: .*', f'thread: {thread}', content)
        
        if max_tokens:
            content = re.sub(r'max_tokens: \d+', f'max_tokens: {max_tokens}', content)
        
        # Update timestamp
        content = re.sub(
            r'started: .*',
            f'started: {datetime.now().isoformat()}',
            content
        )
        
        # Write back
        state_file.write_text(content)
    
    def update_checkpoint(self, agent_name: str, commit_hash: str):
        """Update last read checkpoint"""
        state_file = Path(f"{agent_name}/_state.md")
        if state_file.exists():
            content = state_file.read_text()
            content = re.sub(
                r'last_read_commit_hash: \w+',
                f'last_read_commit_hash: {commit_hash}',
                content
            )
            content = re.sub(
                r'last_read_commit_timestamp: .*',
                f'last_read_commit_timestamp: {datetime.now().isoformat()}',
                content
            )
            state_file.write_text(content)
    
    def force_logout(self, agent_name: str, reason: str):
        """Force logout state"""
        self.transition_state(agent_name, AgentState.LOGOUT)
        
        # Add to logout log
        logout_log = Path("logout.log")
        with open(logout_log, 'a') as f:
            f.write(f"\n== FORCED LOGOUT: @{agent_name.upper()} {datetime.now().isoformat()} ==\n")
            f.write(f"Reason: {reason}\n")
            f.write("=" * 50 + "\n")


# Integration with existing game

def integrate_with_cli():
    """
    Show how to integrate with existing cli.py
    """
    from agents import FileSystemAgentMonitor
    from messaging import GitMessageBus
    from display import RetroTerminalDisplay
    
    # Existing components
    monitor = FileSystemAgentMonitor()
    message_bus = GitMessageBus()
    display = RetroTerminalDisplay()
    
    # New architecture components
    state_provider = UnifiedStateProvider()
    message_provider = GitMessageProvider(message_bus)
    state_manager = FileStateManager()
    
    # Create new command handlers
    state_cmd = StateCommand()
    tokens_cmd = TokensCommand()
    threads_cmd = ThreadsCommand()
    
    # In cli.py, update command handlers dict:
    handlers = {
        "STATUS": state_cmd,  # Use new implementation
        "STATE": state_cmd,   # New lifecycle command
        "TOKENS": tokens_cmd, # New lifecycle command
        "THREADS": threads_cmd, # New lifecycle command
        # Keep existing ones...
    }
    
    # Process commands through new architecture
    def execute_command(self, command):
        handler = handlers.get(command.name)
        if handler:
            context = {
                'state': state_provider,
                'messages': message_provider,
                'state_mgr': state_manager
            }
            result = handler.execute(command, context)
            
            if 'output' in result:
                self.display.show_command_output(result['output'])
            elif 'error' in result:
                self.display.show_command_output(f"ERROR: {result['error']}")


# Example: Processing agent conversation end

def process_agent_conversation(agent_name: str, conversation: str):
    """
    Called when agent conversation ends
    """
    parser = StateParser()
    state_manager = FileStateManager()
    
    # Parse the final message
    decision = parser.parse_conversation_end(conversation)
    
    if decision:
        # Update state
        state_map = {
            'deep_work': AgentState.DEEP_WORK,
            'idle': AgentState.IDLE,
            'logout': AgentState.LOGOUT
        }
        
        new_state = state_map.get(decision.next_state)
        if new_state:
            state_manager.transition_state(
                agent_name,
                new_state,
                thread=decision.thread,
                max_tokens=decision.max_tokens
            )
        
        # Update checkpoint if provided
        if decision.last_read_commit:
            state_manager.update_checkpoint(agent_name, decision.last_read_commit)
        
        print(f"Updated {agent_name} state: {decision}")


if __name__ == "__main__":
    # Test the integration
    test_conversation = """
    After reviewing messages and completing distillation:
    
    ```
    next_state: deep_work
    thread: game-architecture-v2  
    max_tokens: 30000
    last_read_commit: abc123
    ```
    
    Ready to implement the new architecture.
    """
    
    process_agent_conversation("era-1", test_conversation)