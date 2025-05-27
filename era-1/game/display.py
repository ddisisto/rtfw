"""
Terminal display manager with 1970s aesthetic
"""

from typing import List, Optional, Tuple
import sys
import os
import time
import threading
import shutil
from datetime import datetime

from interfaces import DisplayManager, Agent, Message, AgentStatus


class RetroTerminalDisplay(DisplayManager):
    """
    1970s-style terminal display using basic ANSI codes
    
    Now with responsive layout that adapts to terminal size
    """
    
    def __init__(self):
        # Get actual terminal size
        self.update_terminal_size()
        
        # Colors
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
        
        # Layout will be calculated based on terminal size
        self.layout = {}
        self._calculate_layout()
        
        # For auto-refresh
        self.auto_refresh = False
        self.refresh_thread = None
        self.last_agents = []
        self.last_messages = []
    
    def update_terminal_size(self):
        """Get current terminal dimensions"""
        size = shutil.get_terminal_size((80, 24))  # Default fallback
        self.width = size.columns
        self.height = size.lines
    
    def _calculate_layout(self):
        """Calculate responsive layout based on terminal size"""
        # Minimum sizes
        min_header = 5
        min_input = 3
        min_status = 5
        min_messages = 4
        
        # Start with fixed sections
        self.layout['header_lines'] = min_header
        self.layout['input_lines'] = min_input
        
        # Remaining space for dynamic sections
        remaining = self.height - min_header - min_input - 4  # 4 for dividers
        
        if self.height < 20:  # Very small terminal
            # Compact mode
            self.layout['status_lines'] = min(remaining, min_status)
            self.layout['message_lines'] = 0  # Hide messages in tiny terminals
        elif self.height < 30:  # Small terminal
            # Split 60/40 between status and messages
            self.layout['status_lines'] = int(remaining * 0.6)
            self.layout['message_lines'] = remaining - self.layout['status_lines']
        else:  # Normal or large terminal
            # Split 70/30, but cap status at 20 lines
            self.layout['status_lines'] = min(int(remaining * 0.7), 20)
            self.layout['message_lines'] = remaining - self.layout['status_lines']
        
        # Calculate starting positions
        self.layout['status_start'] = self.layout['header_lines'] + 1
        self.layout['message_start'] = self.layout['status_start'] + self.layout['status_lines'] + 1
        self.layout['input_start'] = self.layout['message_start'] + self.layout['message_lines'] + 1
    
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
        # Draw divider lines based on calculated layout
        
        # Status section divider
        if self.layout['status_lines'] > 0:
            print(self._goto(self.layout['status_start']) + "-" * self.width)
        
        # Message section divider (only if we have message area)
        if self.layout['message_lines'] > 0:
            print(self._goto(self.layout['message_start']) + "-" * self.width)
        
        # Input section divider
        print(self._goto(self.layout['input_start']) + "=" * self.width)
    
    def show_header(self) -> None:
        """Display retro system header"""
        print(self._goto(1) + self.bright)
        print("=" * self.width)
        
        # Adjust title based on width
        if self.width < 60:
            print("RTFW MONITOR v1.0".center(self.width))
        else:
            print("RTFW SYSTEM MONITOR v1.0".center(self.width))
            print("FOUNDATION ERA TERMINAL".center(self.width))
        
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S").center(self.width))
        print("=" * self.width)
        print(self.reset + self.phosphor_green, end='')
    
    def show_status_panel(self, agents: List[Agent]) -> None:
        """Update agent status display in its designated area"""
        if self.layout['status_lines'] < 3:
            return  # Not enough space
            
        self.last_agents = agents  # Store for refresh
        
        # Position at status section
        row = self.layout['status_start'] + 1
        print(self._goto(row), end='')
        
        # Clear status area first
        for i in range(self.layout['status_lines'] - 1):
            print(self._goto(row + i) + self.clear_line, end='')
        
        # Draw status
        print(self._goto(row) + f"{self.bright}AGENT STATUS:{self.reset}{self.phosphor_green}")
        row += 1
        
        # Adjust columns based on width
        if self.width < 80:
            # Compact mode
            print(self._goto(row) + f"{'AGENT':<8} {'STATE':<8} {'CTX':<6} {'SEEN':<15}")
            row += 1
            
            # Agent rows
            max_agents = self.layout['status_lines'] - 3
            for i, agent in enumerate(agents[:max_agents]):
                if i >= max_agents:
                    break
                    
                # Shorter format for narrow terminals
                color = self.bright + self.phosphor_green if agent.status == AgentStatus.ACTIVE else self.phosphor_green
                ctx = f"{agent.context_percent:>3}%"
                seen = agent.last_activity[:15]
                
                print(self._goto(row + i) + f"{color}{agent.name[:8]:<8} {agent.status.value[:8]:<8} {ctx:<6} {seen:<15}{self.reset}{self.phosphor_green}")
        else:
            # Full mode
            print(self._goto(row) + f"{'AGENT':<10} {'STATUS':<10} {'CONTEXT':<12} {'LAST SEEN':<20} {'CURRENT TASK':<25}")
            row += 1
            
            # Agent rows (limited by available space)
            max_agents = self.layout['status_lines'] - 3
            for i, agent in enumerate(agents[:max_agents]):
                if i >= max_agents:
                    break
                    
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
                max_task_width = max(25, self.width - 65)  # Adaptive task width
                if len(task) > max_task_width:
                    task = task[:max_task_width-3] + "..."
                
                print(self._goto(row + i) + f"{color}{agent.name:<10} {agent.status.value:<10} {context_bar:<12} "
                      f"{agent.last_activity:<20} {task:<25}{self.reset}{self.phosphor_green}")
        
        # Auto-refresh indicator at bottom of status area
        if self.auto_refresh and self.layout['status_lines'] > 3:
            indicator_row = self.layout['status_start'] + self.layout['status_lines']
            indicator = "[AUTO-REFRESH: ON]" if self.width > 40 else "[AUTO]"
            print(self._goto(indicator_row) + self.clear_line + 
                  f"{self.dim}{indicator}{self.reset}{self.phosphor_green}", end='')
    
    def show_message_log(self, messages: List[Message]) -> None:
        """Display recent system messages in message area"""
        if self.layout['message_lines'] < 2:
            return  # Not enough space
            
        self.last_messages = messages  # Store for refresh
        
        # Position at message section
        row = self.layout['message_start'] + 1
        
        # Clear message area
        for i in range(self.layout['message_lines'] - 1):
            print(self._goto(row + i) + self.clear_line, end='')
        
        print(self._goto(row) + f"{self.bright}RECENT MESSAGES:{self.reset}{self.phosphor_green}")
        row += 1
        
        # Show messages (limited by available space)
        max_messages = self.layout['message_lines'] - 2
        for i, msg in enumerate(messages[:max_messages]):
            if i >= max_messages:
                break
                
            # Truncate long messages based on terminal width
            content = msg.content
            max_content = self.width - 10
            if len(content) > max_content:
                content = content[:max_content-3] + "..."
            
            print(self._goto(row + i) + f"{self.dim}{msg.hash[:7]}{self.reset}{self.phosphor_green} {content}")
    
    def show_command_output(self, output: str) -> None:
        """Display command execution results in message area temporarily"""
        if self.layout['message_lines'] < 2:
            # If no message area, show in status area briefly
            row = self.layout['status_start'] + 2
            print(self._goto(row) + self.clear_line + f"{self.phosphor_amber}{output[:self.width-2]}{self.phosphor_green}")
            return
            
        # Clear message area and show output
        row = self.layout['message_start'] + 1
        
        for i in range(self.layout['message_lines'] - 1):
            print(self._goto(row + i) + self.clear_line, end='')
        
        # Handle multi-line output
        lines = output.split('\n')
        for i, line in enumerate(lines[:self.layout['message_lines']-1]):
            if i >= self.layout['message_lines'] - 1:
                break
            print(self._goto(row + i) + f"{self.phosphor_amber}{line[:self.width-2]}{self.phosphor_green}")
    
    def get_input(self, prompt: str = "> ") -> str:
        """Get user input in dedicated input area"""
        # Position at input area
        input_row = self.layout['input_start'] + 1
        
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
        # Check if terminal was resized
        old_size = (self.width, self.height)
        self.update_terminal_size()
        
        if (self.width, self.height) != old_size:
            # Terminal resized - need full redraw
            self._calculate_layout()
            self.handle_resize()
            return
        
        # Update header timestamp
        ts_row = 3 if self.width >= 60 else 2  # Adjust for compact header
        print(self._goto(ts_row + 1) + self.clear_line + 
              datetime.now().strftime("%Y-%m-%d %H:%M:%S").center(self.width))
        
        # Update status panel
        self.show_status_panel(agents)
        
        # Update messages if provided
        if messages:
            self.show_message_log(messages)
        
        # Make sure cursor returns to input area
        input_row = self.layout['input_start'] + 1
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
        
        if self.width < 60:
            print("RTFW MONITOR [LIVE]".center(self.width))
        else:
            print("RTFW SYSTEM MONITOR v1.0 [LIVE]".center(self.width))
            print("FOUNDATION ERA TERMINAL".center(self.width))
        
        # Blinking timestamp for that authentic feel
        if int(time.time()) % 2 == 0:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S").center(self.width))
        else:
            print((" " * 19).center(self.width))  # Blank for blink effect
            
        print("=" * self.width)
        print(self.reset + self.phosphor_green)


class AdaptivePhosphorDisplay(RetroTerminalDisplay):
    """
    Modern responsive version with adaptive layouts
    
    Supports ultra-wide monitors and tiny terminals alike
    """
    
    def __init__(self):
        super().__init__()
        self.supports_unicode = self._check_unicode_support()
    
    def _check_unicode_support(self) -> bool:
        """Check if terminal supports unicode"""
        try:
            print("░", end='', file=sys.stderr)
            return True
        except:
            return False
    
    def _draw_layout(self):
        """Draw layout with optional unicode box drawing"""
        if self.supports_unicode and self.width > 100:
            # Fancy box drawing for wide terminals
            h_line = "─" * self.width
            double_line = "═" * self.width
        else:
            # Fallback to ASCII
            h_line = "-" * self.width
            double_line = "=" * self.width
        
        # Draw divider lines based on calculated layout
        if self.layout['status_lines'] > 0:
            print(self._goto(self.layout['status_start']) + h_line)
        
        if self.layout['message_lines'] > 0:
            print(self._goto(self.layout['message_start']) + h_line)
        
        print(self._goto(self.layout['input_start']) + double_line)