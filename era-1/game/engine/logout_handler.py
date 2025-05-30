"""
Logout Handler - Automates logout to bootstrap process

Handles:
1. Detecting logout state
2. Waiting for session termination
3. Restarting Claude via tmux
4. Sending bootstrap prompt
"""

import time
from pathlib import Path
from typing import Optional
from datetime import datetime

from .tmux_handler import TmuxHandler
from .agent_creator import AgentCreator


class LogoutHandler:
    """
    Manages the logout → bootstrap automation
    
    When an agent enters logout state:
    1. Updates logout.log
    2. Sends /exit to Claude
    3. Resets context tokens to 0 in _state.md
    4. Runs `claude` command
    5. Sends /clear
    6. Sends /status and captures output
    7. Waits for new session file
    8. Updates symlink
    9. Sends bootstrap prompt
    """
    
    def __init__(self, project_root: Path, sessions_dir: Path):
        self.project_root = project_root
        self.sessions_dir = sessions_dir
        self.logout_log = project_root / "logout.log"
        self.tmux = TmuxHandler()
        self.creator = AgentCreator(project_root, sessions_dir)
    
    def handle_logout(self, agent_name: str, tmux_session: str) -> bool:
        """
        Handle agent logout and bootstrap restart
        
        Args:
            agent_name: Agent name (e.g., 'era-1')
            tmux_session: Tmux session name for the agent
            
        Returns:
            True if successful, False otherwise
        """
        print(f"\n=== LOGOUT HANDLER for {agent_name} ===")
        
        try:
            # 1. Log the logout event
            self._log_logout(agent_name)
            
            # 2. Send /exit to Claude
            print("Sending /exit command...")
            self.tmux.send_claude_command(tmux_session, "/exit", wait_after=2.0)
            
            # 3. Context tokens already reset by state engine
            print("Context tokens reset to 0 by engine")
            
            # 4. Start new Claude session
            print("Starting new Claude session...")
            self.tmux.start_claude_session(tmux_session)
            
            # 5. Send /clear
            print("Sending /clear command...")
            self.tmux.send_claude_command(tmux_session, "/clear", wait_after=1.0)
            
            # 6. Send /status and wait
            print("Sending /status command...")
            self.tmux.send_claude_command(tmux_session, "/status", wait_after=2.0)
            
            # 7. Close status display
            print("Closing status display...")
            self.tmux.send_key(tmux_session, "Enter")
            time.sleep(1)
            
            # 8. Find new session file using common function
            print("Waiting for new session file...")
            before_files = set()  # Empty since we just exited
            new_session = self.creator.find_new_session(before_files)
            if not new_session:
                print("ERROR: No new session file appeared")
                return False
            
            # 9. Create symlink using common function
            if not self.creator.create_symlink(agent_name, new_session):
                print("ERROR: Failed to create symlink")
                return False
            
            # 10. Send bootstrap prompt
            print("Sending bootstrap prompt...")
            agent_upper = agent_name.upper()
            bootstrap_prompt = f"please apply @protocols/bootstrap.md context load for agent @{agent_upper}.md"
            self.tmux.send_prompt(tmux_session, bootstrap_prompt)
            
            print(f"=== LOGOUT HANDLER COMPLETE for {agent_name} ===\n")
            return True
            
        except Exception as e:
            print(f"ERROR in logout handler: {e}")
            return False
    
    def _log_logout(self, agent_name: str):
        """Append logout event to logout.log"""
        timestamp = datetime.now().isoformat()
        with open(self.logout_log, 'a') as f:
            f.write(f"ENGINE: {timestamp} - {agent_name} logout processed\n")
    
    # Methods moved to AgentCreator for reuse
    
    def check_tmux_session_exists(self, session: str) -> bool:
        """Check if tmux session exists"""
        return self.tmux.check_session_exists(session)