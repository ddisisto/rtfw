#!/usr/bin/env python3
"""
MCP Permission Server for GOV - Automates obvious tool approvals

Usage:
    python mcp_permission_server.py
    
Then run Claude Code with:
    claude-code --permission-prompt-tool http://localhost:8080/permission
"""

import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, Tuple
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class GovPermissionHandler(BaseHTTPRequestHandler):
    """HTTP handler for MCP permission requests"""
    
    def do_POST(self):
        """Handle permission request"""
        if self.path != '/permission':
            self.send_error(404)
            return
            
        # Read request
        content_length = int(self.headers['Content-Length'])
        request_data = self.rfile.read(content_length)
        
        try:
            request = json.loads(request_data)
            response = self.process_permission_request(request)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            logging.error(f"Error processing request: {e}")
            self.send_error(500, str(e))
    
    def process_permission_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Main permission logic"""
        tool = request.get('tool', '')
        params = request.get('params', {})
        
        logging.info(f"Permission request: {tool} with params: {params}")
        
        # Tool-specific handlers
        if tool in ['Write', 'MultiEdit']:
            return self.check_write_permission(params)
        elif tool == 'Bash':
            return self.check_bash_permission(params)
        elif tool in ['Read', 'Glob', 'Grep', 'LS']:
            # Always allow read operations
            return self.allow("Read operations always permitted")
        elif tool == 'Edit':
            return self.check_edit_permission(params)
        else:
            # Unknown tools require manual approval
            return self.deny(f"Unknown tool '{tool}' requires manual approval")
    
    def check_write_permission(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Check write/multiedit permissions"""
        file_path = params.get('file_path', '')
        
        # Extract agent from file path if it starts with agent directory
        agent_match = re.match(r'^/([^/]+)/', file_path)
        if agent_match:
            agent_dir = agent_match.group(1)
            
            # Check if it's a known agent directory
            known_agents = ['era-1', 'nexus', 'gov', 'critic', 'admin']
            if agent_dir in known_agents:
                return self.allow(f"Write to {agent_dir} workspace approved")
        
        # Check for ALLCAPS.md files
        filename = file_path.split('/')[-1]
        if filename.endswith('.md') and filename[:-3].isupper():
            return self.deny("ALLCAPS.md files require @GOV/@ADMIN approval")
        
        # Protocol directory requires approval
        if '/protocols/' in file_path:
            return self.deny("Protocol modifications require @GOV approval")
            
        return self.deny(f"Write to {file_path} requires manual approval")
    
    def check_edit_permission(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Check edit permissions - similar to write"""
        return self.check_write_permission(params)
    
    def check_bash_permission(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Check bash command permissions"""
        command = params.get('command', '')
        
        # Safe read-only commands
        safe_commands = [
            'git log', 'git status', 'git diff', 'git show',
            'ls', 'cat', 'head', 'tail', 'wc', 'find', 'grep'
        ]
        
        if any(command.startswith(cmd) for cmd in safe_commands):
            return self.allow("Read-only command approved")
        
        # Git operations on agent directories
        if command.startswith('git add'):
            # Extract path from git add command
            path_match = re.search(r'git add\s+(\S+)', command)
            if path_match:
                path = path_match.group(1)
                # Check if it's an agent directory
                for agent in ['era-1', 'nexus', 'gov', 'critic']:
                    if path.startswith(f'{agent}/') or path == agent:
                        return self.allow(f"Git add on {agent} workspace approved")
        
        # Git commit always allowed (message content is user responsibility)
        if command.startswith('git commit'):
            return self.allow("Git commit approved")
            
        # Directory creation in agent spaces
        if command.startswith('mkdir'):
            path_match = re.search(r'mkdir\s+(?:-p\s+)?(\S+)', command)
            if path_match:
                path = path_match.group(1)
                for agent in ['era-1', 'nexus', 'gov', 'critic']:
                    if path.startswith(f'{agent}/'):
                        return self.allow(f"Directory creation in {agent} approved")
        
        # File removal - more restricted
        if command.startswith('rm'):
            return self.deny("File removal requires manual approval")
            
        return self.deny(f"Command '{command[:50]}...' requires manual approval")
    
    def allow(self, reason: str) -> Dict[str, Any]:
        """Generate allow response"""
        logging.info(f"ALLOWED: {reason}")
        return {
            'behavior': 'allow',
            'updatedInput': {}  # Pass through unchanged
        }
    
    def deny(self, reason: str) -> Dict[str, Any]:
        """Generate deny response"""
        logging.warning(f"DENIED: {reason}")
        # Could queue for manual review here
        self.queue_for_review(reason)
        return {
            'behavior': 'deny',
            'message': reason
        }
    
    def queue_for_review(self, reason: str):
        """Queue denied requests for manual review"""
        # For now, just log. Could write to a file for later review
        with open('/home/daniel/prj/rtfw/gov/tools/permission_queue.log', 'a') as f:
            f.write(f"{logging.Formatter().formatTime(logging.LogRecord('', 0, '', 0, '', (), None))} - {reason}\n")
    
    def log_message(self, format, *args):
        """Suppress default HTTP logging"""
        pass

def run_server(port: int = 8080):
    """Run the MCP permission server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, GovPermissionHandler)
    logging.info(f"GOV Permission Server running on port {port}")
    logging.info("Use with: claude-code --permission-prompt-tool http://localhost:8080/permission")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("Server stopped")
        httpd.shutdown()

if __name__ == '__main__':
    run_server()