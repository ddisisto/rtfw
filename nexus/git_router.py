#!/usr/bin/env python3
"""
Enhanced git-comms router for NEXUS.
Parse git commits → Check tmux windows → Route or log unroutable
"""

import subprocess
import re
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple
from datetime import datetime

class GitRouter:
    """Git-based message router for RTFW agent system."""
    
    def __init__(self, state_file: str = ".gitcomms"):
        self.state_file = Path(state_file)
        self.last_processed = self._load_state()
        self.tmux_windows = self._get_tmux_windows()
        self.unroutable_log = Path("nexus/unroutable.log")
        self.routing_log = Path("nexus/routing.log")
        self.admin_inbox = Path("admin/inbox.txt")
        
    def _load_state(self) -> Optional[str]:
        """Load last processed commit hash."""
        if self.state_file.exists():
            return self.state_file.read_text().strip()
        return None
    
    def _save_state(self, commit_hash: str):
        """Save last processed commit hash."""
        self.state_file.write_text(commit_hash)
    
    def _get_tmux_windows(self) -> Set[str]:
        """Get list of current tmux windows."""
        try:
            result = subprocess.run(
                ["tmux", "list-windows", "-F", "#W"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return set(result.stdout.strip().split('\n'))
            return set()
        except:
            return set()
    
    def _append_to_file(self, filepath: Path, content: str):
        """Atomically append to file with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filepath, 'a') as f:
            f.write(f"[{timestamp}] {content}\n")
    
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
    
    def check_routable(self, msg: Dict) -> Tuple[bool, str]:
        """
        Check if message is routable.
        Returns (is_routable, reason)
        """
        to_agent = msg['to'].lower()
        
        # Special handling for ADMIN
        if to_agent == 'admin':
            return True, "admin-inbox"
        
        # Check if window exists
        if to_agent in self.tmux_windows:
            return True, "tmux-window"
        
        # Not routable
        return False, f"No tmux window '{to_agent}'"
    
    def deliver_message(self, msg: Dict) -> bool:
        """Deliver message to appropriate destination."""
        to_agent = msg['to'].lower()
        routing_msg = f"@Router → @{msg['to'].upper()}: Please review commit {msg['hash']} - {msg['message']}"
        
        # Special handling for ADMIN
        if to_agent == 'admin':
            self._append_to_file(self.admin_inbox, routing_msg)
            return True
        
        # Normal tmux delivery
        agent_window = to_agent
        
        # Send message text
        cmd = ["tmux", "send-keys", "-t", agent_window, routing_msg]
        result = subprocess.run(cmd, capture_output=True)
        
        if result.returncode == 0:
            # Send Enter to submit (CRITICAL: separate command!)
            subprocess.run(["tmux", "send-keys", "-t", agent_window, "Enter"])
            return True
        else:
            print(f"Failed to deliver to {to_agent}: {result.stderr.decode()}")
            return False
    
    def process_messages(self, auto_deliver=False):
        """Main processing loop."""
        messages = self.parse_commits()
        
        if not messages:
            print("No new messages to route")
            self._append_to_file(self.routing_log, "No new messages to route")
            return
        
        print(f"Found {len(messages)} message(s) with @ → @ pattern:\n")
        print(f"Active tmux windows: {sorted(self.tmux_windows)}\n")
        
        routed_count = 0
        unroutable_count = 0
        
        for msg in messages:
            is_routable, reason = self.check_routable(msg)
            status = "[routable]" if is_routable else f"[unroutable: {reason}]"
            print(f"{msg['message']} {status}")
            
            if auto_deliver:
                if is_routable:
                    if self.deliver_message(msg):
                        routed_count += 1
                        log_msg = f"Delivered to {msg['to']}: {msg['message']}"
                        self._append_to_file(self.routing_log, log_msg)
                        print(f"  ✓ Delivered to {msg['to']} ({reason})")
                else:
                    unroutable_count += 1
                    log_msg = f"Unroutable ({reason}): {msg['message']}"
                    self._append_to_file(self.unroutable_log, log_msg)
                    print(f"  ⚠ Logged as unroutable")
            else:
                if is_routable:
                    print(f"  → Would route to {msg['to']} ({reason})")
                else:
                    print(f"  → Would log as unroutable")
        
        # Update state only if we actually processed messages
        if messages and auto_deliver:
            self._save_state(messages[-1]['full_hash'])
            summary = f"Processed {len(messages)} messages: {routed_count} delivered, {unroutable_count} unroutable"
            self._append_to_file(self.routing_log, f"=== Routing complete: {summary} ===")
            print(f"\n{summary}")
            print(f"State updated. Processed through {messages[-1]['hash']}")
        elif messages and not auto_deliver:
            print(f"\nViewing only - no actions taken (use --deliver to process)")

def main():
    """Entry point."""
    import sys
    
    router = GitRouter()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "status":
            print("Git Router Status")
            print(f"State file: {router.state_file}")
            print(f"Last processed: {router.last_processed or 'None'}")
            print(f"Active windows: {sorted(router.tmux_windows)}")
            print(f"Log files: {router.routing_log}, {router.unroutable_log}")
        elif sys.argv[1] == "--deliver":
            router.process_messages(auto_deliver=True)
        else:
            print(f"Unknown argument: {sys.argv[1]}")
            print("Usage: git_router.py [status|--deliver]")
    else:
        router.process_messages(auto_deliver=False)

if __name__ == "__main__":
    main()