"""
Tmux Handler - Manages tmux interactions for all state transitions

Provides common tmux operations needed across different states:
- Sending commands and prompts
- Checking session existence
- Handling claude cli quirks (separate Enter key)
"""

import subprocess
import time
from typing import Optional, List


class TmuxHandler:
    """
    Manages tmux interactions for agent sessions
    
    Handles:
    - Command sending with proper Enter key handling
    - Session existence checks
    - Claude CLI specific quirks
    """
    
    def __init__(self):
        # Claude CLI requires Enter to be sent separately
        self.enter_delay = 0.1  # Small delay between command and Enter
    
    def send_command(self, session: str, command: str, wait_after: float = 0.5) -> bool:
        """
        Send a command to tmux session with separate Enter key
        
        Args:
            session: Tmux session name
            command: Command to send
            wait_after: Time to wait after sending (default 0.5s)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # First send the command text (without Enter)
            escaped = command.replace('"', '\\"')
            cmd = ['tmux', 'send-keys', '-t', session, escaped]
            subprocess.run(cmd, check=True)
            
            # Small delay before Enter
            time.sleep(self.enter_delay)
            
            # Then send Enter separately
            subprocess.run(['tmux', 'send-keys', '-t', session, 'Enter'], check=True)
            
            # Wait for command to process
            if wait_after > 0:
                time.sleep(wait_after)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"ERROR sending tmux command: {e}")
            return False
    
    def send_key(self, session: str, key: str) -> bool:
        """Send a single key to tmux session"""
        try:
            cmd = ['tmux', 'send-keys', '-t', session, key]
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def check_session_exists(self, session: str) -> bool:
        """Check if tmux session exists"""
        try:
            result = subprocess.run(
                ['tmux', 'has-session', '-t', session],
                capture_output=True
            )
            return result.returncode == 0
        except:
            return False
    
    def get_session_list(self) -> List[str]:
        """Get list of all tmux sessions"""
        try:
            result = subprocess.run(
                ['tmux', 'list-sessions', '-F', '#{session_name}'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip().split('\n')
            return []
        except:
            return []
    
    def send_claude_command(self, session: str, command: str, wait_after: float = 2.0) -> bool:
        """
        Send a Claude CLI command (like /exit, /clear, /status)
        
        Args:
            session: Tmux session name
            command: Claude command (should start with /)
            wait_after: Time to wait after sending (default 2s for commands)
            
        Returns:
            True if successful
        """
        if not command.startswith('/'):
            print(f"WARNING: Claude command should start with / but got: {command}")
        
        return self.send_command(session, command, wait_after)
    
    def send_prompt(self, session: str, prompt: str, wait_after: float = 1.0) -> bool:
        """
        Send a prompt to Claude
        
        Args:
            session: Tmux session name  
            prompt: Prompt text to send
            wait_after: Time to wait after sending (default 1s)
            
        Returns:
            True if successful
        """
        return self.send_command(session, prompt, wait_after)
    
    def start_claude_session(self, session: str) -> bool:
        """
        Start a new Claude session in tmux
        
        Args:
            session: Tmux session name
            
        Returns:
            True if successful
        """
        if not self.check_session_exists(session):
            print(f"ERROR: Tmux session '{session}' does not exist")
            return False
        
        # Send 'claude' command to start CLI
        return self.send_command(session, 'claude', wait_after=3.0)