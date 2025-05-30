#!/usr/bin/env python3
"""
Manual test script for agent creation with symlink fix verification

Run this to test the new agent creation process step-by-step.
The script will pause at key points for manual verification.
"""

import sys
import time
from pathlib import Path

# Add the game directory to Python path
sys.path.insert(0, str(Path(__file__).parent / 'game'))

from engine.agent_creator import AgentCreator


def pause(message="Press Enter to continue..."):
    """Pause for user verification"""
    input(f"\n{message}")


def main():
    # Setup
    project_root = Path(__file__).parent.parent
    sessions_dir = project_root / '_sessions'
    
    print("=== AGENT CREATION TEST ===")
    print(f"Project root: {project_root}")
    print(f"Sessions dir: {sessions_dir}")
    
    # Get agent name
    agent_name = input("\nEnter test agent name (e.g., 'test-agent'): ").strip()
    if not agent_name:
        agent_name = f"test-agent-{int(time.time())}"
        print(f"Using default name: {agent_name}")
    
    # Create agent creator
    creator = AgentCreator(project_root, sessions_dir)
    
    # Track existing files
    before_files = set(sessions_dir.glob("*.jsonl"))
    print(f"\nExisting session files: {len(before_files)}")
    
    # Step 1: Create tmux window
    print("\n--- Step 1: Create tmux window ---")
    if not creator.create_tmux_window(agent_name):
        print("Failed to create tmux window!")
        return 1
    
    pause("Check tmux has new window. Press Enter to continue...")
    
    # Step 2: Verify bash
    print("\n--- Step 2: Verify bash ready ---")
    if not creator.verify_bash_ready(agent_name):
        print("Bash not ready!")
        return 1
    
    # Step 3: Start Claude
    print("\n--- Step 3: Start Claude CLI ---")
    if not creator.start_claude_cli(agent_name):
        print("Failed to start Claude!")
        return 1
    
    pause("Verify Claude is starting. Press Enter to continue...")
    
    # Step 4: Send /status
    print("\n--- Step 4: Send /status command ---")
    if not creator.send_status_command(agent_name):
        print("Failed to send /status!")
        return 1
    
    pause("Verify /status was sent and closed. Press Enter to continue...")
    
    # Step 5: Find new session
    print("\n--- Step 5: Find new session file ---")
    session_file = creator.find_new_session(before_files)
    if not session_file:
        print("No new session file found!")
        return 1
    
    # Step 6: Create symlink
    print("\n--- Step 6: Create symlink ---")
    if not creator.create_symlink(agent_name, session_file):
        print("Failed to create symlink!")
        return 1
    
    # Step 7: Initialize state
    print("\n--- Step 7: Initialize state ---")
    if not creator.initialize_state(agent_name):
        print("Failed to initialize state!")
        return 1
    
    # Now test the engine's symlink detection
    print("\n--- Testing Engine Symlink Detection ---")
    pause("About to run engine poll cycle. Press Enter...")
    
    # Import and run engine
    from engine.state_engine import StateEngine
    
    engine = StateEngine(project_root, sessions_dir)
    
    try:
        print("\nRunning engine poll cycle...")
        engine.poll_cycle()
        print("✓ Engine poll successful!")
        
        # Check if symlink was detected
        symlink_path = sessions_dir / f"{agent_name.upper()}_current.jsonl"
        if symlink_path.exists() and symlink_path.resolve() == session_file:
            print(f"✓ Symlink correctly points to: {session_file.name}")
        else:
            print(f"✗ Symlink issue detected!")
            
    except Exception as e:
        print(f"✗ Engine error: {e}")
        return 1
    
    print(f"\n=== TEST COMPLETE ===")
    print(f"Agent '{agent_name}' is ready for bootstrap prompt!")
    print(f"Session: {session_file.name}")
    print(f"\nNext step would be to send bootstrap prompt:")
    print(f'  "please apply @protocols/bootstrap.md context load for agent @{agent_name.upper()}.md"')
    
    # Cleanup option
    cleanup = input("\nCleanup test agent? (y/N): ").lower().strip()
    if cleanup == 'y':
        import subprocess
        # Kill tmux window
        subprocess.run(['tmux', 'kill-window', '-t', agent_name])
        # Remove symlink
        symlink_path.unlink()
        # Remove state file
        state_file = project_root / agent_name / "_state.md"
        if state_file.exists():
            state_file.unlink()
        # Remove directory if empty
        agent_dir = project_root / agent_name
        if agent_dir.exists() and not any(agent_dir.iterdir()):
            agent_dir.rmdir()
        print("✓ Cleanup complete")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())