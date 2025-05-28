"""
Agent monitoring implementation using safe read-only patterns
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple

from interfaces import AgentMonitor, Agent, AgentStatus


class FileSystemAgentMonitor(AgentMonitor):
    """
    Real agent monitoring via filesystem, git, and tmux
    
    Uses patterns from nexus/agent-data-patterns.md for safe access
    """
    
    def __init__(self, repo_root: str = "/home/daniel/prj/rtfw"):
        self.repo_root = Path(repo_root)
        self.session_cache = {}
        self._load_session_mappings()
    
    def _load_session_mappings(self):
        """Load current session mappings from NEXUS"""
        session_file = self.repo_root / "nexus/sessions/current_sessions.json"
        try:
            if session_file.exists():
                with open(session_file) as f:
                    self.session_cache = json.load(f)
        except:
            # Fail gracefully if file missing or invalid
            pass
    
    def _run_command(self, cmd: str) -> str:
        """Run shell command and return output"""
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, 
                text=True, cwd=self.repo_root
            )
            return result.stdout.strip()
        except:
            return ""
    
    def get_all_agents(self) -> List[str]:
        """List all known agents from tmux windows and git history"""
        agents = set()
        
        # Get from tmux windows
        tmux_output = self._run_command("tmux list-windows -F '#{window_name}'")
        for line in tmux_output.splitlines():
            # Skip system windows
            if line and line not in ["admin", "bash"]:
                agents.add(line.upper())
        
        # Get from recent git commits (find agents who have committed)
        git_output = self._run_command(
            "git log --oneline -100 | grep -o '@[A-Z][A-Z0-9-]*:' | sort -u"
        )
        for match in git_output.splitlines():
            if match:
                agent = match.strip('@:')
                agents.add(agent)
        
        # Include known meta agents even if not active
        for meta in ["GOV", "NEXUS", "CRITIC", "ERA-1"]:
            agents.add(meta)
        
        return sorted(list(agents))
    
    def get_agent_status(self, agent_name: str) -> Agent:
        """Get complete status for a single agent"""
        # Check tmux window status
        window_line = self._run_command(
            f"tmux list-windows | grep -i '{agent_name.lower()}'"
        )
        
        if not window_line:
            status = AgentStatus.OFFLINE
        elif "*" in window_line:
            status = AgentStatus.ACTIVE
        elif "-" in window_line:
            status = AgentStatus.SILENT
        else:
            status = AgentStatus.IDLE
        
        # Extra real-time check: see if agent is actively typing
        # by checking if their pane has recent activity
        if status in [AgentStatus.ACTIVE, AgentStatus.IDLE]:
            # Check if window has activity in last 30 seconds
            activity_check = self._run_command(
                f"tmux list-windows -F '#{{window_name}} #{{window_activity}}' | grep -i '{agent_name.lower()}'"
            )
            if activity_check:
                try:
                    parts = activity_check.split()
                    if len(parts) >= 2:
                        activity_time = int(parts[1])
                        current_time = int(self._run_command("date +%s"))
                        if current_time - activity_time < 30:  # Active in last 30 sec
                            status = AgentStatus.ACTIVE
                except:
                    pass
        
        # Get context size
        lines, percent = self.get_context_size(agent_name)
        
        # Get last activity
        last_activity = self.get_last_activity(agent_name)
        
        # Get current task
        current_task = self.get_current_task(agent_name)
        
        # Get session ID if available
        session_id = self.session_cache.get(agent_name.lower())
        
        return Agent(
            name=agent_name,
            status=status,
            context_size=lines,
            context_percent=percent,
            last_activity=last_activity,
            current_task=current_task,
            session_id=session_id
        )
    
    def get_context_size(self, agent_name: str) -> Tuple[int, int]:
        """Return (lines, percent_full) for agent's context.md"""
        context_path = self.repo_root / agent_name.lower() / "context.md"
        
        try:
            if context_path.exists():
                lines = len(context_path.read_text().splitlines())
                # Rough estimate: 2000 lines = 100% capacity
                percent = min(100, (lines * 100) // 2000)
                return lines, percent
        except:
            pass
        
        return 0, 0
    
    def get_last_activity(self, agent_name: str) -> str:
        """Get human-readable time since last commit"""
        output = self._run_command(
            f"git log -1 --format='%ar' --author='@{agent_name}'"
        )
        return output or "Never"
    
    def get_current_task(self, agent_name: str) -> Optional[str]:
        """Extract current task from scratch.md if available"""
        scratch_path = self.repo_root / agent_name.lower() / "scratch.md"
        
        try:
            if scratch_path.exists():
                content = scratch_path.read_text()
                # Look for common task indicators
                for line in content.splitlines():
                    if any(marker in line.lower() for marker in 
                           ["next action", "current task", "working on"]):
                        # Return the line after the marker
                        idx = content.splitlines().index(line)
                        if idx + 1 < len(content.splitlines()):
                            task = content.splitlines()[idx + 1].strip()
                            if task and not task.startswith("#"):
                                return task[:50] + "..." if len(task) > 50 else task
        except:
            pass
        
        return None