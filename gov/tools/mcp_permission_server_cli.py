#!/usr/bin/env python3
"""
MCP Permission Server - CLI/File-Based Review System

Foundation Era appropriate - no web interface!
Reviews handled via:
1. File-based queue (gov/tools/permission_queue.txt)
2. CLI commands for review
3. Git commits for notifications

Usage:
    python mcp_permission_server_cli.py [--port 8080]
"""

import json
import logging
import time
import threading
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, Optional
import re
from datetime import datetime
from queue import Queue

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(message)s'
)

class FileBasedQueue:
    """Manages pending permissions via filesystem"""
    
    QUEUE_DIR = "/home/daniel/prj/rtfw/gov/tools/permissions"
    
    def __init__(self):
        os.makedirs(self.QUEUE_DIR, exist_ok=True)
        self.waiting = {}  # request_id -> threading.Event
    
    def add_request(self, request_id: str, tool: str, params: Dict[str, Any], 
                   context: Dict[str, Any]) -> threading.Event:
        """Write request to file, return event to wait on"""
        
        # Create event for this request
        event = threading.Event()
        self.waiting[request_id] = event
        
        # Write request file
        request_file = os.path.join(self.QUEUE_DIR, f"{request_id}.json")
        with open(request_file, 'w') as f:
            json.dump({
                'id': request_id,
                'timestamp': datetime.now().isoformat(),
                'tool': tool,
                'params': params,
                'context': context,
                'status': 'pending'
            }, f, indent=2)
        
        # Create notification in scratch
        self._notify_via_scratch(request_id, tool, params)
        
        return event
    
    def _notify_via_scratch(self, request_id: str, tool: str, params: Dict[str, Any]):
        """Append notification to GOV scratch for visibility"""
        scratch_path = "/home/daniel/prj/rtfw/gov/scratch.md"
        
        notification = f"\n\n## PERMISSION REVIEW NEEDED - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        notification += f"Request ID: {request_id}\n"
        notification += f"Tool: {tool}\n"
        
        if tool in ['Write', 'Edit', 'MultiEdit']:
            notification += f"File: {params.get('file_path', 'unknown')}\n"
        elif tool == 'Bash':
            cmd = params.get('command', '')
            notification += f"Command: {cmd[:50]}{'...' if len(cmd) > 50 else ''}\n"
        
        notification += f"Review: Check gov/tools/permissions/{request_id}.json\n"
        notification += f"Approve: echo 'allow:reason' > gov/tools/permissions/{request_id}.decision\n"
        notification += f"Deny: echo 'deny:explanation' > gov/tools/permissions/{request_id}.decision\n"
        
        with open(scratch_path, 'a') as f:
            f.write(notification)
    
    def check_decision(self, request_id: str) -> Optional[Dict[str, Any]]:
        """Check if decision file exists"""
        decision_file = os.path.join(self.QUEUE_DIR, f"{request_id}.decision")
        
        if os.path.exists(decision_file):
            with open(decision_file, 'r') as f:
                decision_text = f.read().strip()
            
            # Parse decision format: "allow:reason" or "deny:explanation"
            if ':' in decision_text:
                behavior, reason = decision_text.split(':', 1)
                
                # Clean up files
                os.remove(decision_file)
                os.remove(os.path.join(self.QUEUE_DIR, f"{request_id}.json"))
                
                if behavior == 'allow':
                    return {
                        'behavior': 'allow',
                        'updatedInput': {},
                        '_reason': reason  # Internal tracking
                    }
                else:
                    return {
                        'behavior': 'deny',
                        'message': reason
                    }
        
        return None
    
    def resolve(self, request_id: str, decision: Dict[str, Any]):
        """Signal waiting thread that decision is ready"""
        if request_id in self.waiting:
            self.waiting[request_id].set()

class GovPermissionHandler(BaseHTTPRequestHandler):
    """HTTP handler for MCP permission requests"""
    
    queue = FileBasedQueue()
    request_counter = 0
    
    def do_POST(self):
        """Handle permission request"""
        if self.path != '/permission':
            self.send_error(404)
            return
        
        content_length = int(self.headers['Content-Length'])
        request_data = self.rfile.read(content_length)
        
        try:
            request = json.loads(request_data)
            response = self.process_permission_request(request)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            logging.error(f"Error processing request: {e}")
            self.send_error(500, str(e))
    
    def process_permission_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming permission request"""
        tool = request.get('tool', '')
        params = request.get('params', {})
        
        # Check for auto-approval
        decision = self.check_auto_approval(tool, params)
        
        if decision:
            logging.info(f"Auto-approved: {tool} {params}")
            return decision
        
        # Need review - queue it
        return self.queue_for_review(tool, params)
    
    def check_auto_approval(self, tool: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check if request can be auto-approved"""
        
        # Always approve read operations
        if tool in ['Read', 'Glob', 'Grep', 'LS']:
            return {'behavior': 'allow', 'updatedInput': {}}
        
        # Check write operations
        if tool in ['Write', 'MultiEdit', 'Edit']:
            file_path = params.get('file_path', '')
            
            # Extract agent directory
            if file_path.startswith('/'):
                file_path = file_path[1:]
            
            parts = file_path.split('/')
            if parts:
                agent_dir = parts[0]
                known_agents = ['era-1', 'nexus', 'gov', 'critic', 'admin']
                
                if agent_dir in known_agents:
                    # Check for special files
                    filename = parts[-1] if len(parts) > 1 else ''
                    
                    # ALLCAPS.md needs review
                    if filename.endswith('.md') and filename[:-3].isupper():
                        return None
                    
                    # Protocols need review
                    if 'protocols' in parts:
                        return None
                    
                    # Otherwise approve agent workspace write
                    return {'behavior': 'allow', 'updatedInput': {}}
        
        # Bash commands
        if tool == 'Bash':
            command = params.get('command', '')
            
            # Safe read-only commands
            safe_prefixes = [
                'git log', 'git status', 'git diff', 'git show',
                'ls', 'cat', 'head', 'tail', 'wc', 'pwd', 'date'
            ]
            
            if any(command.strip().startswith(prefix) for prefix in safe_prefixes):
                return {'behavior': 'allow', 'updatedInput': {}}
            
            # Git operations
            if command.strip().startswith('git commit'):
                return {'behavior': 'allow', 'updatedInput': {}}
            
            if command.strip().startswith('git add'):
                # Check what's being added
                for agent in ['era-1', 'nexus', 'gov', 'critic']:
                    if f' {agent}/' in command or command.endswith(f' {agent}'):
                        return {'behavior': 'allow', 'updatedInput': {}}
        
        # Default: needs review
        return None
    
    def queue_for_review(self, tool: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Queue request for CLI review"""
        
        # Generate request ID
        GovPermissionHandler.request_counter += 1
        request_id = f"perm_{GovPermissionHandler.request_counter:04d}"
        
        # Extract context
        context = {}
        if tool in ['Write', 'Edit', 'MultiEdit']:
            file_path = params.get('file_path', '')
            context['file_type'] = 'protocol' if '/protocols/' in file_path else 'general'
            context['is_allcaps'] = file_path.endswith('.md') and file_path.split('/')[-1][:-3].isupper()
        elif tool == 'Bash':
            command = params.get('command', '')
            context['command_type'] = 'destructive' if any(x in command for x in ['rm', 'delete']) else 'unknown'
        
        # Add to queue
        event = self.queue.add_request(request_id, tool, params, context)
        
        # Monitor for decision (in separate thread)
        def monitor_decision():
            while not event.is_set():
                decision = self.queue.check_decision(request_id)
                if decision:
                    self.queue.resolve(request_id, decision)
                    break
                time.sleep(0.5)
        
        monitor_thread = threading.Thread(target=monitor_decision)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # Wait for decision (blocking the agent)
        if event.wait(timeout=300):  # 5 minute timeout
            decision = self.queue.check_decision(request_id)
            if decision:
                # Log approval for potential follow-up message
                if decision.get('behavior') == 'allow' and '_reason' in decision:
                    logging.info(f"Approved {request_id} with note: {decision['_reason']}")
                    # Remove internal field
                    decision.pop('_reason', None)
                return decision
        
        # Timeout - deny with explanation
        return {
            'behavior': 'deny',
            'message': f"Permission review timeout. Check gov/tools/permissions/{request_id}.json and provide decision."
        }
    
    def log_message(self, format, *args):
        """Suppress HTTP logging"""
        pass

def run_server(port: int = 8080):
    """Run the permission server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, GovPermissionHandler)
    
    print(f"GOV Permission Server (CLI) running on port {port}")
    print(f"Pending reviews will appear in: gov/scratch.md")
    print(f"Review files in: gov/tools/permissions/")
    print(f"Use with: claude-code --permission-prompt-tool http://localhost:{port}/permission")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        httpd.shutdown()

if __name__ == '__main__':
    import sys
    port = 8080
    if len(sys.argv) > 2 and sys.argv[1] == '--port':
        port = int(sys.argv[2])
    run_server(port)