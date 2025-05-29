"""
Simplified State Engine - Works with known agent symlinks only
"""

import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

from .models import AgentState, AgentGroundState
from .session_monitor import SessionMonitor
from .jsonl_parser import JSONLParser
from .state_writer import StateWriter
from .prompt_generator import PromptGenerator
from .git_monitor import GitMonitor
from .logout_handler import LogoutHandler
from .tmux_handler import TmuxHandler


class StateEngine:
    """
    Simplified state management engine
    
    Only processes the 4 known agent symlinks.
    Throws exceptions for any unexpected conditions.
    """
    
    def __init__(self, project_root: Path, sessions_dir: Path, poll_interval: int = 1):
        self.project_root = project_root
        self.sessions_dir = sessions_dir
        self.poll_interval = poll_interval
        
        # Initialize components
        self.monitor = SessionMonitor(sessions_dir)
        self.parser = JSONLParser()
        self.writer = StateWriter(project_root)
        self.prompt_gen = PromptGenerator()
        self.git = GitMonitor(project_root)
        self.logout_handler = LogoutHandler(project_root, sessions_dir)
        
        # Track state
        self.running = False
        self.last_poll = None
        self.errors = []
        
    def start(self):
        """Start the state engine polling loop"""
        self.running = True
        print(f"State Engine starting - monitoring {self.sessions_dir}")
        
        while self.running:
            try:
                self.poll_cycle()
                time.sleep(self.poll_interval)
            except KeyboardInterrupt:
                print("\nState Engine stopped by user")
                self.running = False
            except Exception as e:
                error_msg = f"Poll cycle error: {e}"
                print(f"ERROR: {error_msg}")
                self.errors.append(error_msg)
                # Re-raise to fail fast
                raise
    
    def poll_cycle(self):
        """
        Single polling cycle - check all agents and update states
        
        Raises exceptions for any unexpected conditions.
        """
        self.last_poll = datetime.now()
        
        # Get current sessions from symlinks
        sessions = self.monitor.scan_sessions()
        
        # Process each agent
        for agent_name, session_info in sessions.items():
            try:
                self.process_agent(agent_name, session_info)
            except Exception as e:
                error_msg = f"Error processing {agent_name}: {e}"
                print(f"ERROR: {error_msg}")
                self.errors.append(error_msg)
                # Re-raise to fail fast
                raise
    
    def process_agent(self, agent_name: str, session_info):
        """
        Process a single agent's session
        
        Two-tier approach:
        1. ALWAYS update: context, git info, unread messages
        2. ONLY when idle: state transitions and thread changes
        """
        print(f"\nProcessing {agent_name}:")
        print(f"  Session: {session_info.session_id}")
        print(f"  File: {Path(session_info.file_path).name}")
        
        # Read current state first
        current_state = self.writer.read_agent_state(agent_name)
        if not current_state:
            current_state = AgentGroundState()
        
        # ALWAYS update context usage first (needed for state transitions)
        context_info = self.parser.parse_context_usage(Path(session_info.file_path))
        
        # Store the OLD commit hash before updating
        old_commit_hash = current_state.last_write_commit_hash if current_state else None
        
        # Check for state changes in git commits using OLD hash
        # This captures states announced via commit messages
        git_state = self.git.get_agent_state_from_commits(
            agent_name,
            old_commit_hash
        )
        
        if git_state:
            state_str, thread, commit_hash = git_state
            print(f"  Found state in git commit: {state_str} (commit: {commit_hash[:7]})")
            
            # Map string to enum
            state_map = {
                'bootstrap': AgentState.BOOTSTRAP,
                'inbox': AgentState.INBOX,
                'distill': AgentState.DISTILL,
                'deep_work': AgentState.DEEP_WORK,
                'idle': AgentState.IDLE,
                'logout': AgentState.LOGOUT,
                'direct_io': AgentState.DIRECT_IO,
                'offline': AgentState.OFFLINE,
            }
            
            new_state = state_map.get(state_str)
            if new_state and new_state != current_state.state:
                print(f"  Git-based state transition: {current_state.state.value} -> {new_state.value}")
                
                # Update last_read_commit when EXITING inbox state (check BEFORE updating state)
                # Exception: Skip if transitioning to direct_io (likely skipped inbox)
                if (current_state.state == AgentState.INBOX and 
                    new_state != AgentState.INBOX and 
                    new_state != AgentState.DIRECT_IO):
                    current_state.last_read_commit_hash = commit_hash
                    current_state.last_read_commit_timestamp = self.git.get_commit_timestamp(commit_hash)
                    current_state.unread_message_count = 0  # Reset unread count
                    print(f"  Exiting inbox: Updated last_read to {commit_hash[:7]}, reset unread count")
                
                # Now update the state
                current_state.state = new_state
                current_state.thread = thread
                current_state.started = datetime.now()
                # Context snapshot
                if context_info:
                    current_state.context_tokens_at_entry = context_info['used']
                
                # Handle logout → bootstrap automation
                if new_state == AgentState.LOGOUT:
                    print(f"  LOGOUT detected for {agent_name}")
                    # Reset context tokens to 0
                    current_state.context_tokens = 0
                    current_state.context_percent = 0.0
                    # Set offline as expected next state
                    current_state.expected_next_state = AgentState.OFFLINE
                    # Write state immediately before triggering logout
                    self.writer.write_agent_state(agent_name, current_state)
                    
                    # Trigger logout handler
                    tmux_session = agent_name  # Tmux session name is just agent name (e.g. 'era-1')
                    if self.logout_handler.check_tmux_session_exists(tmux_session):
                        print(f"  Triggering logout handler for {tmux_session}")
                        success = self.logout_handler.handle_logout(agent_name, tmux_session)
                        if success:
                            # Update state to offline → bootstrap
                            current_state.state = AgentState.OFFLINE
                            current_state.expected_next_state = AgentState.BOOTSTRAP
                            current_state.session_id = None  # Will be updated on next poll
                    else:
                        print(f"  WARNING: No tmux session '{tmux_session}' found")
        
        # Update context usage in current_state (needed for all states)
        if context_info:
            current_state.context_tokens = context_info['used']
            current_state.max_context_tokens = context_info['max']
            current_state.context_percent = context_info['percent']
            print(f"  Context: {context_info['percent']:.1f}% ({context_info['used']}/{context_info['max']})")
        
        # ALWAYS update git info (moved before direct_io check)
        last_commit = self.git.get_last_agent_commit(agent_name)
        if last_commit:
            current_state.last_write_commit_hash = last_commit.hash
            current_state.last_write_commit_timestamp = last_commit.timestamp
            print(f"  Last commit: {last_commit.hash[:7]} at {last_commit.timestamp}")
            
            # Count unread messages based on last read commit
            if current_state.last_read_commit_hash:
                unread_count = self.git.count_unread_messages(agent_name, current_state.last_read_commit_hash)
                current_state.unread_message_count = unread_count
                print(f"  Unread messages: {unread_count}")
        
        # Skip further processing if agent is in direct_io state
        if current_state.state == AgentState.DIRECT_IO:
            print(f"  Agent in DIRECT_IO state - skipping automated transitions")
            # Update session and write state
            current_state.session_id = session_info.session_id
            current_state.last_updated = datetime.now()
            self.writer.write_agent_state(agent_name, current_state)
            return
        
        # Context and git info already updated above
        
        # ALWAYS update session and timestamps
        current_state.session_id = session_info.session_id
        current_state.last_updated = datetime.now()
        
        # ONLY update state/thread if session is idle
        if session_info.is_stale:
            print(f"  Session is idle - checking for state transitions")
            
            try:
                decisions = self.parser.parse_state_decisions(Path(session_info.file_path))
                
                if decisions:
                    latest = decisions[-1]
                    print(f"  Found state decision: {latest.state.value}")
                    
                    # Check if state actually changed
                    state_changed = (current_state.state != latest.state or
                                   current_state.thread != latest.thread)
                    
                    if state_changed:
                        print(f"  State transition detected!")
                        print(f"    From: {current_state.state.value}")
                        print(f"    To: {latest.state.value}")
                        
                        # Update state fields
                        current_state.state = latest.state
                        current_state.thread = latest.thread
                        current_state.started = latest.timestamp
                        current_state.expected_next_state = latest.expected_next_state
                        
                        # Snapshot context at state entry
                        if context_info:
                            current_state.context_tokens_at_entry = context_info['used']
                        
                        # Update last read commit if provided
                        if latest.last_read_commit:
                            current_state.last_read_commit_hash = latest.last_read_commit
                            current_state.last_read_commit_timestamp = datetime.now()
                        
                        # Generate transition prompt
                        prompt = self.prompt_gen.generate_prompt(
                            agent_name,
                            current_state.state if current_state else None,
                            latest.state,
                            current_state
                        )
                        
                        if prompt:
                            print(f"  Generated prompt: {prompt[:100]}...")
                            # TODO: Send prompt via stdin when connected
                else:
                    print(f"  No state decision in last output - keeping current state")
            
            except Exception as e:
                print(f"  Warning: Could not parse state decision: {e}")
                print(f"  Keeping current state: {current_state.state.value}")
        else:
            print(f"  Session active - metadata updated, state unchanged")
        
        # Always write updated state
        self.writer.write_agent_state(agent_name, current_state)
        print(f"  Updated _state.md")
    
    def stop(self):
        """Stop the state engine"""
        self.running = False