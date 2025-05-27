"""
Command parsing and implementation for 1970s-style interface
"""

import re
from typing import Dict, List, Optional
from datetime import datetime

from interfaces import Command, CommandParser, CommandHandler
from agents import FileSystemAgentMonitor
from messaging import GitMessageBus


class RetroCommandParser(CommandParser):
    """
    Parse commands with 1970s mainframe style
    
    Examples:
    - STATUS
    - STATUS GOV
    - MESSAGE GOV "Please review protocols"
    - LOG 10
    - HELP
    """
    
    def __init__(self):
        self.commands = {
            "STATUS": "Display agent status",
            "MESSAGE": "Send message to agent", 
            "LOG": "Show recent activity",
            "CONTEXT": "Show agent context health",
            "MONITOR": "Toggle real-time monitoring (interactive only)",
            "HELP": "Display available commands",
            "EXIT": "Exit system monitor",
            "QUIT": "Exit system monitor",
        }
    
    def parse(self, input_line: str) -> Optional[Command]:
        """Parse user input into command structure"""
        if not input_line.strip():
            return None
        
        # Split preserving quoted strings
        parts = self._split_with_quotes(input_line.strip().upper())
        if not parts:
            return None
        
        cmd_name = parts[0]
        args = [p.strip('"') for p in parts[1:]]  # Remove quotes from args
        
        return Command(name=cmd_name, args=args, raw=input_line)
    
    def _split_with_quotes(self, line: str) -> List[str]:
        """Split command line preserving quoted strings"""
        # Simple regex to handle quoted strings
        pattern = r'"[^"]*"|[^\s]+'
        return re.findall(pattern, line)
    
    def get_commands(self) -> List[str]:
        """List available commands"""
        return list(self.commands.keys())
    
    def get_help(self, command: Optional[str] = None) -> str:
        """Get help text in period-appropriate style"""
        if command:
            cmd = command.upper()
            if cmd in self.commands:
                return f"{cmd}: {self.commands[cmd]}"
            else:
                return f"UNKNOWN COMMAND: {cmd}"
        
        # General help
        help_text = ["AVAILABLE COMMANDS:", "-" * 40]
        for cmd, desc in self.commands.items():
            help_text.append(f"{cmd:<12} - {desc}")
        help_text.append("-" * 40)
        help_text.append("TYPE 'HELP <COMMAND>' FOR DETAILED INFORMATION")
        
        return "\n".join(help_text)


class StatusCommand(CommandHandler):
    """Handle STATUS command"""
    
    def __init__(self, monitor: FileSystemAgentMonitor):
        self.monitor = monitor
    
    def execute(self, command: Command) -> str:
        """Execute STATUS [agent]"""
        if command.args:
            # Status for specific agent
            agent_name = command.args[0]
            try:
                agent = self.monitor.get_agent_status(agent_name)
                return self._format_single_status(agent)
            except Exception as e:
                return f"ERROR: Cannot retrieve status for {agent_name}"
        else:
            # Status for all agents - handled by display manager
            return ""  # Display manager will show full panel
    
    def _format_single_status(self, agent) -> str:
        """Format detailed status for single agent"""
        lines = [
            f"AGENT: {agent.name}",
            f"STATUS: {agent.status.value}",
            f"CONTEXT: {agent.context_size} lines ({agent.context_percent}% capacity)",
            f"LAST ACTIVITY: {agent.last_activity}",
            f"CURRENT TASK: {agent.current_task or 'None'}",
        ]
        if agent.session_id:
            lines.append(f"SESSION: {agent.session_id}")
        
        return "\n".join(lines)
    
    def get_description(self) -> str:
        return "Display agent status information"


class MessageCommand(CommandHandler):
    """Handle MESSAGE command"""
    
    def __init__(self, message_bus: GitMessageBus):
        self.message_bus = message_bus
    
    def execute(self, command: Command) -> str:
        """Execute MESSAGE @AGENT "content" """
        if len(command.args) < 2:
            return "USAGE: MESSAGE <AGENT> \"<CONTENT>\""
        
        to_agent = command.args[0].lstrip('@')
        content = " ".join(command.args[1:])
        
        try:
            # Send via git commit as ERA-1
            commit_hash = self.message_bus.send_message("ERA-1", to_agent, content)
            return f"MESSAGE SENT TO @{to_agent} [{commit_hash[:7]}]"
        except Exception as e:
            return f"ERROR: Failed to send message - {str(e)}"
    
    def get_description(self) -> str:
        return "Send message to an agent"


class LogCommand(CommandHandler):
    """Handle LOG command"""
    
    def __init__(self, message_bus: GitMessageBus):
        self.message_bus = message_bus
    
    def execute(self, command: Command) -> str:
        """Execute LOG [count]"""
        count = 20  # Default
        if command.args:
            try:
                count = int(command.args[0])
            except ValueError:
                return "ERROR: Count must be a number"
        
        messages = self.message_bus.get_recent_messages(count)
        if not messages:
            return "NO RECENT MESSAGES"
        
        # Format as simple log
        lines = []
        for msg in messages:
            lines.append(f"{msg.hash[:7]} {msg.content}")
        
        return "\n".join(lines)
    
    def get_description(self) -> str:
        return "Display recent system activity"


class HelpCommand(CommandHandler):
    """Handle HELP command"""
    
    def __init__(self, parser: CommandParser):
        self.parser = parser
    
    def execute(self, command: Command) -> str:
        """Execute HELP [command]"""
        if command.args:
            return self.parser.get_help(command.args[0])
        else:
            return self.parser.get_help()
    
    def get_description(self) -> str:
        return "Display help information"