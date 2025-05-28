"""
State Engine - Main orchestration for agent state management
"""

import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set

from .models import AgentState, AgentGroundState, StateDecision
from .session_monitor import SessionMonitor
from .jsonl_parser import JSONLParser
from .state_writer import StateWriter
from .prompt_generator import PromptGenerator


class StateEngine:
    """
    Main state management engine
    
    Polls session files, detects state transitions, updates _state.md files,
    and sends protocol-based prompts to agents.
    """
    
    def __init__(self, project_root: Path, sessions_dir: Path, poll_interval: int = 5):
        self.project_root = project_root
        self.sessions_dir = sessions_dir
        self.poll_interval = poll_interval
        
        # Initialize components
        self.monitor = SessionMonitor(sessions_dir)
        self.parser = JSONLParser()
        self.writer = StateWriter(project_root)
        self.prompt_gen = PromptGenerator()
        
        # Track state
        self.running = False
        self.last_poll = None
        self.errors: List[str] = []
        
        # Known agents (could be dynamic in future)
        self.known_agents = ['era-1', 'gov', 'nexus', 'critic']
    
    def start(self):
        """Start the state engine polling loop"""
        self.running = True
        print(f"State Engine starting - monitoring {self.sessions_dir}")
        
        # Ensure all agents have state files
        self.writer.ensure_state_files_exist(self.known_agents)
        
        while self.running:
            try:
                self.poll_cycle()
                time.sleep(self.poll_interval)
            except KeyboardInterrupt:
                print("\nState Engine stopped by user")
                break
            except Exception as e:
                error_msg = f"Poll cycle error: {e}"
                print(f"ERROR: {error_msg}")
                self.errors.append(error_msg)
                time.sleep(self.poll_interval)
    
    def stop(self):
        """Stop the engine"""
        self.running = False
    
    def poll_cycle(self):
        """
        Single polling cycle:
        1. Scan sessions
        2. Map agents to sessions  
        3. Check stale sessions
        4. Process state transitions
        5. Update symlinks
        """
        self.last_poll = datetime.now()
        
        # Scan all sessions
        sessions = self.monitor.scan_sessions()
        
        # Map agents to current sessions
        agent_mapping = self.monitor.map_agents_to_sessions(sessions)
        
        # Update symlinks
        self.monitor.update_symlinks(agent_mapping)
        
        # Write current_sessions.json for compatibility
        self.monitor.write_current_sessions_json(agent_mapping)
        
        # Get stale sessions (60+ seconds old)
        stale_sessions = self.monitor.get_stale_sessions(sessions)
        
        # Process each stale session
        for session in stale_sessions:
            if session.agent_name:
                self.process_agent_session(session.agent_name, session)
        
        # Check for orphaned sessions
        orphaned = self.monitor.find_orphaned_sessions(sessions)
        if orphaned:
            print(f"WARNING: {len(orphaned)} orphaned sessions found")
            for session in orphaned:
                print(f"  - {session.session_id} (size: {session.file_size} bytes)")
    
    def process_agent_session(self, agent_name: str, session):
        """
        Process a single agent's stale session
        
        1. Parse JSONL for state decision and tokens
        2. Compare with current _state.md
        3. Update state if changed
        4. Send transition prompt if needed
        """
        print(f"\nProcessing stale session for {agent_name}")
        
        # Read current state
        current_state = self.writer.read_agent_state(agent_name)
        if not current_state:
            # Create default state
            current_state = AgentGroundState()
            self.writer.write_agent_state(agent_name, current_state)
        
        # Parse session for latest state and context
        parsed = self.parser.parse_session_file(Path(session.file_path))
        
        # Extract state decision
        state_decision = parsed.get('last_state_decision')
        context_tokens = parsed.get('context_tokens')
        
        # Update context information
        state_changed = False
        
        if context_tokens and context_tokens != current_state.context_tokens:
            current_state.context_tokens = context_tokens
            current_state.context_percent = (context_tokens / current_state.max_tokens) * 100
            current_state.last_updated = datetime.now()
            state_changed = True
        
        # Update session info
        if session.session_id != current_state.session_id:
            current_state.session_id = session.session_id
            state_changed = True
        
        # Check git activity (would need separate git parsing)
        # TODO: Implement git log parsing for commit activity
        
        # Process state transition if decision found
        if state_decision:
            print(f"  Found state decision: {state_decision.next_state.value}")
            
            # Validate transition
            if self.prompt_gen.validate_transition(current_state.state, state_decision.next_state):
                # Update state
                current_state.state = state_decision.next_state
                current_state.thread = state_decision.thread
                current_state.started = state_decision.timestamp
                current_state.state_tokens = 0  # Reset for new state
                
                # Update checkpoint if provided
                if state_decision.last_read_commit:
                    current_state.last_read_commit_hash = state_decision.last_read_commit
                    current_state.last_read_commit_timestamp = datetime.now()
                
                state_changed = True
                
                # Write updated state
                if self.writer.write_agent_state(agent_name, current_state):
                    print(f"  Updated {agent_name} state to {state_decision.next_state.value}")
                    
                    # Send transition prompt
                    self.send_transition_prompt(agent_name, current_state, state_decision)
                else:
                    error_msg = f"Failed to write state for {agent_name}"
                    self.handle_error(agent_name, error_msg)
            else:
                # Invalid transition
                error_msg = (f"Invalid transition for {agent_name}: "
                           f"{current_state.state.value} -> {state_decision.next_state.value}")
                self.handle_error(agent_name, error_msg)
        elif state_changed:
            # Just update context/session info
            self.writer.write_agent_state(agent_name, current_state)
            print(f"  Updated {agent_name} context: {current_state.context_percent:.1f}%")
    
    def send_transition_prompt(self, agent_name: str, state: AgentGroundState, decision: StateDecision):
        """
        Send appropriate prompt for state transition
        
        Uses prompt generator to create protocol-based prompts
        """
        # Determine expected next state
        next_states = {
            AgentState.OFFLINE: AgentState.BOOTSTRAP,
            AgentState.BOOTSTRAP: AgentState.INBOX,
            AgentState.INBOX: AgentState.DISTILL,
            # DISTILL can go multiple places based on decision
            AgentState.DEEP_WORK: AgentState.INBOX,
            AgentState.IDLE: AgentState.INBOX,
            AgentState.LOGOUT: AgentState.OFFLINE,
        }
        
        # For DISTILL, the decision determines next state
        if state.state == AgentState.DISTILL:
            expected_next = decision.next_state
        else:
            expected_next = next_states.get(state.state)
        
        if not expected_next:
            print(f"  No transition prompt needed for {state.state.value}")
            return
        
        # Generate prompt
        context = {}
        if decision.thread:
            context['thread'] = decision.thread
        
        prompt = self.prompt_gen.generate_transition_prompt(
            agent_name,
            state.state,
            expected_next,
            context
        )
        
        if prompt:
            print(f"  Sending prompt: {prompt}")
            # TODO: Actual prompt sending mechanism
            # For now, just log it
            self.log_prompt(agent_name, prompt)
    
    def handle_error(self, agent_name: str, error: str):
        """
        Handle state transition errors
        
        Per requirements: lock agent state and escalate to admin
        """
        print(f"ERROR: {error}")
        self.errors.append(f"{datetime.now()}: {error}")
        
        # Send error prompt
        error_prompt = self.prompt_gen.get_error_prompt(agent_name, error)
        print(f"  Escalating: {error_prompt}")
        self.log_prompt(agent_name, error_prompt)
        
        # TODO: Lock agent state (prevent further transitions)
        # This would require adding a 'locked' flag to AgentGroundState
    
    def log_prompt(self, agent_name: str, prompt: str):
        """
        Log prompt for debugging/audit
        
        In production, this would actually send the prompt to the agent
        """
        log_file = self.project_root / "state_engine_prompts.log"
        
        with open(log_file, 'a') as f:
            f.write(f"{datetime.now().isoformat()} | {agent_name} | {prompt}\n")
    
    def get_status(self) -> Dict:
        """Get current engine status"""
        agent_states = {}
        
        for agent_name in self.known_agents:
            state = self.writer.read_agent_state(agent_name)
            if state:
                agent_states[agent_name] = {
                    'state': state.state.value,
                    'thread': state.thread,
                    'context_percent': state.context_percent,
                    'session_id': state.session_id,
                    'last_updated': state.last_updated.isoformat() if state.last_updated else None
                }
        
        return {
            'running': self.running,
            'last_poll': self.last_poll.isoformat() if self.last_poll else None,
            'agents': agent_states,
            'errors': self.errors[-10:]  # Last 10 errors
        }


# Standalone entry point
if __name__ == "__main__":
    import sys
    
    # Default paths
    project_root = Path("/home/daniel/prj/rtfw")
    sessions_dir = project_root / "_sessions"
    
    # Allow override via command line
    if len(sys.argv) > 1:
        project_root = Path(sys.argv[1])
    if len(sys.argv) > 2:
        sessions_dir = Path(sys.argv[2])
    
    # Create and start engine
    engine = StateEngine(project_root, sessions_dir)
    
    try:
        engine.start()
    except KeyboardInterrupt:
        print("\nShutting down...")
        engine.stop()