"""
Terminal display manager with 1970s aesthetic
"""

from typing import List, Optional
import sys
import time
import threading
from datetime import datetime

from interfaces import DisplayManager, Agent, Message, AgentStatus


class RetroTerminalDisplay(DisplayManager):
    """
    1970s-style terminal display using basic ANSI codes
    
    Keeping it simple initially - can enhance with blessed later
    """
    
    def __init__(self):
        self.width = 80  # Classic terminal width
        self.height = 24  # Classic terminal height
        self.phosphor_green = "\033[32m"  # Green text
        self.phosphor_amber = "\033[33m"  # Amber text  
        self.dim = "\033[2m"
        self.bright = "\033[1m"
        self.reset = "\033[0m"
        self.clear = "\033[2J\033[H"
        self.clear_line = "\033[2K"
        self.save_cursor = "\033[s"
        self.restore_cursor = "\033[u"
        self.hide_cursor = "\033[?25l"
        self.show_cursor = "\033[?25h"
        
        # Layout configuration
        self.header_lines = 5
        self.status_lines = 10  # Reserved for agent status
        self.message_lines = 6  # Reserved for messages
        self.input_lines = 3   # Reserved for input area
        
        # For auto-refresh
        self.auto_refresh = False
        self.refresh_thread = None
        self.last_agents = []
        self.last_messages = []
    
    def _goto(self, row: int, col: int = 1) -> str:
        """ANSI escape to position cursor"""
        return f"\033[{row};{col}H"
    
    def initialize(self) -> None:
        """Set up terminal for 1970s aesthetic"""
        # Clear screen and set green text
        print(self.hide_cursor + self.clear + self.phosphor_green, end='')
        self._draw_layout()
        self.show_header()
    
    def _draw_layout(self):
        """Draw the basic terminal layout structure"""
        # Draw divider lines
        status_start = self.header_lines + 1
        message_start = status_start + self.status_lines + 1
        input_start = message_start + self.message_lines + 1
        
        # Status section divider
        print(self._goto(status_start) + "-" * self.width)
        
        # Message section divider
        print(self._goto(message_start) + "-" * self.width)
        
        # Input section divider
        print(self._goto(input_start) + "=" * self.width)
    
    def show_header(self) -> None:
        """Display retro system header"""
        print(self._goto(1) + self.bright)
        print("=" * self.width)
        print("RTFW SYSTEM MONITOR v1.0".center(self.width))
        print("FOUNDATION ERA TERMINAL".center(self.width))
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S").center(self.width))
        print("=" * self.width)
        print(self.reset + self.phosphor_green, end='')
    
    def show_status_panel(self, agents: List[Agent]) -> None:
        """Update agent status display in its designated area"""
        self.last_agents = agents  # Store for refresh
        
        # Position at status section
        row = self.header_lines + 2
        print(self._goto(row), end='')
        
        # Clear status area first
        for i in range(self.status_lines - 1):
            print(self._goto(row + i) + self.clear_line, end='')
        
        # Draw status
        print(self._goto(row) + f"{self.bright}AGENT STATUS:{self.reset}{self.phosphor_green}")
        row += 1
        
        # Header
        print(self._goto(row) + f"{'AGENT':<10} {'STATUS':<10} {'CONTEXT':<12} {'LAST SEEN':<20} {'CURRENT TASK':<25}")
        row += 1
        
        # Agent rows (limited by available space)
        max_agents = self.status_lines - 3
        for i, agent in enumerate(agents[:max_agents]):
            # Color based on status
            if agent.status == AgentStatus.ACTIVE:
                color = self.bright + self.phosphor_green
            elif agent.status == AgentStatus.OFFLINE:
                color = self.dim
            else:
                color = self.phosphor_green
            
            # Format context as percentage bar
            bar_width = 10
            filled = int(agent.context_percent * bar_width // 100)
            context_bar = f"[{'#' * filled}{'-' * (bar_width - filled)}]"
            
            # Truncate task if needed
            task = agent.current_task or "-"
            if len(task) > 25:
                task = task[:22] + "..."
            
            print(self._goto(row + i) + f"{color}{agent.name:<10} {agent.status.value:<10} {context_bar:<12} "
                  f"{agent.last_activity:<20} {task:<25}{self.reset}{self.phosphor_green}")
        
        # Auto-refresh indicator at bottom of status area
        if self.auto_refresh:
            indicator_row = self.header_lines + self.status_lines
            print(self._goto(indicator_row) + self.clear_line + 
                  f"{self.dim}[AUTO-REFRESH: ON]{self.reset}{self.phosphor_green}", end='')
    
    def show_message_log(self, messages: List[Message]) -> None:
        """Display recent system messages in message area"""
        self.last_messages = messages  # Store for refresh
        
        # Position at message section
        row = self.header_lines + self.status_lines + 3
        
        # Clear message area
        for i in range(self.message_lines - 1):
            print(self._goto(row + i) + self.clear_line, end='')
        
        print(self._goto(row) + f"{self.bright}RECENT MESSAGES:{self.reset}{self.phosphor_green}")
        row += 1
        
        # Show messages (limited by available space)
        max_messages = self.message_lines - 2
        for i, msg in enumerate(messages[:max_messages]):
            if i >= max_messages:
                break
                
            # Truncate long messages
            content = msg.content
            if len(content) > self.width - 10:
                content = content[:self.width - 13] + "..."
            
            print(self._goto(row + i) + f"{self.dim}{msg.hash[:7]}{self.reset}{self.phosphor_green} {content}")
    
    def show_command_output(self, output: str) -> None:
        """Display command execution results in message area temporarily"""
        # Clear message area and show output
        row = self.header_lines + self.status_lines + 3
        
        for i in range(self.message_lines - 1):
            print(self._goto(row + i) + self.clear_line, end='')
        
        print(self._goto(row) + f"{self.phosphor_amber}{output}{self.phosphor_green}")
    
    def get_input(self, prompt: str = "> ") -> str:
        """Get user input in dedicated input area"""
        # Position at input area
        input_row = self.header_lines + self.status_lines + self.message_lines + 2
        
        # Clear input line
        print(self._goto(input_row) + self.clear_line, end='')
        
        # Show cursor and prompt
        print(self._goto(input_row) + f"{self.show_cursor}{self.bright}{self.phosphor_green}{prompt}", end='', flush=True)
        
        try:
            user_input = input()
            print(self.hide_cursor, end='')  # Hide again after input
            return user_input
        except (EOFError, KeyboardInterrupt):
            return "exit"
    
    def refresh_display(self, agents: List[Agent], messages: Optional[List[Message]] = None):
        """Refresh only the data areas, preserving layout"""
        # Update header timestamp
        print(self._goto(4) + self.clear_line + 
              datetime.now().strftime("%Y-%m-%d %H:%M:%S").center(self.width))
        
        # Update status panel
        self.show_status_panel(agents)
        
        # Update messages if provided
        if messages:
            self.show_message_log(messages)
        
        # Make sure cursor returns to input area
        input_row = self.header_lines + self.status_lines + self.message_lines + 2
        print(self._goto(input_row, 3), end='', flush=True)  # After "> "
    
    def start_auto_refresh(self, refresh_callback, interval: int = 5):
        """Start auto-refresh thread"""
        self.auto_refresh = True
        
        def refresh_loop():
            while self.auto_refresh:
                time.sleep(interval)
                if self.auto_refresh:  # Check again after sleep
                    refresh_callback()
        
        self.refresh_thread = threading.Thread(target=refresh_loop, daemon=True)
        self.refresh_thread.start()
    
    def stop_auto_refresh(self):
        """Stop auto-refresh"""
        self.auto_refresh = False
        if self.refresh_thread:
            self.refresh_thread.join(timeout=1)
    
    def handle_resize(self) -> None:
        """Handle terminal resize events"""
        # Redraw entire layout
        print(self.clear, end='')
        self._draw_layout()
        self.show_header()
        
        # Redraw data if available
        if self.last_agents:
            self.show_status_panel(self.last_agents)
        if self.last_messages:
            self.show_message_log(self.last_messages)
    
    def cleanup(self) -> None:
        """Restore terminal to normal state"""
        self.stop_auto_refresh()
        print(self.show_cursor + self.reset + self.clear)
        print("SYSTEM SHUTDOWN COMPLETE")


class RealtimeDisplay(RetroTerminalDisplay):
    """
    Enhanced display with real-time updates
    
    This version actively monitors and refreshes
    """
    
    def __init__(self):
        super().__init__()
        self.update_interval = 3  # seconds
        self.show_timestamps = True
    
    def show_header(self) -> None:
        """Display header with live timestamp"""
        print(self._goto(1) + self.bright)
        print("=" * self.width)
        print("RTFW SYSTEM MONITOR v1.0 [LIVE]".center(self.width))
        print("FOUNDATION ERA TERMINAL".center(self.width))
        
        # Blinking timestamp for that authentic feel
        if int(time.time()) % 2 == 0:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S").center(self.width))
        else:
            print((" " * 19).center(self.width))  # Blank for blink effect
            
        print("=" * self.width)
        print(self.reset + self.phosphor_green)


class PhosphorDisplay(DisplayManager):
    """
    Enhanced display using blessed library for better control
    
    This will be the full implementation with proper windowing
    """
    
    def __init__(self):
        # Defer blessed import to avoid dependency issues initially
        self.term = None
        self.phosphor_green = "#00FF00"
        self.phosphor_amber = "#FFAA00"
        
    def initialize(self) -> None:
        """Set up blessed terminal"""
        try:
            from blessed import Terminal
            self.term = Terminal()
            print(self.term.home + self.term.clear)
            # Set up color palette and layout
        except ImportError:
            # Fallback to basic display
            print("Note: Install 'blessed' for enhanced display")
            self.fallback = RetroTerminalDisplay()
            self.fallback.initialize()
    
    # ... implement other methods with blessed features ...