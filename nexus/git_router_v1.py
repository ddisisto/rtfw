#!/usr/bin/env python3
"""
Minimal git-comms router for NEXUS.
Parse git commits → Extract routable messages → Deliver via tmux
"""

import subprocess
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple

class GitRouter:
    """Git-based message router for RTFW agent system."""
    
    def __init__(self, state_file: str = ".gitcomms"):
        self.state_file = Path(state_file)
        self.last_processed = self._load_state()
        
    def _load_state(self) -> Optional[str]:
        """Load last processed commit hash."""
        if self.state_file.exists():
            return self.state_file.read_text().strip()
        return None
    
    def _save_state(self, commit_hash: str):
        """Save last processed commit hash."""
        self.state_file.write_text(commit_hash)
    
    def parse_commits(self) -> List[Dict]:
        """Parse git log for routable messages."""
        cmd = ["git", "log", "--pretty=format:%H|%s", "--reverse"]
        if self.last_processed:
            cmd.append(f"{self.last_processed}..HEAD")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0 or not result.stdout.strip():
            return []
        
        messages = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            
            hash_full, subject = line.split('|', 1)
            hash_short = hash_full[:7]
            
            # Match @FROM → @TO pattern (with optional priority flags)
            match = re.search(r'@(\w+)\s*→\s*@(\w+)(?:\s*\[([^\]]+)\])?(.*)', subject)
            if match:
                from_agent, to_agent, topic, rest = match.groups()
                messages.append({
                    'hash': hash_short,
                    'from': from_agent,
                    'to': to_agent,
                    'topic': topic or '',
                    'message': subject,
                    'full_hash': hash_full
                })
        
        return messages
    
    def route_message(self, msg: Dict) -> Optional[str]:
        """
        Determine routing for a message.
        Returns routing message if single addressee, None otherwise.
        """
        to_agent = msg['to'].lower()
        
        # TODO: Handle @ALL expansion
        # - Discover agents from @AGENT.md files
        # - Expand to list of active agents
        # - Return multiple routing commands
        if to_agent == 'all':
            return None  # Not auto-routable yet
        
        # Single addressee - create routing message
        # Note: Using generic "Router" instead of "NEXUS" for abstraction
        routing_msg = f"@Router → @{msg['to'].upper()}: Please review commit {msg['hash']} - {msg['message']}"
        return routing_msg
    
    def deliver_via_tmux(self, agent: str, message: str):
        """Send message to agent via tmux."""
        agent_window = agent.lower()
        
        # Send message text
        cmd = ["tmux", "send-keys", "-t", agent_window, message]
        result = subprocess.run(cmd, capture_output=True)
        
        if result.returncode == 0:
            # Send Enter to submit (CRITICAL: separate command!)
            subprocess.run(["tmux", "send-keys", "-t", agent_window, "Enter"])
            return True
        else:
            print(f"Failed to deliver to {agent}: {result.stderr.decode()}")
            return False
    
    def process_messages(self, auto_deliver=False):
        """Main processing loop."""
        messages = self.parse_commits()
        
        if not messages:
            print("No new messages to route")
            return
        
        print(f"Found {len(messages)} message(s) with @ → @ pattern:\n")
        
        # Show all messages with routability status
        for msg in messages:
            routing = self.route_message(msg)
            status = "[auto-routable]" if routing else "[manual review needed]"
            print(f"{msg['message']} {status} [commit: {msg['hash']}]")
        
        print("\nRouting analysis:")
        routed_count = 0
        
        for msg in messages:
            routing = self.route_message(msg)
            if routing:
                print(f"\n→ To {msg['to'].upper()}: {routing}")
                
                # Only deliver if auto_deliver is enabled
                if auto_deliver:
                    if self.deliver_via_tmux(msg['to'], routing):
                        routed_count += 1
                        print(f"  ✓ Delivered")
                else:
                    print(f"  ⚠ Auto-delivery disabled (use --deliver to enable)")
            else:
                print(f"\n→ To {msg['to'].upper()}: Manual routing required (@ALL expansion not implemented)")
        
        # Update state only if we actually delivered messages
        if messages and auto_deliver:
            self._save_state(messages[-1]['full_hash'])
            if routed_count > 0:
                print(f"\nDelivered {routed_count} message(s).")
            print(f"\nState updated. Processed through {messages[-1]['hash']}")
        elif messages and not auto_deliver:
            print(f"\nViewing only - state file not updated (use --deliver to process)")

def main():
    """Entry point."""
    import sys
    
    router = GitRouter()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "status":
            print("Git Router Status")
            print(f"State file: {router.state_file}")
            print(f"Last processed: {router.last_processed or 'None'}")
        elif sys.argv[1] == "--deliver":
            router.process_messages(auto_deliver=True)
        else:
            print(f"Unknown argument: {sys.argv[1]}")
            print("Usage: git_router.py [status|--deliver]")
    else:
        router.process_messages(auto_deliver=False)

if __name__ == "__main__":
    main()