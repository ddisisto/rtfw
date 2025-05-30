#!/usr/bin/env python3
"""
Test Engine Runner - Isolate and debug engine issues
"""

import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from engine.state_engine import StateEngine


def test_engine(dry_run=True):
    """Run engine once and report any errors
    
    Args:
        dry_run: If True, don't write state files (safe to run alongside main engine)
    """
    project_root = Path(__file__).parent.parent.parent
    sessions_dir = project_root / "_sessions"
    
    print(f"Project root: {project_root}")
    print(f"Sessions dir: {sessions_dir}")
    print(f"Sessions exist: {sessions_dir.exists()}")
    print(f"Mode: {'DRY RUN (read-only)' if dry_run else 'LIVE (will write files)'}")
    
    try:
        print("\nCreating engine...")
        engine = StateEngine(project_root, sessions_dir)
        
        print("\nRunning single poll...")
        engine.poll_cycle()
        
        print("\nChecking state files after poll:")
        for agent in ["critic", "era-1", "gov", "nexus"]:
            state_file = project_root / agent / "_state.md"
            if state_file.exists():
                # Read just the state line
                content = state_file.read_text()
                for line in content.splitlines():
                    if line.startswith("state:"):
                        print(f"  {agent}: {line}")
                        break
            else:
                print(f"  {agent}: No _state.md file")
                
    except Exception as e:
        print(f"\nERROR: {type(e).__name__}: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(test_engine())