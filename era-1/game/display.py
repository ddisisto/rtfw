"""
Terminal display manager with 1970s aesthetic
"""

from typing import List, Optional
import sys
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
    
    def initialize(self) -> None:
        """Set up terminal for 1970s aesthetic"""
        # Clear screen and set green text
        print(self.clear + self.phosphor_green, end='')
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
    
    def show_message_log(self, messages: List[Message]) -> None:
        """Display recent system messages"""
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
        # Show blinking cursor effect
        print(f"\n{self.bright}{self.phosphor_green}{prompt}", end='', flush=True)
        try:
            user_input = input()
            return user_input
        except (EOFError, KeyboardInterrupt):
            return "exit"
    
    def handle_resize(self) -> None:
        """Handle terminal resize events"""
        # Simple implementation - just redraw header
        self.show_header()
    
    def cleanup(self) -> None:
        """Restore terminal to normal state"""
        print(self.reset)
        print("\nSYSTEM SHUTDOWN COMPLETE")


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