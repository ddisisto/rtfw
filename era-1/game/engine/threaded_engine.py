"""
Threaded State Engine - Runs in background thread with shared state access
"""

import threading
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

from .state_engine import StateEngine
from .models import AgentGroundState


class ThreadedStateEngine:
    """
    Wrapper around StateEngine that runs in a background thread
    
    Provides thread-safe access to current agent states for TUI/GUI
    Easy to later split into separate daemon process
    """
    
    def __init__(self, project_root: Path, sessions_dir: Path, poll_interval: int = 1):
        # Core engine
        self.engine = StateEngine(project_root, sessions_dir, poll_interval)
        
        # Thread management
        self.thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._state_lock = threading.RLock()
        
        # Shared state - updated by engine thread, read by TUI
        self._agent_states: Dict[str, AgentGroundState] = {}
        self._last_update: Optional[datetime] = None
        self._running = False
        
    def start(self):
        """Start the engine in a background thread"""
        if self.thread and self.thread.is_alive():
            return
        
        self._stop_event.clear()
        self._running = True
        
        # Start engine thread
        self.thread = threading.Thread(
            target=self._run_engine,
            name="StateEngine",
            daemon=True  # Dies with main program
        )
        self.thread.start()
        
        print(f"State Engine thread started")
    
    def stop(self):
        """Stop the background thread"""
        self._stop_event.set()
        self._running = False
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5.0)
            
        print("State Engine thread stopped")
    
    def _run_engine(self):
        """Background thread main loop"""
        while not self._stop_event.is_set():
            try:
                # Run poll cycle
                self.engine.poll_cycle()
                
                # Update shared state
                self._update_shared_state()
                
                # Sleep until next poll
                self._stop_event.wait(self.engine.poll_interval)
                
            except Exception as e:
                print(f"Engine thread error: {e}")
                # Continue running despite errors
    
    def _update_shared_state(self):
        """Update shared state from engine (thread-safe)"""
        with self._state_lock:
            # Read all agent states from known symlinks
            for agent_name in self.engine.monitor.AGENT_SYMLINKS.keys():
                state = self.engine.writer.read_agent_state(agent_name)
                if state:
                    self._agent_states[agent_name] = state
            
            self._last_update = datetime.now()
    
    # Thread-safe accessors for TUI
    
    def get_agent_state(self, agent_name: str) -> Optional[AgentGroundState]:
        """Get current state for an agent (thread-safe)"""
        with self._state_lock:
            return self._agent_states.get(agent_name)
    
    def get_all_agents(self) -> Dict[str, AgentGroundState]:
        """Get all agent states (thread-safe copy)"""
        with self._state_lock:
            return dict(self._agent_states)
    
    def get_status(self) -> Dict:
        """Get engine status (thread-safe)"""
        with self._state_lock:
            agent_summary = {}
            for name, state in self._agent_states.items():
                agent_summary[name] = {
                    'state': state.state.value,
                    'thread': state.thread,
                    'context_percent': state.context_percent,
                    'unread_messages': state.unread_message_count,
                    'session_id': state.session_id
                }
            
            return {
                'running': self._running,
                'thread_alive': self.thread.is_alive() if self.thread else False,
                'last_update': self._last_update.isoformat() if self._last_update else None,
                'agents': agent_summary,
                'errors': self.engine.errors[-5:]  # Last 5 errors
            }
    
    def is_running(self) -> bool:
        """Check if engine thread is running"""
        return self._running and self.thread and self.thread.is_alive()
    
    # Direct engine access for testing/debugging
    
    def force_poll(self):
        """Force an immediate poll cycle (blocks)"""
        self.engine.poll_cycle()
        self._update_shared_state()
    
    def get_engine_errors(self) -> list:
        """Get recent engine errors"""
        return self.engine.errors.copy()


# Example usage in TUI
class TUIExample:
    """Example of how TUI would use the threaded engine"""
    
    def __init__(self, project_root: Path):
        # Create and start engine
        self.engine = ThreadedStateEngine(
            project_root,
            project_root / "_sessions"
        )
        self.engine.start()
    
    def update_display(self):
        """Called periodically by TUI to update display"""
        # Get all agent states from memory (no file I/O)
        agents = self.engine.get_all_agents()
        
        for name, state in agents.items():
            print(f"{name}: {state.state.value} "
                  f"({state.context_percent:.1f}% context) "
                  f"[{state.unread_message_count} unread]")
    
    def cleanup(self):
        """Shutdown cleanly"""
        self.engine.stop()


# Daemon split preparation
class StateEngineDaemon:
    """
    Future: State engine as separate daemon process
    
    Would expose state via:
    - Unix socket
    - Shared memory
    - REST API
    - Message queue
    
    For now, threading is sufficient and simpler
    """
    pass