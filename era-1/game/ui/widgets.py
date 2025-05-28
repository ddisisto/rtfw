"""
Foundation Terminal - Custom Widgets
"""

from textual.app import ComposeResult
from textual.widgets import Static, DataTable, RichLog, Button
from textual.containers import Vertical, Horizontal, ScrollableContainer
from textual.reactive import reactive
from textual import events
from textual.widgets import DataTable
from datetime import datetime
from typing import Dict, Optional


class AgentList(Static):
    """Agent list with live status indicators"""
    
    selected_agent = reactive(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agents_data = {}
        
    def compose(self) -> ComposeResult:
        """Create the agent list layout"""
        yield Static("═ AGENTS ═", classes="title")
        yield DataTable(id="agent-table", show_header=False)
        
    def on_mount(self) -> None:
        """Initialize the data table"""
        table = self.query_one("#agent-table", DataTable)
        table.add_column("agent", key="agent")
        table.add_column("state", key="state")
        table.cursor_type = "row"
        
    def update_agents(self, agents: Dict) -> None:
        """Update the agent list with new data"""
        self.agents_data = agents
        table = self.query_one("#agent-table", DataTable)
        
        # Clear existing rows
        table.clear()
        
        # Add agent rows
        for name, state_data in agents.items():
            state = state_data.state if state_data else "offline"
            context_pct = state_data.context_percent if state_data else 0
            
            # Color code based on state and context
            if state in ["inbox", "deep_work"]:
                style = "active"
            elif state == "idle":
                style = "idle"
            elif context_pct > 80:
                style = "alert"
            else:
                style = "offline"
                
            # Format: "@NAME [state]"
            display = f"@{name:<8} [{state:>10}]"
            table.add_row(display, "", key=name)
            
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle agent selection"""
        if event.row_key:
            self.selected_agent = str(event.row_key.value)


class AgentDetails(Static):
    """Detailed agent information panel"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_agent = None
        self.current_state = None
        
    def compose(self) -> ComposeResult:
        """Create the details layout"""
        with Vertical():
            yield Static("", id="agent-header", classes="title")
            yield Static("", id="agent-info")
            
            yield Static("═ ACTIVITY LOG ═", classes="title")
            yield RichLog(id="activity-log", wrap=True, highlight=True)
            
            yield Static("═ QUICK ACTIONS ═", classes="title")
            with Horizontal(id="quick-actions"):
                yield Button("[M]essage", id="btn-message", variant="primary")
                yield Button("[T]rigger", id="btn-trigger")
                yield Button("[V]iew", id="btn-view")
                
    def update_agent(self, agent_name: str, state_data) -> None:
        """Update display with agent details"""
        self.current_agent = agent_name
        self.current_state = state_data
        
        # Update header
        header = self.query_one("#agent-header", Static)
        header.update(f"═ @{agent_name} ═")
        
        # Update info
        info = self.query_one("#agent-info", Static)
        if state_data:
            info_text = f"""State: {state_data.state}
Thread: {state_data.thread or 'none'}
Context: {state_data.context_percent:.1f}% ({state_data.context_tokens}/{state_data.max_context_tokens})
Session: {state_data.session_id[:8]}...
Last Commit: {state_data.last_write_commit_hash[:7]}
Unread: {state_data.unread_message_count}"""
        else:
            info_text = "Agent offline or no data available"
            
        info.update(info_text)
        
        # Update activity log
        log = self.query_one("#activity-log", RichLog)
        log.clear()
        if state_data and state_data.last_write_commit_timestamp:
            log.write(f"{state_data.last_write_commit_timestamp} - Last commit")
        # TODO: Add more activity from git log


class CommandPalette(Static):
    """Command shortcuts panel"""
    
    def compose(self) -> ComposeResult:
        """Create command palette"""
        yield Static("═ COMMANDS ═", classes="title")
        with Vertical(id="command-list"):
            commands = [
                "[S]tatus - All agents",
                "[M]essage - Send commit", 
                "[T]okens - Context usage",
                "[L]og - System activity",
                "[D]istill - Force distill",
                "[I]nject - State change",
                "[R]efresh - Update now",
                "[H]elp - Show help",
                "[Q]uit - Exit terminal"
            ]
            for cmd in commands:
                yield Static(cmd, classes="command")