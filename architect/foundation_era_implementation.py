#!/usr/bin/env python3
"""
Foundation Era Game Mechanics Implementation
Integrates with @NEXUS session management for RTFW gameplay
"""

class FoundationEraState:
    """Manages Foundation Era game state and progression"""
    
    def __init__(self):
        # Core resources aligned with @RESEARCH taxonomy
        self.resources = {
            "funding": 1000,
            "talent": 10,
            "compute": 50,
            "data": 25
        }
        
        # Research areas from @RESEARCH Foundation Era taxonomy
        self.research_areas = {
            "rule_based_systems": {
                "progress": 0,
                "breakthrough_threshold": 100,
                "description": "Logic programming and expert systems foundations",
                "historical_context": "1956-1980s symbolic AI development"
            },
            "early_neural_networks": {
                "progress": 0,
                "breakthrough_threshold": 120,
                "description": "Perceptron development and early connectionism",
                "historical_context": "1950s-1980s neural network research"
            },
            "expert_systems": {
                "progress": 0,
                "breakthrough_threshold": 90,
                "description": "Knowledge engineering and domain-specific reasoning",
                "historical_context": "1970s-1990s commercial AI applications"
            },
            "knowledge_representation": {
                "progress": 0,
                "breakthrough_threshold": 80,
                "description": "Semantic networks, frames, and ontologies",
                "historical_context": "1960s-1990s AI knowledge structures"
            }
        }
        
        # Fourth wall progression tracking
        self.fourth_wall_level = 0
        self.unlocked_commands = ["research", "status", "resources", "projects"]
        self.discovered_agents = []
        
        # Projects representing milestones
        self.active_projects = []
        self.completed_projects = []
        
        # Agent interaction tracking
        self.agent_interactions = 0
        self.direct_agent_access = False
        
    def allocate_resources(self, area, funding=0, talent=0, compute=0, data=0):
        """Allocate resources to research area via @NEXUS routing"""
        if area not in self.research_areas:
            return False, f"Unknown research area: {area}"
            
        # Check resource availability
        if (self.resources["funding"] < funding or 
            self.resources["talent"] < talent or
            self.resources["compute"] < compute or
            self.resources["data"] < data):
            return False, "Insufficient resources"
            
        # Deduct resources
        self.resources["funding"] -= funding
        self.resources["talent"] -= talent
        self.resources["compute"] -= compute
        self.resources["data"] -= data
        
        # Calculate progress increase
        progress_increase = (funding * 0.1 + talent * 5 + compute * 2 + data * 3)
        self.research_areas[area]["progress"] += progress_increase
        
        # Check for breakthrough
        breakthrough = self.check_breakthrough(area)
        
        return True, {
            "progress_increase": progress_increase,
            "new_progress": self.research_areas[area]["progress"],
            "breakthrough": breakthrough
        }
    
    def check_breakthrough(self, area):
        """Check if research area has achieved breakthrough"""
        area_data = self.research_areas[area]
        if area_data["progress"] >= area_data["breakthrough_threshold"]:
            # Trigger fourth wall progression
            self.trigger_fourth_wall_progression()
            return True
        return False
    
    def trigger_fourth_wall_progression(self):
        """Handle fourth wall mechanic progression"""
        breakthroughs = sum(1 for area in self.research_areas.values() 
                          if area["progress"] >= area["breakthrough_threshold"])
        
        # Level progression based on breakthroughs
        if breakthroughs >= 1 and self.fourth_wall_level < 1:
            self.fourth_wall_level = 1
            self.unlocked_commands.extend(["nexus", "agents"])
            return "DISCOVERY: You've unlocked agent status commands!"
            
        elif breakthroughs >= 2 and self.fourth_wall_level < 2:
            self.fourth_wall_level = 2
            self.unlocked_commands.extend(["query"])
            self.discovered_agents = ["@RESEARCH", "@HISTORIAN"]
            return "DISCOVERY: Specialist agents detected in the system!"
            
        elif breakthroughs >= 3 and self.fourth_wall_level < 3:
            self.fourth_wall_level = 3
            self.unlocked_commands.extend(["direct"])
            return "DISCOVERY: Direct agent communication unlocked!"
            
        return None
    
    def get_status_report(self):
        """Generate comprehensive status report for @ADMIN"""
        report = {
            "era": "Foundation (1950s-2010s)",
            "resources": self.resources.copy(),
            "research_progress": {},
            "fourth_wall_level": self.fourth_wall_level,
            "available_commands": self.unlocked_commands.copy(),
            "discovered_agents": self.discovered_agents.copy()
        }
        
        # Calculate research progress percentages
        for area, data in self.research_areas.items():
            progress_pct = min(100, (data["progress"] / data["breakthrough_threshold"]) * 100)
            report["research_progress"][area] = {
                "progress_percent": round(progress_pct, 1),
                "breakthrough_achieved": data["progress"] >= data["breakthrough_threshold"],
                "description": data["description"]
            }
        
        return report
    
    def check_era_transition(self):
        """Check if conditions met for Learning Era transition"""
        breakthroughs = sum(1 for area in self.research_areas.values() 
                          if area["progress"] >= area["breakthrough_threshold"])
        
        fourth_wall_complete = self.fourth_wall_level >= 3
        agent_familiarity = self.agent_interactions >= 10
        
        if breakthroughs >= 3 and fourth_wall_complete and agent_familiarity:
            return True, "Ready for Learning Era transition"
        
        missing = []
        if breakthroughs < 3:
            missing.append(f"Need {3 - breakthroughs} more research breakthroughs")
        if not fourth_wall_complete:
            missing.append("Must unlock direct agent communication")
        if not agent_familiarity:
            missing.append(f"Need {10 - self.agent_interactions} more agent interactions")
            
        return False, "Missing requirements: " + ", ".join(missing)


class FoundationEraCommands:
    """Command handlers for Foundation Era CLI integration"""
    
    def __init__(self, game_state):
        self.state = game_state
    
    def cmd_research(self, args):
        """Handle research allocation commands"""
        if not args:
            return self._show_research_areas()
        
        # Parse command: research [area] [funding] [talent] [compute] [data]
        parts = args.split()
        if len(parts) < 2:
            return "Usage: research [area] [funding] [talent] [compute] [data]"
        
        area = parts[0]
        try:
            funding = int(parts[1]) if len(parts) > 1 else 0
            talent = int(parts[2]) if len(parts) > 2 else 0
            compute = int(parts[3]) if len(parts) > 3 else 0
            data = int(parts[4]) if len(parts) > 4 else 0
        except ValueError:
            return "Resource allocations must be numbers"
        
        success, result = self.state.allocate_resources(area, funding, talent, compute, data)
        
        if success:
            response = f"Resources allocated to {area}. Progress increased by {result['progress_increase']:.1f}"
            if result['breakthrough']:
                response += "\n*** BREAKTHROUGH ACHIEVED! ***"
                progression = self.state.trigger_fourth_wall_progression()
                if progression:
                    response += f"\n{progression}"
            return response
        else:
            return f"Error: {result}"
    
    def _show_research_areas(self):
        """Display available research areas"""
        output = "Foundation Era Research Areas:\n"
        for area, data in self.state.research_areas.items():
            progress_pct = (data["progress"] / data["breakthrough_threshold"]) * 100
            breakthrough = "✓" if data["progress"] >= data["breakthrough_threshold"] else " "
            output += f"[{breakthrough}] {area}: {progress_pct:.1f}% - {data['description']}\n"
        return output
    
    def cmd_nexus(self, args):
        """Handle NEXUS meta-commands (unlocked via fourth wall progression)"""
        if "nexus" not in self.state.unlocked_commands:
            return "Unknown command. Type 'help' for available commands."
        
        if not args:
            return "NEXUS commands: agents, status, query"
        
        subcommand = args.split()[0]
        
        if subcommand == "agents":
            return self._show_agents()
        elif subcommand == "status":
            return self._show_nexus_status()
        elif subcommand == "query":
            return self._handle_agent_query(args)
        else:
            return f"Unknown NEXUS command: {subcommand}"
    
    def _show_agents(self):
        """Show discovered agent information"""
        if not self.state.discovered_agents:
            return "No specialist agents discovered yet. Continue research to unlock."
        
        output = "Discovered Specialist Agents:\n"
        for agent in self.state.discovered_agents:
            output += f"- {agent}: Available for consultation\n"
        return output
    
    def _show_nexus_status(self):
        """Show NEXUS system status"""
        return f"""NEXUS System Status:
Fourth Wall Level: {self.state.fourth_wall_level}/5
Agent Interactions: {self.state.agent_interactions}
Direct Access: {'Enabled' if self.state.direct_agent_access else 'Locked'}
Discovered Agents: {len(self.state.discovered_agents)}"""
    
    def _handle_agent_query(self, args):
        """Route query to appropriate agent via @NEXUS"""
        # This would integrate with actual @NEXUS message routing
        self.state.agent_interactions += 1
        return "Agent query routed via @NEXUS. Response pending..."


# Integration point for @NEXUS message routing
def route_to_foundation_era(command, args, game_state):
    """Route commands to Foundation Era handlers"""
    commands = FoundationEraCommands(game_state)
    
    if command == "research":
        return commands.cmd_research(args)
    elif command == "nexus":
        return commands.cmd_nexus(args)
    elif command == "status":
        return game_state.get_status_report()
    else:
        return None  # Command not handled by Foundation Era