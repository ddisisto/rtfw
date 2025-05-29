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
            
            # 8. Wait for new session file
            print("Waiting for new session file...")
            new_session = self._wait_for_new_session(agent_name)
            if not new_session:
                print("ERROR: No new session file appeared")
                return False
            
            # 9. Update symlink
            print(f"Updating symlink to {new_session.name}")
            self._update_symlink(agent_name, new_session)
            
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
    
    def _wait_for_new_session(self, agent_name: str, timeout: int = 30) -> Optional[Path]:
        """
        Wait for a new session file to appear
        
        Claude creates session files with random IDs, so we just look
        for any new .jsonl file in the sessions directory.
        
        Returns path to new session file or None if timeout
        """
        # Get all current .jsonl files
        before = set(self.sessions_dir.glob("*.jsonl"))
        
        # Wait for new file
        start_time = time.time()
        while time.time() - start_time < timeout:
            current = set(self.sessions_dir.glob("*.jsonl"))
            new_files = current - before
            
            if new_files:
                # Return the newest file
                return max(new_files, key=lambda p: p.stat().st_mtime)
            
            time.sleep(0.5)
        
        return None
    
    def _update_symlink(self, agent_name: str, target: Path):
        """Update agent's current session symlink"""
        agent_upper = agent_name.upper()
        symlink_name = f"{agent_upper}_current.jsonl"
        symlink_path = self.sessions_dir / symlink_name
        
        # Remove old symlink if exists
        if symlink_path.exists():
            symlink_path.unlink()
        
        # Create new symlink
        symlink_path.symlink_to(target.name)
    
    def check_tmux_session_exists(self, session: str) -> bool:
        """Check if tmux session exists"""
        return self.tmux.check_session_exists(session)