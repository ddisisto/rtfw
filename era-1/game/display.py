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
        self.phosphor_green = "\033[32m"  # Green text
        self.phosphor_amber = "\033[33m"  # Amber text  
        self.dim = "\033[2m"
        self.bright = "\033[1m"
        self.reset = "\033[0m"
        self.clear = "\033[2J\033[H"
        self.save_cursor = "\033[s"
        self.restore_cursor = "\033[u"
        self.hide_cursor = "\033[?25l"
        self.show_cursor = "\033[?25h"
        
        # For auto-refresh
        self.auto_refresh = False
        self.refresh_thread = None
        self.last_agents = []
        self.last_messages = []
    
    def initialize(self) -> None:
        """Set up terminal for 1970s aesthetic"""
        # Clear screen and set green text
        print(self.hide_cursor + self.clear + self.phosphor_green, end='')
        self.show_header()
    
    def show_header(self) -> None:
        """Display retro system header"""
        print(self.bright)
        print("=" * self.width)
        print("RTFW SYSTEM MONITOR v1.0".center(self.width))
        print("FOUNDATION ERA TERMINAL".center(self.width))
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S").center(self.width))
        print("=" * self.width)
        print(self.reset + self.phosphor_green)
    
    def show_status_panel(self, agents: List[Agent]) -> None:
        """Update agent status display"""
        self.last_agents = agents  # Store for refresh
        
        print(f"\n{self.bright}AGENT STATUS:{self.reset}{self.phosphor_green}")
        print("-" * self.width)
        
        # Header
        print(f"{'AGENT':<10} {'STATUS':<10} {'CONTEXT':<12} {'LAST SEEN':<20} {'CURRENT TASK':<25}")
        print("-" * self.width)
        
        # Agent rows
        for agent in agents:
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
            
            print(f"{color}{agent.name:<10} {agent.status.value:<10} {context_bar:<12} "
                  f"{agent.last_activity:<20} {task:<25}{self.reset}{self.phosphor_green}")
        
        print("-" * self.width)
        
        # Auto-refresh indicator
        if self.auto_refresh:
            print(f"{self.dim}[AUTO-REFRESH ACTIVE - Press 'r' to toggle]{self.reset}{self.phosphor_green}")
    
    def show_message_log(self, messages: List[Message]) -> None:
        """Display recent system messages"""
        self.last_messages = messages  # Store for refresh
        
        print(f"\n{self.bright}RECENT MESSAGES:{self.reset}{self.phosphor_green}")
        print("-" * self.width)
        
        for msg in messages[:10]:  # Show last 10
            # Truncate long messages
            content = msg.content
            if len(content) > self.width - 10:
                content = content[:self.width - 13] + "..."
            
            print(f"{self.dim}{msg.hash[:7]}{self.reset}{self.phosphor_green} {content}")
        
        print("-" * self.width)
    
    def show_command_output(self, output: str) -> None:
        """Display command execution results"""
        print(f"\n{self.phosphor_amber}{output}{self.phosphor_green}")
    
    def get_input(self, prompt: str = "> ") -> str:
        """Get user input with retro prompt"""
        # Show cursor for input
        print(f"\n{self.show_cursor}{self.bright}{self.phosphor_green}{prompt}", end='', flush=True)
        try:
            user_input = input()
            print(self.hide_cursor, end='')  # Hide again after input
            return user_input
        except (EOFError, KeyboardInterrupt):
            return "exit"
    
    def refresh_display(self, agents: List[Agent], messages: Optional[List[Message]] = None):
        """Refresh the entire display with new data"""
        # Save cursor position
        print(self.save_cursor, end='')
        
        # Clear and redraw
        print(self.clear, end='')
        self.show_header()
        self.show_status_panel(agents)
        
        if messages:
            self.show_message_log(messages)
        
        # Restore cursor
        print(self.restore_cursor, end='', flush=True)
    
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
        # Simple implementation - just redraw header
        self.show_header()
    
    def cleanup(self) -> None:
        """Restore terminal to normal state"""
        self.stop_auto_refresh()
        print(self.show_cursor + self.reset)
        print("\nSYSTEM SHUTDOWN COMPLETE")


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
        print(self.bright)
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