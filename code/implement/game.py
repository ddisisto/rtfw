#!/usr/bin/env python3
"""
RTFW Game Core
Core game mechanics and state management for RTFW
"""

class GameState:
    """Manages the state of the RTFW game"""
    
    def __init__(self):
        """Initialize a new game state"""
        # Current era (0=Foundation, 1=Learning, 2=Integration, 3=Emergence)
        self.era = 0
        
        # Base resources
        self.resources = {
            "funding": 100,
            "talent": 5,
            "compute": 10,
            "data": 20,
        }
        
        # Active research areas
        self.research_areas = {
            "rule_based_systems": {"progress": 0, "breakthrough": 10},
            "neural_networks": {"progress": 0, "breakthrough": 20},
            "expert_systems": {"progress": 0, "breakthrough": 15},
            "knowledge_representation": {"progress": 0, "breakthrough": 12},
        }
        
        # Current research focus
        self.research_focus = None
        
        # Active projects
        self.projects = [
            {"name": "Basic Pattern Recognition", "status": "In Progress", "progress": 0, "complete": 10}
        ]
        
        # Meta-game unlocks
        self.unlocked_agents = []
        
    def get_research_areas(self):
        """Get available research areas for the current era"""
        return list(self.research_areas.keys())
        
    def focus_research(self, area):
        """Set focus to a specific research area"""
        if area in self.research_areas:
            self.research_focus = area
            return True
        return False
        
    def get_research_report(self):
        """Generate a report on current research status"""
        report = "Research Status:\n"
        for area, data in self.research_areas.items():
            focus = " (FOCUS)" if area == self.research_focus else ""
            report += f"- {area}{focus}: {data['progress']}/{data['breakthrough']} progress\n"
        return report
        
    def attempt_breakthrough(self, area):
        """Attempt a research breakthrough"""
        if area not in self.research_areas:
            return False
            
        # Simple probability check based on progress
        import random
        chance = self.research_areas[area]["progress"] / self.research_areas[area]["breakthrough"]
        if random.random() < chance:
            self.research_areas[area]["progress"] = self.research_areas[area]["breakthrough"]
            return True
        
        # Increment progress even on failure
        self.research_areas[area]["progress"] += 1
        return False
        
    def get_resources(self):
        """Get current resource levels"""
        return self.resources
        
    def get_projects(self):
        """Get list of active projects"""
        return self.projects
        
    def unlock_meta_command(self, agent):
        """Unlock a meta-game agent command"""
        if agent not in self.unlocked_agents:
            self.unlocked_agents.append(agent)
        
    def query_agent(self, agent, query):
        """Send a query to a meta-game agent"""
        # In a real implementation, this would connect to the agent system
        responses = {
            "historian": f"HISTORIAN: {query} relates to early developments in symbolic AI during the 1960s...",
            "research": f"RESEARCH: Current state-of-art for {query} involves transformer architectures...",
            "gamedesign": f"GAMEDESIGN: {query} could be implemented as a resource management mechanic...",
        }
        
        return responses.get(agent, f"Agent {agent} has no response for '{query}'")