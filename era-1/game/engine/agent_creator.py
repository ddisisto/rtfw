"""
Agent Creator - Handles new agent session creation

Extracted from LogoutHandler for reuse in:
- Logout → Bootstrap automation
- Manual agent creation by admin
- Future agent spawning scenarios
"""

import time
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime

from .tmux_handler import TmuxHandler


class AgentCreator:
    """
    Handles creation of new agent sessions
    
    Provides step-by-step methods for:
    1. Creating tmux window
    2. Starting Claude CLI
    3. Capturing session info
    4. Creating symlinks
    5. Initializing state
    """
    
    def __init__(self, project_root: Path, sessions_dir: Path):
        self.project_root = project_root
        self.sessions_dir = sessions_dir
        self.tmux = TmuxHandler()
    
    def create_tmux_window(self, agent_name: str) -> bool:
        """
        Step 1: Create new tmux window for agent
        
        Args:
            agent_name: Name for the window (e.g., 'test-agent')
            
        Returns:
            True if successful
        """
        try:
            # Create new window with bash
            cmd = ['tmux', 'new-window', '-n', agent_name, 'bash']
            import subprocess
            subprocess.run(cmd, check=True)
            print(f"✓ Created tmux window: {agent_name}")
            return True
        except Exception as e:
            print(f"✗ Failed to create window: {e}")
            return False
    
    def verify_bash_ready(self, agent_name: str) -> bool:
        """
        Step 2: Verify bash is ready in the window
        
        Args:
            agent_name: Tmux window name
            
        Returns:
            True if bash prompt detected
        """
        try:
            # Capture pane content
            result = subprocess.run(
                ['tmux', 'capture-pane', '-t', agent_name, '-p'],
                capture_output=True,
                text=True
            )
            
            content = result.stdout
            # Look for bash prompt indicators
            if '$' in content or '#' in content or 'bash' in content.lower():
                print(f"✓ Bash ready in {agent_name}")
                return True
            else:
                print(f"✗ No bash prompt detected")
                return False
                
        except Exception as e:
            print(f"✗ Failed to capture pane: {e}")
            return False
    
    def start_claude_cli(self, agent_name: str) -> bool:
        """
        Step 3: Start Claude CLI in the window
        
        Args:
            agent_name: Tmux window name
            
        Returns:
            True if successful
        """
        print(f"Starting Claude CLI in {agent_name}...")
        return self.tmux.start_claude_session(agent_name)
    
    def send_status_command(self, agent_name: str) -> bool:
        """
        Step 4: Send /status command and capture
        
        Args:
            agent_name: Tmux window name
            
        Returns:
            True if successful
        """
        print("Sending /status command...")
        success = self.tmux.send_claude_command(agent_name, "/status", wait_after=2.0)
        
        if success:
            # Close status display
            print("Closing status display...")
            self.tmux.send_key(agent_name, "Enter")
            time.sleep(1)
            
        return success
    
    def find_new_session(self, before_files: set[Path], timeout: int = 10) -> Optional[Path]:
        """
        Step 5: Find the newly created session file
        
        Args:
            before_files: Set of files that existed before
            timeout: Max seconds to wait
            
        Returns:
            Path to new session file or None
        """
        print("Looking for new session file...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            current = set(self.sessions_dir.glob("*.jsonl"))
            new_files = current - before_files
            
            if new_files:
                newest = max(new_files, key=lambda p: p.stat().st_mtime)
                print(f"✓ Found new session: {newest.name}")
                return newest
            
            time.sleep(0.5)
        
        print("✗ No new session file found")
        return None
    
    def create_symlink(self, agent_name: str, session_file: Path) -> bool:
        """
        Step 6: Create symlink for the agent
        
        Args:
            agent_name: Agent name (e.g., 'test-agent')
            session_file: Path to session JSONL file
            
        Returns:
            True if successful
        """
        try:
            # Format symlink name (uppercase)
            symlink_name = f"{agent_name.upper()}_current.jsonl"
            symlink_path = self.sessions_dir / symlink_name
            
            # Remove if exists
            if symlink_path.exists():
                symlink_path.unlink()
            
            # Create new symlink
            symlink_path.symlink_to(session_file.name)
            print(f"✓ Created symlink: {symlink_name} -> {session_file.name}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to create symlink: {e}")
            return False
    
    def initialize_state(self, agent_name: str) -> bool:
        """
        Step 7: Initialize agent state file
        
        Args:
            agent_name: Agent name
            
        Returns:
            True if successful
        """
        try:
            # Create agent directory
            agent_dir = self.project_root / agent_name
            agent_dir.mkdir(exist_ok=True)
            
            # Create initial _state.md
            state_file = agent_dir / "_state.md"
            state_content = f"""# {agent_name.upper()} Ground State [READ-ONLY]
# CRITICAL: This file is maintained by the game engine
# DO NOT EDIT - Read for objective truth only
# COMMIT this file with your workspace
# Format Version: 1.0

## Git Activity
last_read_commit_hash: HEAD
last_read_commit_timestamp: {datetime.now().isoformat()}
last_write_commit_hash: 
last_write_commit_timestamp: 

## Context Window
session_id: pending
context_tokens: 0
max_context_tokens: 128000
context_percent: 0.0%
last_updated: {datetime.now().isoformat()}

## Last Observed Agent State
state: offline
thread: *
started: {datetime.now().isoformat()}
context_tokens_at_entry: 0
expected_next_state: bootstrap
unread_message_count: 0
"""
            
            with open(state_file, 'w') as f:
                f.write(state_content)
            
            print(f"✓ Created initial state file: {state_file}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to initialize state: {e}")
            return False
    
    def full_agent_creation(self, agent_name: str) -> Tuple[bool, Optional[Path]]:
        """
        Perform full agent creation sequence
        
        Args:
            agent_name: Name for the new agent
            
        Returns:
            (success, session_file_path)
        """
        print(f"\n=== CREATING AGENT: {agent_name} ===\n")
        
        # Track existing files
        before_files = set(self.sessions_dir.glob("*.jsonl"))
        
        # Step 1: Create tmux window
        if not self.create_tmux_window(agent_name):
            return False, None
        
        time.sleep(0.5)
        
        # Step 2: Verify bash
        if not self.verify_bash_ready(agent_name):
            return False, None
        
        # Step 3: Start Claude
        if not self.start_claude_cli(agent_name):
            return False, None
        
        # Step 4: Send /status
        if not self.send_status_command(agent_name):
            return False, None
        
        # Step 5: Find new session
        session_file = self.find_new_session(before_files)
        if not session_file:
            return False, None
        
        # Step 6: Create symlink
        if not self.create_symlink(agent_name, session_file):
            return False, session_file
        
        # Step 7: Initialize state
        if not self.initialize_state(agent_name):
            return False, session_file
        
        print(f"\n=== AGENT CREATION COMPLETE ===")
        print(f"Agent: {agent_name}")
        print(f"Session: {session_file.name}")
        print(f"Ready for bootstrap prompt!\n")
        
        return True, session_file


# Import subprocess at module level for the functions that need it
import subprocess