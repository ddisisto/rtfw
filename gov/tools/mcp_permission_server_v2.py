#!/usr/bin/env python3
"""
MCP Permission Server v2 - Queue for Review Instead of Auto-Deny

Key change: Instead of denying, we queue complex requests for GOV/ADMIN review
with context, allowing for learning moments and nuanced decisions.

Usage:
    python mcp_permission_server_v2.py
    
Then run Claude Code with:
    claude-code --permission-prompt-tool http://localhost:8080/permission
"""

import json
import logging
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, Tuple, Optional
import re
from datetime import datetime
from queue import Queue

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class PermissionQueue:
    """Manages pending permission requests"""
    
    def __init__(self):
        self.pending = Queue()
        self.decisions = {}  # request_id -> decision
        self.waiting = {}    # request_id -> threading.Event
        
    def add_request(self, request_id: str, request: Dict[str, Any]) -> threading.Event:
        """Add request to queue, return event to wait on"""
        event = threading.Event()
        self.waiting[request_id] = event
        self.pending.put({
            'id': request_id,
            'timestamp': datetime.now(),
            'request': request
        })
        return event
    
    def get_pending(self) -> list:
        """Get all pending requests"""
        items = []
        while not self.pending.empty():
            items.append(self.pending.get())
        # Put them back
        for item in items:
            self.pending.put(item)
        return items
    
    def resolve(self, request_id: str, decision: Dict[str, Any]):
        """Resolve a pending request"""
        self.decisions[request_id] = decision
        if request_id in self.waiting:
            self.waiting[request_id].set()

class GovPermissionHandler(BaseHTTPRequestHandler):
    """HTTP handler for MCP permission requests"""
    
    queue = PermissionQueue()
    request_counter = 0
    
    def do_POST(self):
        """Handle permission request"""
        if self.path == '/permission':
            self.handle_permission_request()
        elif self.path == '/review':
            self.handle_review_interface()
        elif self.path.startswith('/decide/'):
            self.handle_decision()
        else:
            self.send_error(404)
    
    def handle_permission_request(self):
        """Process incoming permission request"""
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
        """Main permission logic - auto-approve or queue for review"""
        tool = request.get('tool', '')
        params = request.get('params', {})
        
        logging.info(f"Permission request: {tool} with params: {params}")
        
        # Check for auto-approval patterns
        decision = self.check_auto_approval(tool, params)
        
        if decision:
            return decision
        else:
            # Queue for review instead of auto-deny
            return self.queue_for_review(tool, params, request)
    
    def check_auto_approval(self, tool: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check if request can be auto-approved"""
        
        # Always approve read operations
        if tool in ['Read', 'Glob', 'Grep', 'LS']:
            return self.allow("Read operations always permitted")
        
        # Check write operations
        if tool in ['Write', 'MultiEdit', 'Edit']:
            file_path = params.get('file_path', '')
            
            # Agent writing to own workspace
            agent_match = re.match(r'^/?([^/]+)/', file_path)
            if agent_match:
                agent_dir = agent_match.group(1)
                known_agents = ['era-1', 'nexus', 'gov', 'critic', 'admin']
                if agent_dir in known_agents:
                    # But still check for special files
                    filename = file_path.split('/')[-1]
                    if filename.endswith('.md') and filename[:-3].isupper():
                        return None  # Queue for review
                    return self.allow(f"Write to {agent_dir} workspace approved")
        
        # Check bash commands
        if tool == 'Bash':
            command = params.get('command', '')
            
            # Safe read-only commands
            safe_commands = [
                'git log', 'git status', 'git diff', 'git show',
                'ls', 'cat', 'head', 'tail', 'wc', 'find', 'grep',
                'pwd', 'date', 'echo'
            ]
            
            if any(command.strip().startswith(cmd) for cmd in safe_commands):
                return self.allow("Read-only command approved")
            
            # Git commit always allowed
            if command.strip().startswith('git commit'):
                return self.allow("Git commit approved")
            
            # Git add on own workspace
            if command.strip().startswith('git add'):
                path_match = re.search(r'git add\s+([^\s]+)', command)
                if path_match:
                    path = path_match.group(1)
                    for agent in ['era-1', 'nexus', 'gov', 'critic']:
                        if path.startswith(f'{agent}/') or path == agent:
                            return self.allow(f"Git add on {agent} workspace approved")
        
        # Everything else needs review
        return None
    
    def queue_for_review(self, tool: str, params: Dict[str, Any], 
                        full_request: Dict[str, Any]) -> Dict[str, Any]:
        """Queue request for GOV/ADMIN review"""
        
        # Generate request ID
        GovPermissionHandler.request_counter += 1
        request_id = f"req_{GovPermissionHandler.request_counter}"
        
        # Create context-rich entry
        review_request = {
            'tool': tool,
            'params': params,
            'context': self.extract_context(tool, params),
            'full_request': full_request
        }
        
        # Add to queue
        event = self.queue.add_request(request_id, review_request)
        
        # Log for notification
        self.notify_reviewers(request_id, tool, params)
        
        # Wait for decision (with timeout)
        if event.wait(timeout=300):  # 5 minute timeout
            # Decision was made
            decision = self.queue.decisions.get(request_id)
            if decision:
                return decision
        
        # Timeout - return safe default
        return self.deny_with_explanation(
            f"Review timeout - please check with @GOV or @ADMIN about {tool} on {params}"
        )
    
    def extract_context(self, tool: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Extract helpful context for reviewers"""
        context = {}
        
        if tool in ['Write', 'Edit', 'MultiEdit']:
            file_path = params.get('file_path', '')
            context['file_path'] = file_path
            context['is_protocol'] = '/protocols/' in file_path
            context['is_allcaps'] = file_path.endswith('.md') and file_path.split('/')[-1][:-3].isupper()
            
        elif tool == 'Bash':
            command = params.get('command', '')
            context['command'] = command
            context['is_destructive'] = any(cmd in command for cmd in ['rm', 'delete', 'remove'])
            context['modifies_files'] = any(cmd in command for cmd in ['>', 'cp', 'mv'])
        
        return context
    
    def notify_reviewers(self, request_id: str, tool: str, params: Dict[str, Any]):
        """Log notification for reviewers"""
        message = f"\n{'='*60}\n"
        message += f"PERMISSION REVIEW NEEDED - {request_id}\n"
        message += f"Tool: {tool}\n"
        message += f"Params: {json.dumps(params, indent=2)}\n"
        message += f"Review at: http://localhost:8080/review\n"
        message += f"{'='*60}\n"
        
        logging.warning(message)
        
        # Also write to a notification file
        with open('/home/daniel/prj/rtfw/gov/tools/permission_notifications.txt', 'a') as f:
            f.write(f"{datetime.now()} - {request_id}: {tool} {params}\n")
    
    def handle_review_interface(self):
        """Serve review interface"""
        # Simple HTML interface for reviewing pending requests
        pending = self.queue.get_pending()
        
        html = """
        <html>
        <head><title>GOV Permission Review</title></head>
        <body>
        <h1>Pending Permission Requests</h1>
        """
        
        for item in pending:
            req_id = item['id']
            req = item['request']
            html += f"""
            <div style='border: 1px solid #ccc; padding: 10px; margin: 10px;'>
                <h3>{req_id} - {req['tool']}</h3>
                <pre>{json.dumps(req['params'], indent=2)}</pre>
                <p>Context: {json.dumps(req['context'], indent=2)}</p>
                <button onclick="decide('{req_id}', 'allow')">ALLOW with explanation</button>
                <button onclick="decide('{req_id}', 'deny')">DENY with explanation</button>
            </div>
            """
        
        html += """
        <script>
        function decide(id, behavior) {
            const reason = prompt('Explanation for ' + behavior + ':');
            if (reason) {
                fetch('/decide/' + id, {
                    method: 'POST',
                    body: JSON.stringify({behavior: behavior, reason: reason})
                });
                location.reload();
            }
        }
        </script>
        </body></html>
        """
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def handle_decision(self):
        """Handle review decision"""
        request_id = self.path.split('/')[-1]
        
        content_length = int(self.headers['Content-Length'])
        decision_data = self.rfile.read(content_length)
        decision = json.loads(decision_data)
        
        # Create appropriate response
        if decision['behavior'] == 'allow':
            response = self.allow(f"Approved by reviewer: {decision['reason']}")
        else:
            response = self.deny_with_explanation(f"Denied by reviewer: {decision['reason']}")
        
        # Resolve the queued request
        self.queue.resolve(request_id, response)
        
        self.send_response(200)
        self.end_headers()
    
    def allow(self, reason: str) -> Dict[str, Any]:
        """Generate allow response"""
        logging.info(f"ALLOWED: {reason}")
        return {
            'behavior': 'allow',
            'updatedInput': {}  # Pass through unchanged
        }
    
    def deny_with_explanation(self, explanation: str) -> Dict[str, Any]:
        """Generate deny response with learning context"""
        logging.warning(f"DENIED: {explanation}")
        return {
            'behavior': 'deny',
            'message': explanation
        }
    
    def log_message(self, format, *args):
        """Suppress default HTTP logging"""
        pass

def run_server(port: int = 8080):
    """Run the MCP permission server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, GovPermissionHandler)
    logging.info(f"GOV Permission Server v2 running on port {port}")
    logging.info("Review interface at: http://localhost:8080/review")
    logging.info("Use with: claude-code --permission-prompt-tool http://localhost:8080/permission")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("Server stopped")
        httpd.shutdown()

if __name__ == '__main__':
    run_server()