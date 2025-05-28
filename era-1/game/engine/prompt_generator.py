"""
Prompt Generator - Creates protocol-based prompts for state transitions
"""

from pathlib import Path
from typing import Optional, Dict

from .models import AgentState


class PromptGenerator:
    """
    Generates prompts for agent state transitions based on protocols
    
    Prompt format follows @ADMIN's specification:
    - Bootstrap: "apply protocols/bootstrap.md for agent @AGENT.md, in @agent/_state.md"
    - Others: "please proceed to [state] state per protocols/[protocol].md"
    """
    
    # Map states to protocol files
    STATE_PROTOCOLS = {
        AgentState.BOOTSTRAP: "bootstrap.md",
        AgentState.INBOX: "inbox.md",  # TODO: Create this protocol
        AgentState.DISTILL: "distill.md",
        AgentState.DEEP_WORK: "deep-work.md",  # TODO: Create this protocol
        AgentState.IDLE: "idle.md",  # TODO: Create this protocol
        AgentState.LOGOUT: "logout.md",  # TODO: Create this protocol
    }
    
    def generate_transition_prompt(
        self, 
        agent_name: str, 
        from_state: AgentState, 
        to_state: AgentState,
        context: Optional[Dict] = None
    ) -> Optional[str]:
        """
        Generate appropriate prompt for state transition
        
        Args:
            agent_name: Name of agent (e.g., 'era-1', 'gov')
            from_state: Current state
            to_state: Target state
            context: Optional context (thread name, etc.)
            
        Returns:
            Prompt string or None if transition not valid
        """
        # Special case: offline -> bootstrap
        if from_state == AgentState.OFFLINE and to_state == AgentState.BOOTSTRAP:
            return self._generate_bootstrap_prompt(agent_name)
        
        # Check if we have a protocol for target state
        if to_state not in self.STATE_PROTOCOLS:
            return None
        
        # Standard transition prompt
        protocol = self.STATE_PROTOCOLS[to_state]
        
        # Check if protocol file exists (for validation)
        # TODO: Some protocols don't exist yet, so we note them
        protocol_path = Path(f"protocols/{protocol}")
        protocol_exists = protocol_path.exists()
        
        if not protocol_exists and protocol != "bootstrap.md":
            # For missing protocols, use generic format
            # TODO: Create these protocols
            return f"@ADMIN: please proceed to {to_state.value} state [protocol {protocol} pending]"
        
        # Generate standard prompt
        prompt = f"@ADMIN: please proceed to {to_state.value} state per protocols/{protocol}"
        
        # Add context if relevant
        if context:
            if 'thread' in context and context['thread']:
                prompt += f" [thread: {context['thread']}]"
            if 'reason' in context:
                prompt += f" [{context['reason']}]"
        
        return prompt
    
    def _generate_bootstrap_prompt(self, agent_name: str) -> str:
        """Generate bootstrap prompt with exact format"""
        # Convert agent name to proper format (era-1 -> ERA-1)
        agent_upper = agent_name.upper()
        
        return f"@ADMIN: apply protocols/bootstrap.md for agent @{agent_upper}.md, in @{agent_name}/_state.md"
    
    def validate_transition(self, from_state: AgentState, to_state: AgentState) -> bool:
        """
        Validate if a state transition is allowed
        
        Based on lifecycle protocol state machine
        """
        valid_transitions = {
            AgentState.OFFLINE: [AgentState.BOOTSTRAP],
            AgentState.BOOTSTRAP: [AgentState.INBOX],
            AgentState.INBOX: [AgentState.DISTILL],
            AgentState.DISTILL: [AgentState.DEEP_WORK, AgentState.IDLE, AgentState.LOGOUT],
            AgentState.DEEP_WORK: [AgentState.INBOX],
            AgentState.IDLE: [AgentState.INBOX],
            AgentState.LOGOUT: [AgentState.OFFLINE],
            AgentState.DIRECT_IO: [AgentState.INBOX],  # Admin can return to any state
        }
        
        allowed = valid_transitions.get(from_state, [])
        return to_state in allowed
    
    def get_error_prompt(self, agent_name: str, error: str) -> str:
        """
        Generate error prompt for manual intervention
        
        Used when invalid transitions or errors occur
        """
        return f"@ADMIN: ERROR in {agent_name} state management - {error}. Manual review required."
    
    def get_missing_protocol_list(self) -> list:
        """
        Return list of protocols that need to be created
        
        Useful for tracking implementation progress
        """
        missing = []
        
        for state, protocol in self.STATE_PROTOCOLS.items():
            protocol_path = Path(f"protocols/{protocol}")
            if not protocol_path.exists() and protocol != "bootstrap.md":
                missing.append((state.value, protocol))
        
        return missing