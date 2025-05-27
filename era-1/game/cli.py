#!/usr/bin/env python3
"""
ERA-1 Foundation Terminal - Main Game Loop

A 1970s-style system monitoring terminal that provides real control
over the rtfw multi-agent system.

Usage:
    cli.py                                  # Interactive mode
    cli.py status [AGENT]                   # Show status
    cli.py message AGENT "content"          # Send message
    cli.py log [--count N] [--from AGENT]   # Show logs
"""

import sys
import signal
import argparse
from typing import Dict, Optional

from interfaces import CommandHandler
from agents import FileSystemAgentMonitor  
from messaging import GitMessageBus
from display import RetroTerminalDisplay
from commands import (
    RetroCommandParser, StatusCommand, MessageCommand, 
    LogCommand, HelpCommand, Command
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
        self.monitoring = False
    
    def start_interactive(self):
        """Start the interactive game loop"""
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
                
                # Handle special interactive commands
                if user_input.upper() == "MONITOR":
                    self._toggle_monitoring()
                    continue
                
                # Parse command
                command = self.parser.parse(user_input)
                if not command:
                    continue
                
                # Execute command
                self._execute_command(command)
                    
            except Exception as e:
                self.display.show_command_output(f"SYSTEM ERROR: {str(e)}")
        
        # Cleanup
        self.display.cleanup()
    
    def execute_one_shot(self, cmd_name: str, args: list):
        """Execute a single command and exit"""
        # Create command object
        command = Command(name=cmd_name.upper(), args=args, raw=" ".join([cmd_name] + args))
        
        # Simple output for one-shot mode
        if cmd_name == "status" and not args:
            # Full status - show all agents
            agents = []
            for agent_name in self.monitor.get_all_agents():
                agent = self.monitor.get_agent_status(agent_name)
                agents.append(agent)
            
            # Simple text output
            print("AGENT      STATUS     CONTEXT    LAST SEEN")
            print("-" * 50)
            for agent in agents:
                print(f"{agent.name:<10} {agent.status.value:<10} {agent.context_percent:>3}%      {agent.last_activity}")
        else:
            # Execute normally
            if command.name in self.handlers:
                output = self.handlers[command.name].execute(command)
                if output:
                    print(output)
            else:
                print(f"Unknown command: {cmd_name}")
                sys.exit(1)
    
    def _execute_command(self, command: Command):
        """Execute a parsed command"""
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
    
    def _toggle_monitoring(self):
        """Toggle real-time monitoring mode"""
        if self.monitoring:
            self.display.stop_auto_refresh()
            self.monitoring = False
            self.display.show_command_output("MONITORING DISABLED")
        else:
            # Start auto-refresh with callback
            def refresh():
                try:
                    agents = []
                    for agent_name in self.monitor.get_all_agents():
                        agent = self.monitor.get_agent_status(agent_name)
                        agents.append(agent)
                    
                    # Get recent messages too
                    messages = self.message_bus.get_recent_messages(10)
                    
                    # Refresh display
                    self.display.refresh_display(agents, messages)
                except Exception as e:
                    # Fail silently in refresh to avoid spam
                    pass
            
            self.display.start_auto_refresh(refresh, interval=3)
            self.monitoring = True
            self.display.show_command_output("MONITORING ENABLED - REFRESH EVERY 3 SECONDS")


def create_parser():
    """Create argument parser for CLI mode"""
    parser = argparse.ArgumentParser(
        description="ERA-1 Foundation Terminal - System Monitor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ./cli.py                              # Start interactive mode
  ./cli.py status                       # Show all agent status  
  ./cli.py status GOV                   # Show GOV agent status
  ./cli.py message GOV "Hello"          # Send message to GOV
  ./cli.py log                          # Show recent activity
  ./cli.py log --count 50               # Show last 50 messages
  ./cli.py log --from GOV               # Show messages from GOV
  ./cli.py log --mentions ERA-1         # Show messages mentioning ERA-1
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show agent status')
    status_parser.add_argument('agent', nargs='?', help='Agent name (optional)')
    
    # Message command
    msg_parser = subparsers.add_parser('message', help='Send message to agent')
    msg_parser.add_argument('agent', help='Target agent')
    msg_parser.add_argument('content', help='Message content')
    
    # Log command
    log_parser = subparsers.add_parser('log', help='Show activity log')
    log_parser.add_argument('--count', '-n', type=int, default=20, help='Number of entries')
    log_parser.add_argument('--from', '-f', dest='from_agent', help='Filter by sender')
    log_parser.add_argument('--mentions', '-m', help='Filter by mentions')
    
    return parser


def main():
    """Entry point with CLI argument support"""
    parser = create_parser()
    args = parser.parse_args()
    
    terminal = ERA1Terminal()
    
    try:
        if args.command:
            # One-shot command mode
            if args.command == 'status':
                terminal.execute_one_shot('status', [args.agent] if args.agent else [])
            
            elif args.command == 'message':
                terminal.execute_one_shot('message', [args.agent, args.content])
            
            elif args.command == 'log':
                # Build log arguments
                log_args = [str(args.count)]
                
                # Enhanced log handling for filters
                if args.from_agent or args.mentions:
                    # Need to implement filtered log in one-shot mode
                    bus = GitMessageBus()
                    
                    if args.mentions:
                        messages = bus.get_messages_for_agent(args.mentions, args.count)
                    else:
                        messages = bus.get_recent_messages(args.count)
                    
                    # Filter by sender if specified
                    if args.from_agent:
                        messages = [m for m in messages if m.author == args.from_agent]
                    
                    # Print results
                    if not messages:
                        print("NO MESSAGES FOUND")
                    else:
                        for msg in messages[:args.count]:
                            print(f"{msg.hash[:7]} {msg.content}")
                else:
                    terminal.execute_one_shot('log', log_args)
        else:
            # Interactive mode (default)
            terminal.start_interactive()
            
    except KeyboardInterrupt:
        print("\n\nSYSTEM SHUTDOWN")
        sys.exit(0)
    except Exception as e:
        print(f"\nFATAL ERROR: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()