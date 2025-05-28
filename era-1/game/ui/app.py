"""
Foundation Terminal - Main Application
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, DataTable, RichLog, Input
from textual.binding import Binding
from textual.reactive import reactive
from textual import events
from textual.timer import Timer
from datetime import datetime
from pathlib import Path
import sys

# Add parent for engine imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.threaded_engine import ThreadedStateEngine
from ui.widgets import AgentList, AgentDetails, CommandPalette
from ui.theme import PHOSPHOR_CSS


class FoundationTerminal(App):
    """Main TUI Application"""
    
    CSS = PHOSPHOR_CSS
    TITLE = "Foundation Terminal v0.1.0"
    BINDINGS = [
        Binding("q", "quit", "Quit", key_display="Q"),
        Binding("r", "refresh", "Refresh", key_display="R"),
        Binding("m", "message", "Message", key_display="M"),
        Binding("s", "status", "Status", key_display="S"),
        Binding("h", "help", "Help", key_display="H"),
    ]
    
    def __init__(self):
        super().__init__()
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.sessions_dir = self.project_root / "_sessions"
        self.engine = None
        self.refresh_timer = None
        
        # Configuration options
        self.debug_mode = False
        self.use_engine = True
        self.refresh_interval = 5.0
        self.color_theme = "amber"
        self.oneshot_mode = False
        
    def compose(self) -> ComposeResult:
        """Create the application layout"""
        yield Header(show_clock=True)
        
        with Horizontal(id="main"):
            # Left sidebar
            with Vertical(id="sidebar"):
                yield AgentList(id="agent-list")
                yield CommandPalette(id="commands")
            
            # Main content area
            yield AgentDetails(id="agent-details")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize the application after mounting"""
        # Start the state engine if enabled
        if self.use_engine:
            self.engine = ThreadedStateEngine(
                self.project_root,
                self.sessions_dir
            )
            self.engine.start()
        
        # Start refresh timer
        self.refresh_timer = self.set_interval(self.refresh_interval, self.refresh_agents)
        
        # Load initial agent data
        self.refresh_agents()
        
        # In oneshot mode, capture and exit after first render
        if self.oneshot_mode:
            # Use call_after_refresh to ensure UI is fully rendered
            self.call_after_refresh(self._oneshot_capture)
        
    def on_unmount(self) -> None:
        """Clean up when app closes"""
        if self.engine:
            self.engine.stop()
            
    def refresh_agents(self) -> None:
        """Refresh agent states from engine"""
        if not self.engine:
            # Use mock data when engine is disabled
            from datetime import datetime
            
            # Mock agent data structure
            class MockState:
                def __init__(self, name, state, thread, context_pct):
                    self.state = state
                    self.thread = thread
                    self.context_percent = context_pct
                    self.context_tokens = int(context_pct * 1280)
                    self.max_context_tokens = 128000
                    self.session_id = "mock-session-12345"
                    self.last_write_commit_hash = "abc123d"
                    self.last_write_commit_timestamp = datetime.now().isoformat()
                    self.unread_message_count = 0
            
            agents = {
                "ERA-1": MockState("ERA-1", "deep_work", "tui-implementation", 17.0),
                "GOV": MockState("GOV", "idle", None, 45.2),
                "NEXUS": MockState("NEXUS", "inbox", "message-routing", 23.5),
                "CRITIC": MockState("CRITIC", "distill", "pattern-analysis", 82.1),
            }
        else:
            # Get all agent states from engine
            agents = self.engine.get_all_agents()
        
        # Update agent list widget
        agent_list = self.query_one("#agent-list", AgentList)
        agent_list.update_agents(agents)
        
        # Update details if an agent is selected
        if agent_list.selected_agent:
            details = self.query_one("#agent-details", AgentDetails)
            if agent_list.selected_agent in agents:
                details.update_agent(
                    agent_list.selected_agent,
                    agents[agent_list.selected_agent]
                )
    
    def action_refresh(self) -> None:
        """Manual refresh action"""
        if self.engine:
            self.engine.force_poll()
        self.refresh_agents()
        
    def action_message(self) -> None:
        """Open message dialog"""
        # TODO: Implement message modal
        self.notify("Message feature coming soon!")
        
    def action_status(self) -> None:
        """Show all agent statuses"""
        # TODO: Implement status modal
        self.notify("Status overview coming soon!")
        
    def action_help(self) -> None:
        """Show help"""
        # TODO: Implement help modal
        self.notify("Help coming soon!")
    
    def _oneshot_capture(self) -> None:
        """Capture screen in oneshot mode and exit"""
        # Schedule exit after a brief delay to ensure render completes
        self.set_timer(0.5, lambda: self.exit())


if __name__ == "__main__":
    app = FoundationTerminal()
    app.run()