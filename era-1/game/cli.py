#!/usr/bin/env python3
"""
ERA-1 Foundation Terminal - Main Game Loop

A 1970s-style system monitoring terminal that provides real control
over the rtfw multi-agent system.
"""

import sys
import signal
from typing import Dict

from interfaces import CommandHandler
from agents import FileSystemAgentMonitor  
from messaging import GitMessageBus
from display import RetroTerminalDisplay
from commands import (
    RetroCommandParser, StatusCommand, MessageCommand, 
    LogCommand, HelpCommand
)


class ERA1Terminal:
    """Main game controller"""
    
    def __init__(self):
        # Initialize components
        self.display = RetroTerminalDisplay()
        self.monitor = FileSystemAgentMonitor()
        self.message_bus = GitMessageBus()
        self.parser = RetroCommandParser()
        
        # Initialize command handlers
        self.handlers: Dict[str, CommandHandler] = {
            "STATUS": StatusCommand(self.monitor),
            "MESSAGE": MessageCommand(self.message_bus),
            "LOG": LogCommand(self.message_bus),
            "HELP": HelpCommand(self.parser),
        }
        
        self.running = True
    
    def start(self):
        """Start the game loop"""
        # Set up signal handlers
        signal.signal(signal.SIGINT, self._handle_interrupt)
        signal.signal(signal.SIGTERM, self._handle_interrupt)
        
        # Initialize display
        self.display.initialize()
        
        # Show initial status
        self._show_full_status()
        
        # Main game loop
        while self.running:
            try:
                # Get user input
                user_input = self.display.get_input()
                
                if user_input.upper() in ["EXIT", "QUIT"]:
                    self.running = False
                    continue
                
                # Parse command
                command = self.parser.parse(user_input)
                if not command:
                    continue
                
                # Execute command
                if command.name in self.handlers:
                    output = self.handlers[command.name].execute(command)
                    
                    # Special handling for STATUS with no args
                    if command.name == "STATUS" and not command.args:
                        self._show_full_status()
                    elif output:
                        self.display.show_command_output(output)
                else:
                    self.display.show_command_output(
                        f"UNKNOWN COMMAND: {command.name}\nTYPE 'HELP' FOR AVAILABLE COMMANDS"
                    )
                    
            except Exception as e:
                self.display.show_command_output(f"SYSTEM ERROR: {str(e)}")
        
        # Cleanup
        self.display.cleanup()
    
    def _show_full_status(self):
        """Display full agent status panel"""
        try:
            agents = []
            for agent_name in self.monitor.get_all_agents():
                agent = self.monitor.get_agent_status(agent_name)
                agents.append(agent)
            
            self.display.show_status_panel(agents)
        except Exception as e:
            self.display.show_command_output(f"ERROR RETRIEVING STATUS: {str(e)}")
    
    def _handle_interrupt(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        self.running = False


def main():
    """Entry point"""
    terminal = ERA1Terminal()
    
    try:
        terminal.start()
    except Exception as e:
        print(f"\nFATAL ERROR: {str(e)}")
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()