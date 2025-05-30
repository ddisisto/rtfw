"""
PID file management for single-instance enforcement
"""

import os
import sys
import fcntl
from pathlib import Path
from typing import Optional


class PidFile:
    """Ensure only one instance of the engine runs at a time"""
    
    def __init__(self, pid_path: Path):
        self.pid_path = pid_path
        self.pid_file = None
        
    def acquire(self) -> bool:
        """Try to acquire exclusive lock. Returns True if successful."""
        try:
            # Create pid file if it doesn't exist
            self.pid_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Open for writing (create if needed)
            self.pid_file = open(self.pid_path, 'w')
            
            # Try to get exclusive lock (non-blocking)
            fcntl.flock(self.pid_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            
            # Write our PID
            self.pid_file.write(str(os.getpid()))
            self.pid_file.flush()
            
            return True
            
        except IOError:
            # Lock is held by another process
            if self.pid_file:
                self.pid_file.close()
                self.pid_file = None
            return False
    
    def release(self):
        """Release the lock and remove pid file"""
        if self.pid_file:
            try:
                # Unlock
                fcntl.flock(self.pid_file.fileno(), fcntl.LOCK_UN)
                self.pid_file.close()
                # Remove file
                self.pid_path.unlink(missing_ok=True)
            except:
                pass
            finally:
                self.pid_file = None
    
    def read_pid(self) -> Optional[int]:
        """Read PID from file if it exists"""
        try:
            if self.pid_path.exists():
                return int(self.pid_path.read_text().strip())
        except:
            pass
        return None
    
    def is_running(self, pid: int) -> bool:
        """Check if a process with given PID is running"""
        try:
            # Send signal 0 - doesn't actually send anything, just checks
            os.kill(pid, 0)
            return True
        except ProcessLookupError:
            return False
        except PermissionError:
            # Process exists but we can't signal it
            return True
    
    def __enter__(self):
        if not self.acquire():
            existing_pid = self.read_pid()
            if existing_pid and self.is_running(existing_pid):
                print(f"ERROR: Another instance is already running (PID: {existing_pid})")
                print(f"Kill it with: kill {existing_pid}")
            else:
                print("ERROR: Could not acquire lock on pid file")
                print(f"Remove stale file with: rm {self.pid_path}")
            sys.exit(1)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()