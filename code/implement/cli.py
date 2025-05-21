#!/usr/bin/env python3
"""
RTFW CLI Interface
A command-line interface for the Riding The Fourth Wall game
"""

import cmd
import sys
import os
from game import GameState

class RTFWCLI(cmd.Cmd):
    """Command processor for RTFW game"""
    
    intro = """
NEXUS v0.1 (Alpha)
A recursive journey into artificial intelligence
----------------------------------------------
> You have connected to NEXUS terminal.
> Type 'help' to begin.
"""
    prompt = 'NEXUS> '
    
    def __init__(self):
        super().__init__()
        self.game_state = GameState()
        
    def do_research(self, arg):
        """
        Research command: Investigate AI development areas
        Usage: research [topic]
               research list - Show available research areas
               research focus [area] - Allocate resources to specific research
               research report - Get current research status
               research breakthrough [area] - Attempt to accelerate progress
        """
        args = arg.split()
        if not args:
            print("What would you like to research?")
            return
            
        if args[0] == "list":
            areas = self.game_state.get_research_areas()
            print("Available research areas:")
            for area in areas:
                print(f"- {area}")
        elif args[0] == "focus" and len(args) > 1:
            area = args[1]
            success = self.game_state.focus_research(area)
            if success:
                print(f"Research focus shifted to {area}")
            else:
                print(f"Cannot focus research on {area}")
        elif args[0] == "report":
            report = self.game_state.get_research_report()
            print(report)
        elif args[0] == "breakthrough" and len(args) > 1:
            area = args[1]
            success = self.game_state.attempt_breakthrough(area)
            if success:
                print(f"Breakthrough achieved in {area}!")
            else:
                print(f"Breakthrough attempt in {area} failed.")
        else:
            print("Unknown research command. Try 'help research'")
    
    def do_resources(self, arg):
        """
        Show current resource levels
        """
        resources = self.game_state.get_resources()
        print("Current resources:")
        for name, amount in resources.items():
            print(f"- {name}: {amount}")
    
    def do_allocate(self, arg):
        """
        Allocate resources to projects
        Usage: allocate [amount] [resource] to [project]
        """
        # Implementation here
        print("Resource allocation updated")
    
    def do_projects(self, arg):
        """
        List active projects
        """
        projects = self.game_state.get_projects()
        print("Active projects:")
        for project in projects:
            print(f"- {project['name']}: {project['status']}")
    
    def do_discover(self, arg):
        """Hidden command to discover meta-features"""
        if arg == "hidden_systems":
            print("SYSTEM: You've discovered the developer interface!")
            print("NEW COMMAND UNLOCKED: @historian")
            self.game_state.unlock_meta_command("historian")
        else:
            print("Nothing unusual discovered.")
    
    def default(self, line):
        """Handle meta-commands"""
        if line.startswith('@'):
            parts = line[1:].split(None, 1)
            agent = parts[0]
            query = parts[1] if len(parts) > 1 else ""
            
            if agent in self.game_state.unlocked_agents:
                print(f"Accessing {agent.upper()} agent interface...")
                response = self.game_state.query_agent(agent, query)
                print(response)
            else:
                print(f"Unknown command or agent: {line}")
                return
        else:
            print(f"Unknown command: {line}")
    
    def do_exit(self, arg):
        """Exit the RTFW CLI"""
        print("Disconnecting from NEXUS terminal...")
        return True
        
    def do_quit(self, arg):
        """Exit the RTFW CLI"""
        return self.do_exit(arg)
        
    do_EOF = do_quit

if __name__ == '__main__':
    RTFWCLI().cmdloop()