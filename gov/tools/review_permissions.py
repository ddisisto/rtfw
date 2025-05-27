#!/usr/bin/env python3
"""
CLI tool for reviewing permission requests

Usage:
    python review_permissions.py           # List pending
    python review_permissions.py <id>      # Show details
    python review_permissions.py <id> allow "reason"
    python review_permissions.py <id> deny "explanation"
"""

import sys
import os
import json
from datetime import datetime

QUEUE_DIR = "/home/daniel/prj/rtfw/gov/tools/permissions"

def list_pending():
    """List all pending permission requests"""
    if not os.path.exists(QUEUE_DIR):
        print("No pending permissions")
        return
    
    files = [f for f in os.listdir(QUEUE_DIR) if f.endswith('.json')]
    
    if not files:
        print("No pending permissions")
        return
    
    print("PENDING PERMISSION REQUESTS")
    print("-" * 60)
    
    for filename in sorted(files):
        with open(os.path.join(QUEUE_DIR, filename), 'r') as f:
            req = json.load(f)
        
        age = datetime.now() - datetime.fromisoformat(req['timestamp'])
        age_str = f"{int(age.total_seconds())}s ago"
        
        print(f"{req['id']}: {req['tool']} - {age_str}")
        
        if req['tool'] in ['Write', 'Edit', 'MultiEdit']:
            print(f"  File: {req['params'].get('file_path', 'unknown')}")
        elif req['tool'] == 'Bash':
            cmd = req['params'].get('command', '')
            print(f"  Cmd: {cmd[:50]}{'...' if len(cmd) > 50 else ''}")
        print()

def show_details(request_id):
    """Show detailed information about a request"""
    filepath = os.path.join(QUEUE_DIR, f"{request_id}.json")
    
    if not os.path.exists(filepath):
        print(f"Request {request_id} not found")
        return
    
    with open(filepath, 'r') as f:
        req = json.load(f)
    
    print(f"PERMISSION REQUEST: {request_id}")
    print("=" * 60)
    print(f"Tool: {req['tool']}")
    print(f"Time: {req['timestamp']}")
    print(f"\nParameters:")
    print(json.dumps(req['params'], indent=2))
    print(f"\nContext:")
    print(json.dumps(req['context'], indent=2))
    print("\nTo approve: review_permissions.py", request_id, "allow \"reason\"")
    print("To deny:    review_permissions.py", request_id, "deny \"explanation\"")

def make_decision(request_id, behavior, reason):
    """Record a decision"""
    filepath = os.path.join(QUEUE_DIR, f"{request_id}.json")
    
    if not os.path.exists(filepath):
        print(f"Request {request_id} not found")
        return
    
    # Write decision file
    decision_file = os.path.join(QUEUE_DIR, f"{request_id}.decision")
    with open(decision_file, 'w') as f:
        f.write(f"{behavior}:{reason}")
    
    print(f"Decision recorded: {behavior.upper()}")
    
    # For denials, suggest messaging the agent
    if behavior == 'deny':
        print(f"\nAgent is now blocked. Send explanation:")
        print(f"git commit -m \"@GOV: Permission denied - {reason}\"")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        list_pending()
    elif len(sys.argv) == 2:
        show_details(sys.argv[1])
    elif len(sys.argv) == 4:
        make_decision(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print(__doc__)